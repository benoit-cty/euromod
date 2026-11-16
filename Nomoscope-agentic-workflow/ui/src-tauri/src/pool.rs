//! The app's one database, held in Tauri state (both desktop apps; the RAG
//! chat compiles this file in with `#[path]`).
//!
//! The URL — the analyst's login, password included — is read once from the
//! environment and stays on the Rust side: commands never take it from the
//! webview, and what the webview is shown has the password masked
//! ([redact]). A few idle connections are kept and handed out per command
//! instead of a connection per call. Changing the URL ([Db::set_url]) points
//! the whole app at the new database at once and drops the idle connections
//! of the old one.

use crate::pg::connect;
use postgres::Client;
use std::ops::{Deref, DerefMut};
use std::sync::{Arc, Mutex, MutexGuard};
use std::time::Duration;

/// Idle connections kept for reuse; more may be open while commands run.
const MAX_IDLE: usize = 4;
/// An idle connection is checked before reuse (it may have died with a
/// database restart); one that does not answer within this is replaced.
const VALIDATE_TIMEOUT: Duration = Duration::from_secs(2);
/// What a password is shown as.
pub const MASK: &str = "****";

pub const DEFAULT_URL: &str = "postgresql://jrc:jrc@localhost:5434/legislation";

#[derive(Clone)]
pub struct Db {
    inner: Arc<Mutex<Inner>>,
}

struct Inner {
    url: String,
    /// Bumped by every URL change, so a connection opened on the old URL is
    /// not returned to the pool of the new one.
    generation: u64,
    idle: Vec<Client>,
}

impl Db {
    pub fn new(url: String) -> Self {
        Db { inner: Arc::new(Mutex::new(Inner { url, generation: 0, idle: Vec::new() })) }
    }

    /// `WORKFLOW_DATABASE_URL`, else the dev stack's default.
    pub fn from_env() -> Self {
        Db::new(std::env::var("WORKFLOW_DATABASE_URL").unwrap_or_else(|_| DEFAULT_URL.to_string()))
    }

    fn lock(&self) -> MutexGuard<'_, Inner> {
        // A panic while holding the lock leaves plain data behind: keep going.
        self.inner.lock().unwrap_or_else(|poisoned| poisoned.into_inner())
    }

    pub fn url(&self) -> String {
        self.lock().url.clone()
    }

    /// Point the app at another database. The caller has checked it answers.
    pub fn set_url(&self, url: String) {
        let mut inner = self.lock();
        inner.url = url;
        inner.generation += 1;
        inner.idle.clear();
    }

    /// A connection for one command: an idle one that still answers, else a
    /// new one. It goes back to the pool when dropped.
    pub fn client(&self) -> Result<Pooled, String> {
        let (url, generation) = {
            let inner = self.lock();
            (inner.url.clone(), inner.generation)
        };
        loop {
            let idle = self.lock().idle.pop();
            let Some(mut client) = idle else { break };
            if client.is_valid(VALIDATE_TIMEOUT).is_ok() {
                return Ok(Pooled { client: Some(client), db: self.clone(), generation });
            }
        }
        let client = connect(&url)?;
        Ok(Pooled { client: Some(client), db: self.clone(), generation })
    }
}

/// A pooled connection; derefs to `postgres::Client`.
pub struct Pooled {
    client: Option<Client>,
    db: Db,
    generation: u64,
}

impl Deref for Pooled {
    type Target = Client;
    fn deref(&self) -> &Client {
        self.client.as_ref().expect("pooled client taken")
    }
}

impl DerefMut for Pooled {
    fn deref_mut(&mut self) -> &mut Client {
        self.client.as_mut().expect("pooled client taken")
    }
}

impl Drop for Pooled {
    fn drop(&mut self) {
        let Some(client) = self.client.take() else { return };
        if client.is_closed() {
            return;
        }
        let mut inner = self.db.lock();
        if inner.generation == self.generation && inner.idle.len() < MAX_IDLE {
            inner.idle.push(client);
        }
    }
}

/// The URL with its password masked, for display. Both forms libpq accepts:
/// `postgresql://user:password@host/db` and `host=… password=…`.
pub fn redact(url: &str) -> String {
    if let Some((scheme, rest)) = url.split_once("://") {
        let (authority, tail) = split_authority(rest);
        return match authority.rsplit_once('@') {
            Some((userinfo, host)) => match userinfo.split_once(':') {
                Some((user, _)) => format!("{scheme}://{user}:{MASK}@{host}{tail}"),
                None => url.to_string(),
            },
            None => url.to_string(),
        };
    }
    url.split_whitespace()
        .map(|part| match part.split_once('=') {
            Some((key, _)) if key == "password" => format!("password={MASK}"),
            _ => part.to_string(),
        })
        .collect::<Vec<_>>()
        .join(" ")
}

/// A URL typed over a redacted one keeps the current password where the mask
/// still stands in for it: the analyst can change the host or the database
/// without retyping a password the webview never had.
pub fn unredact(new: &str, current: &str) -> String {
    let Some(password) = password_of(current) else { return new.to_string() };
    if let Some((scheme, rest)) = new.split_once("://") {
        let (authority, tail) = split_authority(rest);
        if let Some((userinfo, host)) = authority.rsplit_once('@') {
            if let Some((user, MASK)) = userinfo.split_once(':') {
                return format!("{scheme}://{user}:{password}@{host}{tail}");
            }
        }
        return new.to_string();
    }
    new.split_whitespace()
        .map(|part| if part == format!("password={MASK}") { format!("password={password}") } else { part.to_string() })
        .collect::<Vec<_>>()
        .join(" ")
}

fn password_of(url: &str) -> Option<String> {
    if let Some((_, rest)) = url.split_once("://") {
        let (authority, _) = split_authority(rest);
        let (userinfo, _) = authority.rsplit_once('@')?;
        return userinfo.split_once(':').map(|(_, p)| p.to_string());
    }
    url.split_whitespace()
        .find_map(|part| part.strip_prefix("password=").map(str::to_string))
}

/// `user:pw@host:port` and the `/db?options` after it.
fn split_authority(rest: &str) -> (&str, &str) {
    // the password may contain '/', so the host starts after the last '@'
    let host_start = rest.rfind('@').map(|i| i + 1).unwrap_or(0);
    match rest[host_start..].find(['/', '?']) {
        Some(i) => rest.split_at(host_start + i),
        None => (rest, ""),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn redact_masks_the_password_only() {
        assert_eq!(
            redact("postgresql://jrc:s3cr/t@localhost:5434/legislation?sslmode=disable"),
            "postgresql://jrc:****@localhost:5434/legislation?sslmode=disable"
        );
        assert_eq!(redact("postgresql://jrc@localhost/legislation"), "postgresql://jrc@localhost/legislation");
        assert_eq!(redact("host=db user=ana password=pw dbname=x"), "host=db user=ana password=**** dbname=x");
    }

    #[test]
    fn unredact_restores_the_current_password_behind_the_mask() {
        let current = "postgresql://jrc:pw@localhost:5434/legislation";
        assert_eq!(
            unredact("postgresql://jrc:****@otherhost:5432/legislation", current),
            "postgresql://jrc:pw@otherhost:5432/legislation"
        );
        // a password typed in full is taken as typed
        assert_eq!(
            unredact("postgresql://ana:new@localhost/legislation", current),
            "postgresql://ana:new@localhost/legislation"
        );
        assert_eq!(
            unredact("host=db password=**** dbname=y", "host=db password=pw dbname=x"),
            "host=db password=pw dbname=y"
        );
    }

    /// Connections are reused, and a URL change drops the old database's.
    #[test]
    fn the_pool_reuses_connections_until_the_url_changes() {
        let url = std::env::var("WORKFLOW_DATABASE_URL").unwrap_or_else(|_| DEFAULT_URL.to_string());
        if connect(&url).is_err() {
            return;
        }
        let db = Db::new(url.clone());
        let pid = |db: &Db| -> i32 { db.client().unwrap().query_one("SELECT pg_backend_pid()", &[]).unwrap().get(0) };
        let first = pid(&db);
        assert_eq!(pid(&db), first, "the idle connection is reused");
        db.set_url(url);
        assert_ne!(pid(&db), first, "a new URL starts from fresh connections");
    }
}
