//! The desktop apps' SQL reads, one module per subject. Writes are not here:
//! decisions and metadata edits go through `store.rs` (the sanctioned SQL
//! functions), jobs through `jobs.rs`, golden verdicts through `golden.rs`.
//!
//! - [corpus]: the legislation DB's library status (Database tab, Overview,
//!   Add-sources pickers) and the instrument picker of a contributed document;
//! - [search]: the article search and a hit's language renderings, shared with
//!   the RAG chat (compiled in there with `#[path]`);
//! - [eval]: the `eval` schema's runs and results (Evaluation tab);
//! - [params]: the `params` schema's parameters, edits and decisions;
//! - [phoenix]: Phoenix project ids for trace deep-links.

pub mod corpus;
pub mod eval;
pub mod params;
pub mod phoenix;
pub mod search;
