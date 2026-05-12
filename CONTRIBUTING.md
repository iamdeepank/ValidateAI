# Contributing to ValidateAI

Thank you for contributing to ValidateAI.

ValidateAI is an Agentic AI platform for dashboard validation, UI-data reconciliation, and automated data quality verification using:

- LangGraph
- LangChain
- Groq
- Playwright
- Streamlit
- database

This document explains the development workflow, coding standards, testing expectations, and contribution process.

---

# Development Philosophy

This project follows a few important engineering principles:

- typed state management
- observable agent execution
- isolated graph nodes
- structured outputs over free-form text
- reproducible testing
- minimal hidden side effects

We prioritize:
- maintainability
- debuggability
- reliability
- testability

over:
- rapid hacks
- prompt-heavy logic
- dynamic runtime code generation

---

# Project Structure

```text
src/
├── agents/
├── config/
├── db/
├── endpoints/
├── llm/
├── schemas/
├── tools/
├── utils/
├── tests/

```