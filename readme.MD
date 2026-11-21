PUCIT CGPA Guider (MCP + Memory + Streaming)

An AI-powered conversational agent for PUCIT BS(CS) students that calculates semester GPAs, projects CGPAs, checks target CGPA feasibility across remaining semesters, and saves graduation reports.

Built with LangChain, Groq, FastMCP, and LangGraph SQLite Checkpointing, this project decouples all calculation tools onto a remote Model Context Protocol (MCP) server while adding persistent multi-user memory, live token streaming, and graceful downtime handling.

Deployment & Submission Details

GitHub Repository: https://github.com/ahsanimranchaudhary/CGPA-calculator

Live MCP Server URL: <PASTE_YOUR_DEPLOYED_MCP_URL_HERE> (e.g., https://your-app.horizon.prefect.io/mcp)

MCP Server API Key: <PASTE_YOUR_FASTMCP_API_KEY_HERE> (remove if your host does not require authentication)

Features

Remote MCP Tool Server (server.py): Exposes all 8 deterministic Python calculation tools over HTTP using FastMCP, making them reusable by any MCP-compatible client or framework.

Persistent Multi-User Memory (AsyncSqliteSaver): Saves conversation history per thread_id in chat_history.sqlite, so students can close the app and resume later without re-entering their details.

Live Streaming (astream): Streams model responses token-by-token (stream_mode=["updates", "messages"], version="v2") and reports tool execution updates in real time.

Resilient Server-Down Handling: Wraps async MCP tool calls so that if the MCP server goes offline mid-conversation, the agent catches the network error and returns a safe tool message instead of crashing or corrupting SQLite history.

Unreachable Target Rule: Iteratively widens the semester horizon when a target CGPA requires more than a 4.0 GPA in the immediate next semester.

Project Structure

CGPA-calculator/
├── agent.py           # Async LangChain agent with MCPAdapter, SQLite memory, streaming & error handling
├── llm.py             # Groq chat model initialization (groq:openai/gpt-oss-20b)
├── server.py          # FastMCP HTTP server exposing all tools
├── tools.py           # PUCIT BS(CS) course catalog & 8 GPA/CGPA calculation functions
├── requirements.txt   # Python dependencies
├── .env.example       # Template for environment variables
├── .gitignore         # Excludes .venv, .env, SQLite files, and PDFs
└── README.md          # Project documentation


Available MCP Tools

All 8 functions from tools.py are served via server.py:

Tool Name

Description

marks_to_grade

Converts raw marks (0–100) into PUCIT grade points (0.0–4.0).

calculate_semester_gpa

Computes a single semester's GPA weighted by credit hours.

calculate_new_cgpa

Projects updated CGPA after completing an additional semester.

required_gpa_for_target

Calculates the GPA needed over remaining credit hours to hit a target CGPA.

get_semester_courses

Returns the PUCIT BS(CS) courses and credit hours for semesters 1–8.

get_remaining_credit_hours

Computes total graded credit hours remaining until graduation.

check_unreachable_target

Iteratively checks target CGPA feasibility across widening semester horizons.

save_report

Saves a GPA calculation report or graduation plan to a text file.

Setup & Installation

1. Clone the Repository

git clone https://github.com/ahsanimranchaudhary/CGPA-calculator.git
cd CGPA-calculator


2. Create & Activate a Virtual Environment

python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate


3. Install Dependencies

pip install "langchain[mcp]" langchain-groq fastmcp langgraph-checkpoint-sqlite aiosqlite python-dotenv


4. Configure Environment Variables

Create a .env file (based on .env.example) with your keys and MCP server URL:

GROQ_API_KEY=your_groq_api_key
MCP_URL=http://127.0.0.1:8000/mcp
FASTMCP_KEY=


(To use the hosted server instead of localhost, set MCP_URL to your deployed URL and FASTMCP_KEY to your server API key if required.)

Running the Project

Option A: Test the MCP Server Standalone

List all available tools or call one directly without running the agent:

fastmcp list server.py
fastmcp call server.py get_remaining_credit_hours current_semester=5


To test the deployed online server:

fastmcp list <YOUR_DEPLOYED_MCP_URL> --auth <YOUR_API_KEY>


Option B: Run Locally (Server + Agent)

Terminal 1 — Start the MCP server:

python server.py


Terminal 2 — Start the conversational agent:

python agent.py


Chat Commands

While chatting with the agent, you can use the following built-in commands:

/switch — Switch to a different student's saved chat (thread_id).

/history — Display the saved conversation history for the active user.

/forget — Permanently delete the current user's saved thread from chat_history.sqlite.

quit or exit — Exit the application.
