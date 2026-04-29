# ValidateAI

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
MSTR_BASE_URL=https://your-mstr-instance.com
MSTR_USERNAME=your_username
MSTR_PASSWORD=your_password
MSTR_PROJECT_ID=your_project_id

# Optional
SLACK_WEBHOOK_URL=https://hooks.slack.com/...



mstr_validator/
├── main.py                  # Entry point — run validation from CLI
├── requirements.txt
├── .env.example
├── config/
│   └── settings.py          # Centralised config & env loading
├── agents/
│   ├── filter_parser.py     # NL → structured filter JSON agent
│   ├── ui_data_agent.py     # Playwright MSTR scraper agent
│   ├── db_agent.py          # Snowflake query agent
│   ├── comparator.py        # Diff / validation logic agent
│   └── reporter.py          # LLM-generated report agent
├── tools/
│   ├── playwright_tool.py   # LangChain tool wrapper for Playwright
│   └── snowflake_tool.py    # LangChain tool wrapper for Snowflake
├── graph/
│   └── workflow.py          # LangGraph state machine definition
├── reports/                 # Output HTML/JSON reports saved here
└── tests/
    └── test_comparator.py   # Unit tests