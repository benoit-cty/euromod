import { test } from 'node:test';
import assert from 'node:assert/strict';
import { acceptGate, buildForm, editedFields, newReference, parsedValue } from './proposal.js';

const proposed = {
  value: 0.25,
  valid_from: '2025-01-01',
  legal_status: 'enacted_in_force',
  source_type: 'legislation',
  references: [
    { title: 'CGI art. 197', jrc_database_id: 'c1', source_trust_class: 'evidence', supporting_extract: '25 %', extract_offsets: [3, 7] },
  ],
};

test('the form holds the proposal as editable text', () => {
  const form = buildForm(proposed);
  assert.equal(form.brackets, false);
  assert.equal(form.valueText, '0.25');
  assert.equal(form.references[0]._extract_orig, '25 %');
  assert.equal(form.references[0].source_trust_class, 'evidence');
  assert.equal(buildForm(null), null);
  const brackets = buildForm({ value: [{ threshold: 0, rate: 0 }] });
  assert.equal(brackets.brackets, true);
  assert.match(brackets.valueText, /"threshold": 0/);
});

test('Accept is gated on dates, legal status and a quote', () => {
  const form = buildForm(proposed);
  assert.deepEqual(acceptGate(form, 'changed'), { ok: true, reason: '' });
  assert.equal(acceptGate(null, 'changed').ok, false);
  assert.match(acceptGate(form, 'provisional').reason, /^provisional/);
  assert.match(acceptGate({ ...form, valid_from: '' }, 'changed').reason, /valid from/);
  assert.match(acceptGate({ ...form, valid_to: '31/12/2025' }, 'changed').reason, /^Valid to must be a date/);
  assert.match(acceptGate({ ...form, legal_status: '' }, 'changed').reason, /legal status/);
  const unquoted = { ...form, references: [{ ...form.references[0], supporting_extract: '  ' }] };
  assert.match(acceptGate(unquoted, 'changed').reason, /no reference quotes the law/);
  // the national team needs no quote
  assert.equal(acceptGate({ ...unquoted, source_type: 'national_team' }, 'changed').ok, true);
});

test('the edited value is parsed the way EUROMOD holds it', () => {
  const form = buildForm(proposed);
  assert.equal(parsedValue({ ...form, valueText: ' 0.3 ' }), 0.3);
  assert.equal(parsedValue({ ...form, valueText: '$PSS * 4' }), '$PSS * 4');
  assert.equal(parsedValue({ ...form, valueText: '' }), null);
  assert.equal(parsedValue({ ...form, valueText: '{"a": 1}' }), '{"a": 1}', 'an object is not a scalar');
  assert.deepEqual(parsedValue({ brackets: true, valueText: '[{"rate": 0.1}]' }), [{ rate: 0.1 }]);
  assert.throws(() => parsedValue({ brackets: true, valueText: '[{' }));
});

test('a hand-edited quote loses its verified offsets', () => {
  const form = buildForm(proposed);
  assert.deepEqual(editedFields(form, 0.25).references[0].extract_offsets, [3, 7]);
  form.references[0].supporting_extract = '25 pour cent';
  const fields = editedFields(form, 0.25);
  assert.equal(fields.references[0].extract_offsets, null);
  assert.equal(fields.value, 0.25);
  assert.equal(fields.valid_to, null);
  form.references.push(newReference());
  assert.equal(editedFields(form, null).references[1].supporting_extract, null);
});
