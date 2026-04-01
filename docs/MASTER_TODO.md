# Master TODO (Execution Plan + Anti-Hallucination Controls)

## Usage
Track this checklist as the single source of truth for implementation progress.  
Status values to use: `[ ] pending`, `[-] in progress`, `[x] done`, `[!] blocked`.

## Phase 0 - Project Baseline
- [ ] Confirm runtime path (`local`, `vercel`, or both).
- [ ] Standardize one startup command for local development.
- [ ] Verify env variable policy (`.env.example` only, no real keys in repo).
- [ ] Remove or quarantine sensitive local files from version control patterns.
- [ ] Define single canonical docs index in `docs/`.

## Phase 1 - Data and Schema Foundation
- [ ] Build data ingestion script: Excel/CSV -> cleaned dataframes.
- [ ] Enforce column naming conventions (`snake_case`, no spaces).
- [ ] Load to target SQL database (SQLite for dev + PostgreSQL for production-like).
- [ ] Generate schema manifest:
  - [ ] table list
  - [ ] column list + types
  - [ ] PK/FK relationships
  - [ ] nullable/default flags
- [ ] Add business glossary mapping file (aliases/synonyms).
- [ ] Create automated schema sanity checks.

## Phase 2 - NL2SQL Pipeline Core
- [ ] Implement API endpoint for chat query intake.
- [ ] Implement schema retrieval component.
- [ ] Implement prompt builder with strict SQL-only contract.
- [ ] Implement SQL generator service (LLM call wrapper).
- [ ] Implement SQL validator/safety gate.
- [ ] Implement SQL runner abstraction.
- [ ] Implement response formatter (table + narrative).
- [ ] Add conversation context handling.

## Phase 3 - Hallucination Guardrails (Critical)
- [ ] Add unknown identifier detector (tables/columns not in schema).
- [ ] Add approved join-path enforcement.
- [ ] Add SQL denylist:
  - [ ] `DROP`
  - [ ] `DELETE`
  - [ ] `TRUNCATE`
  - [ ] `ALTER`
  - [ ] multi-statement blocks
- [ ] Add ambiguity detector:
  - [ ] if multiple plausible entities exist, ask clarifying question.
- [ ] Add "no confident answer" fallback template.
- [ ] Add prompt injection protections:
  - [ ] sanitize user text
  - [ ] strip tool/system override patterns
  - [ ] enforce final parser contract.
- [ ] Log hallucination incidents with root-cause category.

## Phase 4 - Evaluation Framework
- [ ] Build benchmark dataset (`question`, `expected_sql`, `expected_result`).
- [ ] Tag question difficulty and intent type.
- [ ] Implement evaluation runner with batch mode.
- [ ] Track metrics:
  - [ ] SQL validity
  - [ ] execution success
  - [ ] result correctness
  - [ ] latency
  - [ ] token/cost (if available)
  - [ ] hallucination rate
- [ ] Generate markdown report after each run.
- [ ] Create release gate thresholds for deployment approval.

## Phase 5 - Security, Access, and Compliance
- [ ] Add user resolver with real identity context.
- [ ] Add access groups for sensitive tool execution.
- [ ] Add structured audit logs for every query.
- [ ] Add basic rate limiting and abuse controls.
- [ ] Ensure secrets are loaded via env/secret manager only.
- [ ] Create incident response checklist for unsafe query attempts.

## Phase 6 - Developer Experience and Reliability
- [ ] Add `Makefile`/PowerShell task shortcuts (setup, run, test, eval).
- [ ] Add smoke tests for startup + health endpoint.
- [ ] Add CI checks (lint + tests + evaluation sanity run).
- [ ] Add clear error messages and troubleshooting guide.
- [ ] Add model/provider fallback strategy.

## Phase 7 - UI and Product Experience
- [ ] Ensure frontend supports:
  - [ ] streaming updates
  - [ ] SQL visibility toggle by role
  - [ ] result table rendering
  - [ ] narrative summary
- [ ] Add follow-up question UX with conversation state.
- [ ] Add "query explanation" panel for trust and transparency.

## Phase 8 - Production Readiness
- [ ] Define deployment topology and environment configs.
- [ ] Add observability dashboards (latency, failures, hallucination rate).
- [ ] Run load and resilience tests.
- [ ] Execute UAT with non-technical users.
- [ ] Sign off go-live checklist.

## Immediate Next Sprint (Recommended)
- [ ] Implement schema manifest + retrieval first.
- [ ] Add SQL validator and unknown identifier checks.
- [ ] Prepare first benchmark set (at least 30 questions).
- [ ] Run baseline evaluation on one selected LLM.
- [ ] Document failure analysis and top 5 prompt improvements.

## Done Criteria (Project-Level)
- [ ] Benchmark target reached and stable for 3 consecutive runs.
- [ ] Hallucination rate reduced to agreed threshold.
- [ ] No destructive SQL execution path possible.
- [ ] Reproducible setup for a new developer in <= 30 minutes.
- [ ] Project docs fully aligned with actual runtime behavior.
