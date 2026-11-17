// The UI's vocabularies stay in step with the database and the worker (code
// audit 2.1): the units and source types params.edit_parameter() accepts, and
// the job types the worker publishes in Nomergon-worker/job_types.json.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { SOURCE_TYPES, UNITS } from './vocabulary.js';
import { jobTypeLabel } from '../../../shared/lib/labels.js';

const root = new URL('../../../../', import.meta.url);
const sql = readFileSync(new URL('Nomoscope-agentic-workflow/pipeline/db/params_schema.sql', root), 'utf8');

function sqlList(field) {
  const m = new RegExp(`p_field = '${field}'[\\s\\S]*?NOT IN\\s*\\(([^)]*)\\)`).exec(sql);
  assert.ok(m, field);
  return [...m[1].matchAll(/'([^']+)'/g)].map((x) => x[1]).sort();
}

test('units match edit_parameter()', () => {
  assert.deepEqual([...UNITS].sort(), sqlList('unit'));
});

test('source types match edit_parameter()', () => {
  assert.deepEqual([...SOURCE_TYPES].sort(), sqlList('source_type'));
});

test('every worker job type has a plain label', () => {
  const spec = JSON.parse(readFileSync(new URL('Nomergon-worker/job_types.json', root), 'utf8'));
  for (const { name } of spec.job_types) {
    assert.ok(jobTypeLabel(name).hint, `no label for job type ${name}`);
  }
});
