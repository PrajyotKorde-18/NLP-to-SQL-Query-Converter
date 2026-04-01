# Project Requirements (Domain-Agnostic Text-to-SQL)

## 1) Problem Statement
Non-technical users need database insights without writing SQL.  
The system must translate natural language into executable SQL and return accurate, explainable results across different business domains.

## 2) Scope
In scope:
- Domain-agnostic translation mapping arbitrary questions to database schemas via prompt engineering and metadata mapping.
- Data ingestion capabilities for Excel/CSV into a relational database.
- Read-only execution of generated SQL on selected database connections.
- Robust guardrails against SQL injection, data modifications (DML), and schema modifications (DDL).
- Web-based interface to submit queries and view results + plain-text explanations.
- Evaluation metrics framework to gauge accuracy, execution success, and response latency.

Out of Scope:
- Advanced analytics requiring code execution outside SQL.
- Large scale data pipelining or warehousing beyond demo/evaluation scope.
- State-altering SQL commands.

## 3) Functional Requirements
- System shall parse user's natural language input.
- System shall construct context including database schema, mapping, and examples.
- System shall interface with an LLM via defined endpoints (e.g., Groq OpenAI-compatible endpoints) using specifically tailored prompts.
- System shall accurately extract the SQL query and the narrative explanation from the LLM output.
- System shall validate the SQL against a robust denylist (e.g., DROP, DELETE, INSERT, UPDATE, ALTER, TRUNCATE, MULTI-STATEMENT).
- System shall execute validated analytical queries against the specified SQLite or PostgreSQL runtime.
- System shall provide the execution results (tabular data) and narrative explanation back to the requester.

## 4) Non-Functional Requirements
- **Performance**: High availability and low latency streaming response via FastAPI and SSE.
- **Security**: Environment-based config for API keys. Strong prevention of arbitrary code/SQL execution vulnerabilities.
- **Portability**: Support for deployment onto local machines, Vercel APIs, or containerized endpoints.
- **Extensibility**: Capability to swap LLM providers or plug in new database connectors with minimal code change.

## 5) Anti-Hallucination Requirements
- **Identifier Verification**: System must verify tables/columns used in SQL exist in the known schema mapping.
- **Approved Joins**: System should check against a known set of valid foreign key relationships.
- **Fallback**: System shall decline queries explicitly when there is insufficient data/context instead of guessing randomly.
- **Prompt Injection**: System must actively sanitize and quarantine edge-case user prompts.
