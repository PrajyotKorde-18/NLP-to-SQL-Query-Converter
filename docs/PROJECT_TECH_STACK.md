# Project Tech Stack (Domain-Agnostic Text-to-SQL)

## Objective
Build a production-capable, domain-agnostic NL2SQL assistant that:
- accepts natural-language business questions,
- generates safe SQL,
- executes against relational databases,
- returns table + narrative responses,
- minimizes hallucinations with schema-grounded retrieval and evaluation.

## Core Runtime Stack
- `Python 3.10+` as primary backend language.
- `FastAPI` for API and SSE streaming endpoints.
- `Vanna` framework components already present in this repo (`src/vanna/*`).
- `SQLAlchemy` for database abstraction where needed.
- `pandas` for tabular transforms and evaluation prep.
- `uvicorn` as local ASGI server.

## LLM Layer
- Primary inference provider (current): `Groq OpenAI-compatible endpoint` via `OpenAILlmService`.
- Default model in repo: `llama-3.3-70b-versatile`.
- Optional providers already supported by repo architecture:
  - OpenAI, Anthropic, Gemini, Bedrock, Ollama, Mistral, etc.
- Recommendation:
  - keep one default production model,
  - run periodic offline benchmark against 2-4 alternatives.

## Data and Database Layer
- Development/demo DBs:
  - `SQLite` (`Chinook.sqlite`) for quick bootstrap.
  - `PostgreSQL` via `EnhancedPostgresRunner` for production-like testing.
- Source data onboarding path (project scope):
  - Excel/CSV -> preprocessing -> relational tables -> schema metadata extraction.
- Future database adapters (already feasible in codebase):
  - MySQL, Snowflake, BigQuery, Redshift, Oracle, SQL Server, DuckDB.

## Retrieval + Grounding Strategy
- Grounding source: DDL/schema memories + limited sampled rows (optional).
- Retrieval memory: `DemoAgentMemory` in current local implementation (upgrade path: persistent store).
- Recommended grounding payload:
  - table names,
  - column names/types,
  - foreign key relationships,
  - business glossary aliases,
  - approved join paths.

## API + Interface
- Backend:
  - FastAPI app via `VannaFastAPIServer`.
  - Chat endpoint with streamable outputs.
- Frontend:
  - Existing static app (`static/index.html`) and/or web component.
- Output format:
  - generated SQL (role-gated),
  - query result table,
  - concise natural language explanation.

## Evaluation and Quality Stack
- Unit and integration tests: `pytest`, `pytest-asyncio`.
- SQL/result quality evaluation:
  - exact-match (SQL canonicalized),
  - execution accuracy,
  - result equivalence,
  - latency and token cost.
- Hallucination controls:
  - schema-constrained prompting,
  - SQL validator/linter,
  - denylist for destructive SQL,
  - confidence/fallback response path.

## Security and Governance
- Environment-based secret management (`GROQ_API_KEY`, DB creds).
- User/role controls through resolver + tool access groups.
- Row-level policies (roadmap for enterprise mode).
- Query audit logging and traceability (request id, user id, SQL, execution status).

## Dev Tooling and Ops
- Code quality: ruff/pytest/tox configurations already present.
- Deployment targets:
  - local workstation (primary),
  - Vercel API style deployment path exists (`api/index.py`),
  - containerization recommended for production parity.
- Monitoring (recommended):
  - request latency,
  - SQL failure rate,
  - hallucination/fallback rate,
  - top failed intents.

## Minimal Production Stack Recommendation
- FastAPI + Vanna + PostgreSQL runner.
- One primary LLM provider + one fallback provider.
- Persistent schema metadata store.
- Prompt/version registry.
- Automated evaluation suite before model/prompt release.
