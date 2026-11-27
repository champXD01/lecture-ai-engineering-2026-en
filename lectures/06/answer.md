# Lecture 06 answers

## Exercises

<!-- Paste the original [tool call] lines. Leave unfinished steps blank. -->

- Tool name in STEP 1: `glossary_get_lecture_summary`
- STEP 2 [tool call]:
- STEP 3 [tool call]:
- STEP 4 [tool call]:
- Observations and questions: The Lecture 2 summary tool was successfully called and returned the key points from Lecture 2.

## Homework

### Basic

- **Level attempted:** Basic

- **What you did:**
  - Opened `app/mcp_server.py`.
  - Registered `tools.get_lecture_summary` as an MCP tool using:
    `server.tool()(tools.get_lecture_summary)`
  - Kept the existing `tools.search_glossary` registration unchanged.

- **Results:**
  - `uv run python -m app.mcp_agent --list-tools` displayed both tools:
    - `glossary_search_glossary`
    - `glossary_get_lecture_summary`
  - `uv run python -m app.mcp_agent --trace "What do we learn in Lecture 2?"` successfully called `glossary_get_lecture_summary`.
  - The tool returned the Lecture 2 summary.
  - `uv run pytest -q` completed successfully: **21 passed in 4.60s**.

- **Observations and questions:**
  - Registering the lecture-summary function made it available to the agent through the MCP server.
  - The trace confirmed that the agent could select and use the newly registered tool.
  - All 21 tests passed.
