# ValidateAI

input
 ↓
validate
 ↓
plan
 ↓
ui
 ↓
sql_generation
 ↓
db_query
 ↓
comparison
 ↓
report
 ↓
END

## 🔐 Environment Variables Setup

This project relies on environment variables for configuration (API keys, model settings, tracing, etc.).

> These variables are **injected at runtime via Makefile** and consumed using **Pydantic Settings**.

---

### ⚙️ Option 1: Global Setup using (`.bashrc`) (Recommended)

You can define environment variables globally in your local environment.

#### 1. Open your bash configuration:

```bash
nano ~/.bashrc
```

#### 2. Add the following:

```bash
export LLM_GROQ_API_KEY="your_groq_api_key"
export LLM_MODEL="llama-3.1-8b-instant"


#### 3. Apply changes:

```bash
source ~/.bashrc
```

#### 4. Verify:

```bash
echo $LLM_GROQ_API_KEY
```

---

### 🚀 Running the Application

The project uses a Makefile to pass environment variables at runtime:

```bash
make run-agent
```

Example (simplified):

```make
run-agent:
	LLM_GROQ_API_KEY=$(LLM_GROQ_API_KEY) \
	uv run python -m gen_agent.main
```

---

### How to install OS level packages
```make
import subprocess

subprocess.run(["playwright", "install-deps", "chromium"])

```

## Install SQLite CLI
```make
sudo apt update
sudo apt install sqlite3
```

### Check Backend DB
```make
make sqlite-view
```

### Show Tables
```make
.tables
```

### Describe Table

```make
.schema player_metrics
```
### Show Data
```make
SELECT * FROM player_metrics;
```


### 🧠 How It Works

* Environment variables are defined in `.bashrc` (global scope)
* `make run-agent` passes them into the runtime environment
* **Pydantic Settings** reads them inside the application
* No direct dependency on `.env` is required

---

### ⚠️ Notes

* Do **not** hardcode API keys in code
* Do **not** commit secrets to Git
* Rotate keys if exposed
* Restart terminal or run `source ~/.bashrc` if variables are not picked up

---


## Rough Knowledge



`
User → FastAPI → LangGraph Agent
                     ↓
              (Groq LLM)
                     ↓
     Structured Input + Execution Plan
`


**🧩 LangGraph Design (Phase 1)**
Nodes we will build:
1. Input Parser Node
Converts NL → structured JSON
2. Planner Node
Converts structured JSON → execution plan
3. Validator Node
Ensures schema correctness







**User input layer**

Natural language filters, custom validation instructions, env (prod/preprod)

**LangGraph orchestrator**
State machine — routes tasks: parse filters → fetch UI → fetch DB → compare → report
Maintains agent state, retries, error handling across steps

**Filter parser agent**
LLM parses NL input
→ structured filter JSON

**UI data agent**
Playwright scrapes MSTR
report with filters applied

**Backend DB agent**
Snowflake SQL query
using parsed filters

**Comparator agent**
Diff UI data vs DB data — row count, value, null checks
Handles prod vs preprod comparison mode

**Validation reporter agent**
LLM-generated summary — pass/fail, mismatches, insights

**Output layer**
Validation report (HTML/JSON/CLI) · Slack/email notification · Audit log

**Data sources**
MicroStrategy UI (Playwright) · Snowflake

**Config / memory**
Filter templates · LangGraph checkpointer








ANTHROPIC_API_KEY=your_key_here

# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema

# MicroStrategy
MSTR_BASE_URL=https://mstr-instance.com
MSTR_USERNAME=your_username
MSTR_PASSWORD=your_password
MSTR_PROJECT_ID=your_project_id


Extend the existing LangGraph + Streamlit + Playwright system with:

Local demo database
SQL generation agent
DB execution node
UI vs DB comparison node
Test result generation (PASS / FAIL)
Full execution visibility in Streamlit


User
 ↓
Streamlit UI
 ↓
LangGraph Orchestrator
 ├── input_node
 ├── validator_node
 ├── planner_node
 ├── ui_node
 ├── sql_generation_node
 ├── db_query_node
 ├── comparison_node
 ├── audit_node
 └── report_node
 ↓
SQLite (Execution History + Metrics)
 ↓
Validation Report






ValidateAI/
├── Makefile
├── pyproject.toml
├── .env
├── streamlit_app.py
│
├── src/
│   ├── agents/
│   │   ├── graph/
│   │   │   ├── nodes/
│   │   │   │   ├── input_node.py
│   │   │   │   ├── validator_node.py
│   │   │   │   ├── planner_node.py
│   │   │   │   ├── ui_node.py
│   │   │   │   ├── sql_generation_node.py
│   │   │   │   ├── db_query_node.py
│   │   │   │   ├── comparison_node.py
│   │   │   │   ├── audit_node.py
│   │   │   │   └── report_node.py
│   │   │   │
│   │   │   └── graph_builder.py
│   │   │
│   │   └── graph_provider.py
│   │
│   ├── config/
│   │   ├── llm_settings.py
│   │   ├── tableau_settings.py
│   │   └── db_settings.py
│   │
│   ├── db/
│   │   ├── connection.py
│   │   ├── models.py
│   │   ├── seed.py
│   │   └── repositories/
│   │       └── audit_repository.py
│   │
│   ├── llm/
│   │   ├── llm_provider.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── input_schema.py
│   │   ├── plan_schema.py
│   │   ├── sql_schema.py
│   │   ├── comparison_schema.py
│   │   ├── report_schema.py
│   │   └── state_schema.py
│   │
│   ├── tools/
│   │   ├── tableau_scraper.py
│   │   └── sql_executor.py
│   │
│   └── utils/
│       ├── logger.py
│       └── helpers.py
│
└── logs/




# ValidateAI — Comparison Strategies Guide

## Overview

In ValidateAI, a comparison strategy defines:

```text
What exactly should be validated between UI data and backend data?
```

Different dashboard types require different comparison approaches.

For example:

* Analytical tables → row-level validation
* KPI cards → aggregate validation
* Historical dashboards → snapshot validation
* Statistical dashboards → distribution validation

---

# Comparison Strategy Types

---

# 1. Row-Level Comparison

## Definition

Compare:

```text
UI row ↔ DB row
```

using deterministic matching keys.

---

## Example

| Player | UI Value | DB Value |
| ------ | -------- | -------- |
| oSee   | 1.04     | 1.04     |

---

## Matching Keys

Typical matching keys:

* player_name
* team
* role
* country

---

## Metric Comparison

Example:

```python
ui_row["t_target_last12"] == db_row["t_target_last12"]
```

---

## Pros

* Highly accurate
* Easy debugging
* Excellent auditability
* Best for analytical dashboards

---

## Cons

* Sensitive to floating-point differences
* Sensitive to sorting/filter mismatches

---

## Best Use Cases

* Tableau tables
* MicroStrategy reports
* Power BI tables
* Entity-based analytical dashboards

---

# 2. Aggregate Comparison

## Definition

Compare aggregated values.

Example:

```text
SUM(UI values) ↔ SUM(DB values)
```

---

## Example

| Source | Total Revenue |
| ------ | ------------- |
| UI     | 1,000,000     |
| DB     | 1,000,001     |

---

## Example Logic

```python
sum(ui_values) == sum(db_values)
```

---

## Pros

* Scalable
* Fast
* Good for KPI dashboards

---

## Cons

* Hides row-level issues
* Can pass despite incorrect rows

---

## Best Use Cases

* KPI cards
* Summary dashboards
* Executive reports
* Aggregated business metrics

---

# 3. Tolerance Comparison

## Definition

Allow acceptable numeric variation.

Example:

```python
abs(ui_value - db_value) <= tolerance
```

---

## Example

| UI   | DB   | Tolerance | Result |
| ---- | ---- | --------- | ------ |
| 1.01 | 1.02 | 0.05      | PASS   |

---

## Pros

* Handles float precision issues
* Enterprise-standard approach
* Realistic for BI dashboards

---

## Cons

* Incorrect tolerance values can hide defects

---

## Best Use Cases

* Numeric dashboard validation
* Floating-point KPIs
* Statistical dashboards

---

## Important Note

Tolerance is usually combined with:

```text
row_level + tolerance
```

rather than being used independently.

---

# 4. Snapshot Comparison

## Definition

Compare current dashboard output against historical snapshots.

Example:

```text
Today's dashboard ↔ Yesterday's dashboard
```

---

## Pros

* Detects unexpected dashboard changes
* Useful for regression testing
* Useful in CI/CD pipelines

---

## Cons

* Requires historical storage
* Real business changes can trigger failures

---

## Best Use Cases

* Deployment validation
* Regression testing
* Dashboard drift detection

---

# 5. Schema Validation

## Definition

Validate dashboard structure instead of data values.

Checks:

* column names
* column order
* headers
* data types

---

## Example

```text
Dashboard contains:
- Role
- Team
- Country
```

---

## Pros

* Detects UI structural regressions
* Fast validation

---

## Cons

* Does not validate data correctness

---

## Best Use Cases

* UI regression testing
* Layout validation
* Dashboard structural integrity

---

# 6. Count Validation

## Definition

Compare only row counts.

Example:

```python
len(ui_rows) == len(db_rows)
```

---

## Pros

* Very simple
* Very fast
* Good smoke-test layer

---

## Cons

* Weak validation strategy
* Does not validate actual values

---

## Best Use Cases

* Smoke tests
* Initial sanity checks
* Pipeline health checks

---

# 7. Distribution Validation

## Definition

Compare statistical distribution patterns.

Example:

| Role  | UI Count | DB Count |
| ----- | -------- | -------- |
| AWPer | 10       | 10       |

---

## Pros

* Detects aggregation anomalies
* Useful for analytics dashboards

---

## Cons

* Not row-accurate
* Limited debugging detail

---

## Best Use Cases

* Statistical dashboards
* Trend analytics
* Segmentation dashboards

---

# 8. Trend Validation

## Definition

Validate trends over time.

Example:

```text
7-day KPI trend validation
```

---

## Pros

* Good for time-series analytics
* Detects abnormal KPI movement

---

## Cons

* Requires historical data
* More complex comparison logic

---

## Best Use Cases

* Forecasting dashboards
* Analytics dashboards
* Monitoring systems

---

# 9. Ranking Validation

## Definition

Validate ordering and ranking.

Example:

```text
Top 10 players
Top products
Top regions
```

---

## Example Logic

```python
ui_rank == db_rank
```

---

## Pros

* Useful for leaderboard dashboards
* Useful for ranking analytics

---

## Cons

* Sensitive to ties and sorting rules

---

## Best Use Cases

* Leaderboards
* Top-N reports
* Ranking dashboards

---

# 10. Visual Validation

## Definition

Validate screenshots visually.

Techniques:

* OCR
* image similarity
* computer vision

---

## Pros

* Detects rendering issues
* Detects UI visual problems

---

## Cons

* Expensive
* Flaky
* Hard to maintain

---

## Best Use Cases

* UI rendering validation
* Pixel-level regression testing
* Dashboard visual consistency

---

# Recommended Strategy for ValidateAI

---

# Current Recommendation

## Use:

```text
row_level + tolerance
```

---

## Why?

Your dashboard is:

```text
Entity-centric analytical dashboard
```

with:

* rows
* filters
* metrics
* KPIs
* player-level analytics

This makes deterministic row-level validation the best approach.

---

# Recommended Matching Keys

```json
[
  "player_name",
  "team",
  "role",
  "country"
]
```

---

# Recommended Metric Validation

```python
abs(ui_value - db_value) <= tolerance
```

---

# Recommended Configuration

```json
{
  "comparison_type": "row_level",
  "tolerance": 0.05,
  "match_keys": [
    "player_name",
    "team",
    "role"
  ]
}
```

---

# Suggested ValidateAI Roadmap

| Phase    | Strategy              |
| -------- | --------------------- |
| Current  | row_level + tolerance |
| Next     | aggregate             |
| Advanced | snapshot              |
| Future   | visual validation     |

---

# Enterprise Best Practices

## Recommended

* Deterministic comparison logic
* Python-based validation rules
* Tolerance-aware comparisons
* Structured audit logging
* Explainable failures
* Reproducible validations

---

## Avoid

* Pure screenshot comparison
* Exact float equality
* Fully autonomous LLM validation
* Business logic hidden inside prompts

---

# Final Recommendation

For ValidateAI:

```text
LLM should understand intent.
Python should perform deterministic validation.
```

This architecture provides:

* stability
* observability
