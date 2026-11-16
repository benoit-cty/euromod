// Number, duration and date formatting for both desktop apps: one place, so
// a count, an elapsed time or a percentage reads the same on every page.

/** 34903 -> "34 903": thin-space thousands, as the reviewers' legal texts write them. */
export function formatCount(n) {
  if (n == null) return '—';
  return Number(n).toLocaleString('en-US').replaceAll(',', ' ');
}

/**
 * A number for display: at most `digits` decimals, en-US grouping ("1,234.5");
 * '—' for a missing value.
 */
export function formatNumber(n, digits = 2) {
  if (n == null || Number.isNaN(Number(n))) return '—';
  return Number(n).toLocaleString('en-US', { maximumFractionDigits: digits });
}

/** Exactly `digits` decimals ("0.12340"); '—' for a missing value. */
export function formatFixed(n, digits = 2) {
  if (n == null || Number.isNaN(Number(n))) return '—';
  return Number(n).toFixed(digits);
}

/** A percentage already on the 0–100 scale: 87.25 -> "87.3%". */
export function formatPercent(v, digits = 1) {
  return v == null ? '—' : `${Number(v).toFixed(digits)}%`;
}

/** Milliseconds as a short duration: "42s", "3m 05s", "2h 07m"; '' when unknown. */
export function formatDuration(ms) {
  if (ms == null || Number.isNaN(ms)) return '';
  const s = Math.max(0, Math.round(ms / 1000));
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${String(s % 60).padStart(2, '0')}s`;
  return `${Math.floor(m / 60)}h ${String(m % 60).padStart(2, '0')}m`;
}
