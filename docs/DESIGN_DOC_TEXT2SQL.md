# Design Document: Domain-Agnostic Text-to-SQL Assistant

## 1. Purpose
This document defines the end-to-end architecture for a robust Text-to-SQL assistant that can work across industries by relying on schema grounding rather than domain-specific hardcoding.

## 2. High-Level Architecture
1) Data onboarding
2) Schema manifest extraction and metadata memory
3) Natural Language Chat Interface
4) Prompt construction and Entity grounding
5) LLM Text-to-SQL generation
6) Safety/Validation gate (Guardrails)
7) Database Execution Layer
8) Delivery of Result and Explanation back to interface

## 3. Component Details
- **Schema Management Component**: Extracts schema metadata (tables, columns, datatypes) automatically from connected relational databases.
- **Inference Service**: Pluggable LLM interface connecting primarily to an LLM provider endpoint. Uses predefined roles and boundaries to keep responses constrained.
- **Query Guard Layer**: Inspects the generated text. Parses the generated SQL string using an AST or regex pattern validator to assert that it is a SELECT/analytical query and doesn't target restricted/blacklisted functions (e.g. `DROP`, `DELETE`).
- **Database Executor**: Wraps standard DBAPI/SQLAlchemy calls specifically enforcing limited execution rights. Automatically adds `LIMIT 100` to prevent result buffer overflow.
- **Formatter**: Assembles the execution artifact (data result dataframe or JSON array) and textual narrative to feed back to the conversational interface.

## 4. Failure Modes and Mitigation
### LLM Hallucinations
- *Mode*: LLM invents tables, columns, or bad relationships.
- *Mitigation*: Schema constraints during prompt stage. Denylist mechanisms. Hard verification of AST nodes against the schema graph.

### Destructive Queries
- *Mode*: Prompt injection forces LLM to output a `DROP TABLE` statement.
- *Mitigation*: Stringent validation layer (Query Guard) checking for analytical keywords only before passing down to the Database Executor.

### Bad/Long Output
- *Mode*: The executed query runs a Cartesian join that returns too much data, freezing the service.
- *Mitigation*: Enforcement of analytical result limits and timeouts at the Database Executor level.
