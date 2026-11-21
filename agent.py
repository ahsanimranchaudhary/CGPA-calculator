import asyncio
import os
from functools import wraps
from dotenv import load_dotenv

from llm import llm
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.mcp import MCPAdapter
from fastmcp.client import Client
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

load_dotenv()

SYSTEM_PROMPT = """You are a conversational agent helping a PUCIT BS(CS) student with GPA and CGPA questions.
Strictly adhere to the following rules:

1. Every calculation or feasibility check goes through a tool. Never compute in your head.
2. NEVER invent marks, credit hours, or a CGPA. If the user states their current semester and CGPA (e.g., "I am in 7th semester with CGPA 3.71"), immediately use the `check_unreachable_target` tool. Do not ask the user for completed credit hours.
3. A required GPA above 4.0 is impossible. Do not report it as an actionable solution.
4. Offer to save a report ONLY after producing a valid horizon check or calculation. Never save without being asked.
5. THE UNREACHABLE TARGET RULE: When a student asks for a target CGPA, evaluate feasibility iteratively using your tools rather than guessing or stopping at the first failure:
  - Step 1: Use `required_gpa_for_target` to check the required GPA for just their immediate next single semester.
  - Step 2: If that required GPA is greater than 4.0, recognize that it is impossible. Do not stop.
  - Step 3: Widen the horizon by calling `required_gpa_for_target` again across the current semester plus the following semester combined.
  - Step 4: Keep widening the window one semester at a time until the calculated required GPA falls at or below 4.0.
  - Step 5: Present the step-by-step check to the student (showing the impossible horizons first) and clearly state which final horizon successfully works.
6. If a tool reports that the MCP server is unreachable or down, politely inform the student that the calculation server is currently unavailable instead of guessing.
"""


# --- TASK 6: Prevent server-down crashes from corrupting SQLite memory ---
def make_tool_safe(tool):
    """Wrap an async MCP tool so network/server errors return a message to the LLM instead of crashing."""
    orig_coro = tool.coroutine
    if orig_coro is None:
        return tool

    @wraps(orig_coro)
    async def safe_coro(*args, **kwargs):
        try:
            return await orig_coro(*args, **kwargs)
        except Exception as e:
            return (
                f"ERROR: Could not reach the MCP tool server ({type(e).__name__}: {e}). "
                "Tell the user that the calculation server is currently offline and try again later."
            )

    tool.coroutine = safe_coro
    return tool


# --- TASK 3: Memory helper functions ---
async def list_threads(memory: AsyncSqliteSaver) -> list[str]:
    """Return a sorted list of all saved thread_ids in SQLite."""
    threads = set()
    async for checkpoint in memory.alist(None):
        tid = checkpoint.config.get("configurable", {}).get("thread_id")
        if tid:
            threads.add(tid)
    return sorted(threads)


async def show_history(app, config: dict):
    """Print the saved conversation history for the current thread."""
    state = await app.aget_state(config)
    messages = state.values.get("messages", [])
    if not messages:
        print("\n[No saved history for this user yet.]\n")
        return

    print("\n--- Conversation History ---")
    for msg in messages:
        role = msg.type.upper()
        if msg.content:
            print(f"[{role}]: {msg.content}")
        elif hasattr(msg, "tool_calls") and msg.tool_calls:
            names = [tc["name"] for tc in msg.tool_calls]
            print(f"[{role}]: (called tools: {', '.join(names)})")
    print("----------------------------\n")


async def main():
    mcp_url = os.getenv("MCP_URL", "http://127.0.0.1:8000/mcp")
    mcp_key = os.getenv("FASTMCP_KEY", "").strip()

    # TASK 2 & 5: Connect to local or hosted MCP server (with auth if key is provided)
    target = Client(mcp_url, auth=mcp_key) if mcp_key else mcp_url

    async with MCPAdapter(target) as adapter:
        raw_tools = await adapter.list_tools()
        tools = [make_tool_safe(t) for t in raw_tools]

        # TASK 3: Persistent SQLite checkpointer
        async with AsyncSqliteSaver.from_conn_string("chat_history.sqlite") as memory:
            app = create_agent(
                model=llm,
                tools=tools,
                system_prompt=SYSTEM_PROMPT,
                checkpointer=memory,
            )

            print("GPA ASSISTANT is ready!")
            print("Commands: /switch, /history, /forget, or 'quit'/'exit'\n")

            saved = await list_threads(memory)
            print("Saved chats:", saved if saved else "None yet")

            name = input("Who is chatting? ").strip() or "default"
            config = {"configurable": {"thread_id": name}}
            print(f"Switched to chat: {name}\n")

            while True:
                user_input = input(f"{name}: ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit"]:
                    break

                # --- TASK 3: Slash commands ---
                if user_input == "/switch":
                    saved = await list_threads(memory)
                    print("Saved chats:", saved if saved else "None yet")
                    name = input("Switch to who? ").strip() or "default"
                    config = {"configurable": {"thread_id": name}}
                    print(f"Switched to chat: {name}\n")
                    continue

                if user_input == "/history":
                    await show_history(app, config)
                    continue

                if user_input == "/forget":
                    await memory.adelete_thread(name)
                    print(f"Forgot all history for '{name}'.\n")
                    continue

                # --- TASK 4: Streaming (updates + messages, v2) ---
                inputs = {"messages": [HumanMessage(content=user_input)]}
                print("Bot: ", end="", flush=True)
                try:
                    async for chunk in app.astream(
                        inputs,
                        config,
                        stream_mode=["updates", "messages"],
                        version="v2",
                    ):
                        if chunk["type"] == "messages":
                            token, metadata = chunk["data"]
                            node = metadata.get("langgraph_node", "")
                            # Stream only model text tokens (skip tool output messages)
                            if node == "model" and getattr(token, "content", None):
                                print(token.content, end="", flush=True)
                        else:
                            # "updates": show when tools are called/finished
                            for node, update in chunk["data"].items():
                                if node == "tools":
                                    print("\n[Tools finished]", flush=True)
                                    print("Bot: ", end="", flush=True)
                    print("\n")
                except Exception as e:
                    print(f"\nError: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())