# ValidateAI


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


import subprocess

subprocess.run(["playwright", "install-deps", "chromium"])


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
