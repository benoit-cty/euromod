// The hand-off prompt: everything a review item knows about a parameter, as
// one block of text a reviewer pastes into an external chat assistant (Claude,
// …) when the pipeline did not settle it — not_found, provisional, or a
// proposal the reviewer doubts. The UI only builds text; it calls no model.
//
// `context` is api.parameterContext(): the parameter's EUROMOD texts,
// law-language texts and value history (every member for a `group:` target).
// It is optional — the prompt is still useful from the queue item alone.

import { countryName, routingLabel } from '../../../shared/lib/labels.js';

// Official portals per country — the same list the scout searches
// (scout.COUNTRY_SOURCES), with the law's language.
export const COUNTRY_SOURCES = {
  FR: {
    lang: 'French',
    portals: [
      'legifrance.gouv.fr (lois, décrets, arrêtés, codes, conventions collectives KALI)',
      'bofip.impots.gouv.fr (doctrine)',
      'legislation.lassuranceretraite.fr (Cnav circulars)',
      'unedic.org (circulars)',
    ],
  },
  ES: {
    lang: 'Spanish',
    portals: [
      'boe.es (Boletín Oficial del Estado: consolidated legislation and the daily gazette)',
      'the autonomous community’s own official bulletin for a regional parameter',
    ],
  },
  NL: {
    lang: 'Dutch',
    portals: ['wetten.overheid.nl (Basiswettenbestand)', 'zoek.officielebekendmakingen.nl (Staatscourant, Staatsblad)'],
  },
  IE: {
    lang: 'English',
    portals: [
      'irishstatutebook.ie (Acts and Statutory Instruments)',
      'gov.ie / revenue.ie (official rates published by the department)',
    ],
  },
  LT: { lang: 'Lithuanian', portals: ['e-tar.lt (Teisės aktų registras)', 'e-seimas.lrs.lt'] },
  BE: { lang: 'French and Dutch', portals: ['ejustice.just.fgov.be (Moniteur belge / Belgisch Staatsblad)'] },
};

const LAW_LANG = { FR: 'fr', ES: 'es', NL: 'nl', IE: 'en', LT: 'lt', BE: 'fr' };

const TEMPORAL_BASIS = {
  in_force: (year) =>
    `the value in force during ${year}. EUROMOD reads it on 1 July ${year}; a change entering into force later in ${year} counts too — then give both values and their dates.`,
  income_year: (year) =>
    `the value EUROMOD applies to the incomes of ${year}. The law labels it by the income year one year earlier: it is in the act/article for «income ${year - 1}» (e.g. the finance act for ${year}).`,
  start_of_year: (year) => `the value in force on 1 January ${year} (not a revision later in ${year}).`,
};

function en(texts, field) {
  const t = texts?.[field];
  if (!t) return null;
  return t.en ?? Object.values(t)[0] ?? null;
}

function showValue(entry) {
  if (!entry) return '—';
  if (entry.raw != null && entry.raw !== '') return String(entry.raw);
  const value = entry.value;
  if (value == null) return 'n/a';
  return typeof value === 'object' ? JSON.stringify(value) : String(value);
}

function itemValue(pv) {
  if (!pv || pv.value == null) return '—';
  return typeof pv.value === 'object' ? JSON.stringify(pv.value) : String(pv.value);
}

function describeParameter(p, country, { member = false } = {}) {
  const lines = [];
  const head = member ? `- ${p.name ?? p.model_target}${p.group_role ? ` (${p.group_role})` : ''}` : null;
  if (head) lines.push(head);
  const pad = member ? '  ' : '';
  // a short label that is just the variable name says nothing
  const short = en(p.texts, 'short_label');
  const fullLabel = en(p.texts, 'label');
  const labels = [short !== p.name ? short : null, fullLabel].filter((l, i, all) => l && all.indexOf(l) === i);
  if (labels.length) lines.push(`${pad}Label: ${labels.join(' — ')}`);
  const description = en(p.texts, 'description');
  if (description) lines.push(`${pad}Description: ${description}`);
  const explanation = en(p.texts, 'explanation');
  if (explanation) lines.push(`${pad}EUROMOD note: ${explanation}`);
  const lawLang = LAW_LANG[country];
  for (const t of p.law_texts ?? []) {
    if (t.lang === lawLang && t.lang !== 'en' && (t.field === 'label' || t.field === 'description')) {
      lines.push(`${pad}In the law’s language (${t.origin.replace('_', ' ')}): ${t.content}`);
    }
  }
  if (p.unit) lines.push(`${pad}Unit in EUROMOD: ${p.unit}`);
  const history = (p.history ?? []).slice(-6);
  if (history.length) {
    lines.push(
      `${pad}Values EUROMOD has held: ` +
        history.map((h) => `${h.system_year ?? h.valid_from?.slice(0, 4)}: ${showValue(h)}`).join('; '),
    );
  }
  return lines;
}

function uniqueCitations(trace) {
  const seen = new Map();
  for (const hit of trace ?? []) {
    const key = hit.citation ?? hit.context_header;
    if (!key || seen.has(key)) continue;
    seen.set(key, hit.validity ? `${key} (${hit.validity})` : key);
  }
  return [...seen.values()];
}

/** The prompt text for one review item. */
export function buildHandoffPrompt(item, context = null) {
  const country = item.country;
  const year = item.system_year ?? Number(item.as_of?.slice(0, 4));
  const params = context?.parameters ?? [];
  const isGroup = item.model_target?.startsWith('group:') || params.length > 1;
  const basis = params[0]?.temporal_basis ?? 'in_force';
  const sources = COUNTRY_SOURCES[country];
  const out = [];

  out.push(
    `I maintain EUROMOD, the EU tax-benefit microsimulation model. I need the legal value of one ` +
      `${isGroup ? 'tax/benefit schedule' : 'policy parameter'} for ${countryName(country)} (${country}), ` +
      `system year ${year}, found in the official legislation and quoted word for word. ` +
      `Our automated legislation assistant could not settle it, so please research it on the web.`,
  );

  out.push('', '## The parameter');
  out.push(`EUROMOD id: ${item.model_target}`);
  if (item.label && item.label !== item.model_target) out.push(`Name: ${item.label}`);
  out.push(`Value type: ${item.value_type ?? '—'} · unit: ${item.unit ?? '—'}`);
  if (!params.length) {
    out.push(`Value EUROMOD holds now: ${itemValue(item.current_value)}`);
  } else if (isGroup) {
    out.push('Members of the schedule:');
    for (const p of params) out.push(...describeParameter(p, country, { member: true }));
  } else {
    out.push(...describeParameter(params[0], country));
  }
  out.push(`What is wanted: ${(TEMPORAL_BASIS[basis] ?? TEMPORAL_BASIS.in_force)(year)}`);

  out.push('', '## What our assistant already tried');
  out.push(`Outcome: ${routingLabel(item.routing).label}.`);
  if (item.proposed_value) {
    const ref = item.proposed_value.references?.[0];
    out.push(
      `It proposed ${itemValue(item.proposed_value)} from ${item.proposed_value.valid_from ?? '?'}` +
        (ref ? `, citing ${ref.title ?? ref.legal_unit_ref ?? 'a text'}` : '') +
        '. Check it independently; do not take it as given.',
    );
    if (ref?.supporting_extract) out.push(`Its quote: «${ref.supporting_extract}»`);
  }
  for (const issue of item.critique?.issues ?? []) {
    if (/^no value proposed$/i.test(issue)) continue;
    out.push(`- ${issue.replace(/^model:\s*/i, 'Its reasoning: ')}`);
  }
  const scout = item.scout;
  if (scout?.needs?.length) {
    out.push('It said it was missing:');
    for (const need of scout.needs) out.push(`- ${need}`);
  }
  if (scout?.reasoning) out.push(`Its search notes: ${scout.reasoning}`);
  const read = uniqueCitations(item.retrieval_trace);
  if (read.length) {
    out.push(
      `Texts it read (our corpus, ${read.length}): ${read.slice(0, 12).join('; ')}` + (read.length > 12 ? '; …' : ''),
    );
  }

  out.push('', '## How to answer');
  if (sources) {
    out.push(`Use official primary sources, in ${sources.lang} where the law is: ${sources.portals.join('; ')}.`);
  } else {
    out.push('Use official primary sources: the national official journal and consolidated legislation portal.');
  }
  out.push(
    '- The source of truth is the legal text (act, decree, order, collective agreement) or, failing that, ' +
      'official administrative guidance (circular, ministry publication) — say which it is.',
    '- Do NOT use the EUROMOD Country Report, OpenFisca, news or commercial sites as evidence; they may point you to the law, nothing more.',
    `- Give the value in EUROMOD’s unit (${item.unit ?? 'as above'}). If the law states it in another unit or ` +
      'EUROMOD holds a modelling convention (days vs months, a monthly vs yearly amount, a percentage as a fraction), ' +
      'quote the law’s figure and show the conversion explicitly.',
    '- If the value is computed (a base × a coefficient, a revaluation), give each operand with its own verbatim quote and the arithmetic.',
    '- If you cannot find a text stating it, say so plainly. Do not guess and do not fall back on the value EUROMOD holds.',
    '',
    'Reply with this block (the quote copied character for character, in the original language):',
    '',
    'VALUE: <number or schedule, in EUROMOD’s unit>',
    'UNIT: <unit>',
    'IN FORCE FROM: <YYYY-MM-DD> (to <YYYY-MM-DD> if it ends within the year)',
    'SOURCE: <act title, number and date — article/paragraph>',
    'SOURCE TYPE: legislation | administrative guidance',
    'OFFICIAL URL: <link to the official text, ideally the article>',
    'QUOTE: «<verbatim extract stating the figure>»',
    'CONVERSION / DERIVATION: <none, or the arithmetic with each operand’s quote>',
    `SAME AS EUROMOD (${itemValue(item.current_value)})?: yes | no — <one line>`,
    'CONFIDENCE AND CAVEATS: <one or two lines>',
  );
  return out.join('\n');
}
