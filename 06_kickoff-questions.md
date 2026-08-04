# Kick-off Meeting — Consolidated Question List

Grouped by theme; the ⭐ items materially affect deliverables or contractual feasibility and must be answered in the meeting.

## A. Scope & country selection
1. ⭐ Which 5 member states? Criteria = accessibility × language spread. Proposal to discuss: France, Ireland, + one hard-access (EL/BG), one API-rich (EE/FI), one large/complex (ES/DE). Who has national-team contacts for each candidate?
2. ⭐ Fiscal models in scope for the parameter format: EUROMOD only, or also EDGE-M3 / DIRECT (even as extensibility examples)?
3. Which policy domains within fiscal law for the pilot (PIT, SIC, main benefits)? Full country systems are too big for a pilot.
3b. ⭐ Retrieval strategy fork (see `10_retrieval-strategy-challenge.md`): does JRC expect an exhaustive ingested corpus as an asset, or is a lazy, agent-populated cache acceptable as the RAG's corpus? Does the Deliverable 2 reviewer accept the "retrieval-first RAG" reading of Activity 2?
4. Which EUROMOD system years anchor the pilot (e.g. reproduce the 2024→2025 update)?

## B. Data & ground truth
5. ⭐ Can JRC export EUROMOD parameter files for several past system years for the pilot countries (golden-set ground truth)?
6. Status of Hannes's Ireland JSON DB — schema, lessons, should Activity 1 align with it?
7. Access to EUROMOD Country Reports source files (not just PDFs)?
8. For non-codified parameters: what is the current channel with national teams, and can it feed a structured DB (MCP interface)?

## C. Infrastructure & tooling (with IT team)
9. ⭐ Where does this run? JRC infrastructure, AWS Bedrock availability, GPU access for embeddings/reranking, database hosting (PostgreSQL available?).
10. ⭐ Which LLM endpoints are permitted/procured? (Contract requires comparing different LLMs → multi-provider access is a hard requirement. Direct bearing on ALOHA's OpenAI-only limitation.)
11. Is ALOHA expected/desired as the orchestration layer, or is the choice open (LangGraph etc.)?
12. JRC GitLab: repo structure, CI availability, code review norms, licensing of deliverable code.
13. Any data-handling constraints on national legal texts or on sending them to external LLM APIs?

## D. Ways of working
14. ⭐ Acceptance criteria per deliverable (payments are acceptance-gated) — agree in writing.
15. Division of labour expert ↔ IT team for Activity 2 implementation and Activity 3 UI (who codes what; role on UI?).
16. Fortnightly call slot + standing agenda; async channel (email? Teams?).
17. Seville visit timing — propose Sep/Oct during architecture drafting (contract ties it to Activities 1–2).
18. Roles of the team on the JRC side; who reviews which deliverable?

## E. Report & publication
19. Technical report template, publication channel, clearance timeline (does 31 Dec mean draft-final or cleared-final?).
20. Authorship expectations.

## F. Legal/admin (contract hygiene)
21. Invoicing procedure for interim payment (after D1+D2 acceptance) and final payment.
22. Travel booking/reimbursement process for the Seville visit.
