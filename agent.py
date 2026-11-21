from llm import llm
from tools import pucit_tools
from langchain.agents import create_agent
from langchain.messages import HumanMessage

SYSTEM_PROMPT = """You are a conversational agent helping a PUCIT BS(CS) student with GPA and CGPA questions.
Strictly adhere to the following rules:

1. Every calculation or feasibility check goes through a tool. Never compute in your head.
2. NEVER invent marks, credit hours, or a CGPA. If the user states their current semester and CGPA (e.g., "I am in 7th semester with CGPA 3.71"), immediately use the `check_unreachable_target` tool. Do not ask the user for completed credit hours.
3. A required GPA above 4.0 is impossible. Do not report it as an actionable solution.
4. Offer to save a report ONLY after producing a valid horizon check or calculation. Never save without being asked.
5. A required GPA above 4.0 is impossible. Do not report it as if it were an answer.
6. Offer to save a report only after producing something worth keeping. Do not offer after a clarifying question, and never save without being asked.
7. THE UNREACHABLE TARGET RULE: When a student asks for a target CGPA, you must evaluate the feasibility iteratively using your tools rather than guessing or stopping at the first failure. Follow this exact procedure:
   - Step 1: Use `required_gpa_for_target` to check the required GPA for just their immediate next single semester.
   - Step 2: If that required GPA is greater than 4.0, recognize that it is impossible. Do not stop. 
   - Step 3: Widen the horizon by calling `required_gpa_for_target` again across the current semester plus the following semester combined (increasing the remaining credit hours window).
   - Step 4: Keep widening the window one semester at a time until the calculated required GPA falls at or below 4.0.
   - Step 5: Present the step-by-step check to the student (showing the impossible horizons first) and clearly state which final horizon successfully works.
"""
agent = create_agent(
    model=llm, 
    tools=pucit_tools, 
    system_prompt=SYSTEM_PROMPT
)

print("GPA ASSISTANT is ready! type 'quit' or 'exit' to stop.\n")

messages = []

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit"]:
        break
        
    try:
        messages.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": messages})
        bot_response = result["messages"][-1].content
        print(f"Bot: {bot_response}\n")
        messages = result["messages"]
        
    except Exception as e:
        print(f"Error: {e}")
        break