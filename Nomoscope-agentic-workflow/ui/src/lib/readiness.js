// One verdict per country from the corpus statistics (`db_stats`): can the
// assistant work on this country's parameters today, and if not, why not.
// The detailed tables stay available on the Legislation page; this is the
// one-line answer a reviewer actually needs.

/**
 * @param row     one `stats.by_country` entry
 * @param inputs  the matching `stats.model_inputs.by_country` entry (may be undefined)
 * @returns {{ level: 'ready'|'partial'|'missing', problems: string[], embeddedPct: number|null, englishPct: number|null }}
 */
export function countryReadiness(row, inputs) {
  const problems = [];
  const pct = (part, whole) => (whole ? Math.round((part / whole) * 100) : null);
  const embeddedPct = pct(row?.embedded_chunks ?? 0, row?.chunks ?? 0);
  const englishPct = pct(row?.en_versions ?? 0, row?.text_versions ?? 0);

  if (!row || !row.instruments) {
    return { level: 'missing', problems: ['no legislation in the library yet'], embeddedPct, englishPct };
  }
  if (embeddedPct != null && embeddedPct < 100) {
    problems.push(`${100 - embeddedPct}% of texts not yet searchable (embeddings to build)`);
  }
  if (!inputs?.parameters) problems.push('EUROMOD parameters not loaded');
  if (!(inputs?.country_report?.reports > 0)) problems.push('no Country Report');

  // Without parameters there is nothing to check; the rest only degrades quality.
  const level = !inputs?.parameters ? 'missing' : problems.length ? 'partial' : 'ready';
  return { level, problems, embeddedPct, englishPct };
}
