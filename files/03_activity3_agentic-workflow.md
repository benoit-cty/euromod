# Activity 3 — Agentic Workflow + Validation UI (80 units, deadline 15 Dec 2026)

**Deliverable:** documentation of the agentic-workflow architecture. The UI is built *together with the IT team*; the expert documents the architecture and defines the workflow.

---

## 1. Workflow definition (proposal to document)

Target loop, per (country, policy instrument, reference date):

1. **Task framing** — read current parameter value(s) from the model export (Activity 1 format) incl. current legal reference if any.
2. **Retrieval** — query the RAG with `as_of` date; hybrid retrieve candidate legal units; pull structured-extraction results for tables/schedules.
3. **Proposal** — LLM drafts an updated parameter record in the Activity 1 schema: new value, effective dates, pinpoint legal citation, confidence, original-language quote + translation.
4. **Self-check / critique step** — second pass (same or different model) verifies: citation actually contains the value; dates consistent; units/currency sane; schema-valid. Cheap and dramatically reduces silent errors.
5. **Diff & routing** — compare proposal vs. current model value: `unchanged | changed | new | not_found | national_team_source`. Only meaningful diffs go to human review.
6. **Human validation (UI)** — reviewer sees side-by-side: current value, proposed value, cited legal text (original + translation), confidence, provenance. Actions: accept / reject / edit / escalate to national team. Every decision logged (this log *is* future training/validation data).
7. **Write-back** — accepted records exported in the structured format for the modelling team (direct write into EUROMOD files is out of scope unless JRC asks; propose export-first).

Design stance: a **structured pipeline with LLM steps**, not a free-roaming autonomous agent. Determinism where possible (retrieval, schema validation, diffing), LLM where needed (reading law, drafting proposals, critique). This framing also makes the KPI evaluation (Activity 4) tractable.

## 2. Orchestration framework decision

Options on the table — the architecture doc should compare and recommend:
- **LangGraph** (graph-of-steps fits the pipeline framing; good state/checkpointing),
- LangChain plain (fine for a linear pipeline, weaker at branching/review loops),
- CrewAI (multi-agent framing probably overkill here),
- **ALOHA (EC-JRC)** — politically attractive (in-house), but known concerns: maturity, infra complexity, OpenAI-only endpoints. Since Activity 5 requires comparing *different LLMs*, endpoint flexibility is a hard requirement → position ALOHA as a possible orchestration host with LangGraph inside, or defer.
- **MCP** for the structured national-team database integration (Luis's approach) — document as the tool-interface layer regardless of orchestrator.

Model access: multi-provider needed (GPT-4o via Bedrock/Azure?, Anthropic API, possibly open-weight for a cost/sovereignty comparison point). Confirm what JRC procurement/infra actually allows — this is a kick-off question with contractual weight.

## 3. Validation UI (with IT team, Kosta's domain)

- Keep the expert's role to: review-workflow specification, data contract (Activity 1 schema in/out), decision-log schema. 
- Stack candidates already discussed: Tauri + Svelte; but a plain web app on JRC infra may be simpler for a multi-user review tool — raise at kick-off, don't pre-commit.
- Minimum screens: review queue (filterable by country/instrument/status/confidence), record detail (side-by-side + citation viewer), audit log.

## 4. Document outline (the deliverable)

1. Workflow overview & design principles (pipeline-with-LLM-steps, human-in-the-loop)
2. Step-by-step specification (inputs/outputs/failure modes per step)
3. Orchestrator comparison & recommendation
4. Prompt & model-version management (prompts are versioned artefacts in GitLab)
5. Tool interfaces (RAG API, structured DB via MCP, schema validators)
6. UI review workflow & decision-log schema
7. Observability: run IDs, retrieval traces, token/cost logging (feeds KPI report)
8. Security & guardrails (schema enforcement, no write-back without human acceptance)

## 5. Sequencing & dependencies

- Can start as soon as Activity 1 schema is frozen (Aug) using a mocked RAG; swap in the real RAG as Activity 2's vertical slice lands (Oct).
- Deadline shared with Activity 4 (15 Dec) → run them interleaved: every workflow run on the golden set produces KPI numbers.

## 6. Risks

- Endpoint constraints discovered late (ALOHA/OpenAI-only, Bedrock availability) → resolve at kick-off.
- Hallucinated citations → mitigated by critique step + "citation must quote retrieved chunk verbatim" rule + UI showing the source text.
- Scope creep toward full autonomy — the contract says *propose* updates; human validation is the product, not a fallback.
