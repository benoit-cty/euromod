// Duration formatting for both desktop apps: one place, so an elapsed time
// reads the same on every page.

/** Milliseconds as a short duration: "42s", "3m 05s", "2h 07m"; '' when unknown. */
export function formatDuration(ms) {
  if (ms == null || Number.isNaN(ms)) return '';
  const s = Math.max(0, Math.round(ms / 1000));
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, '0')}s`;
  return `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, '0')}m`;
}
