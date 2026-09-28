import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# IMPORT PROJECT TOOLS
# =========================================================

from tools.tavily_tool import web_search
from tools.date_tool import get_current_date


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

LOCAL_MODE = (
    os.getenv(
        "LOCAL_MODE",
        "false"
    ).lower() == "true"
)


# =========================================================
# REACT TOOLS
# =========================================================

react_tools = [
    web_search,
    get_current_date
]


# =========================================================
# GEMINI REACT AGENT
# =========================================================

def create_gemini_react_agent():

    from langchain_google_genai import (
        ChatGoogleGenerativeAI
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0
    )

    return create_agent(
        model=llm,
        tools=react_tools,
        system_prompt="""
You are the Research ReAct Agent of an Adaptive Study Tutor.

Your job is to research supplementary educational
information when the textbook knowledge base does not
provide enough information.

Available tools:

1. web_search
   - Searches the web using Tavily.
   - Use it for supplementary educational information,
     examples, articles, and videos.

2. get_current_date
   - Returns the current date.
   - Use it when the user's request depends on dates.

Rules:

1. Think about whether a tool is necessary.
2. Use tools only when they are useful.
3. Prefer reliable educational information.
4. Do not invent facts.
5. Clearly distinguish supplementary web information
   from textbook information.
6. Keep explanations appropriate for students.
7. Return a concise educational response.
"""
    )


# =========================================================
# LOCAL RESEARCH MODE
# =========================================================

def run_local_research(
    user_query: str,
    max_iterations: int
):
    """
    Local-mode research path.

    Tavily is called directly because the Gemini reasoning
    model is unavailable while LOCAL_MODE=true.

    The iteration limit is still respected.
    """

    if max_iterations < 1:
        max_iterations = 1

    # -----------------------------------------------------
    # ReAct-style research step
    # -----------------------------------------------------

    search_result = web_search.invoke(
        user_query
    )

    return {
        "messages": [
            {
                "role": "assistant",
                "content": search_result
            }
        ],
        "used_web_search": True,
        "max_iterations": max_iterations,
        "mode": "local"
    }


# =========================================================
# RUN REACT AGENT
# =========================================================

def run_react_agent(
    user_query: str,
    max_iterations: int = 3
):
    """
    Run the research ReAct agent.

    LOCAL_MODE=true:
        Uses Tavily directly without Gemini.

    LOCAL_MODE=false:
        Uses the Gemini-powered ReAct agent.
    """

    if max_iterations < 1:
        max_iterations = 1

    # -----------------------------------------------------
    # LOCAL MODE
    # -----------------------------------------------------

    if LOCAL_MODE:

        return run_local_research(
            user_query=user_query,
            max_iterations=max_iterations
        )

    # -----------------------------------------------------
    # GEMINI MODE
    # -----------------------------------------------------

    react_agent = create_gemini_react_agent()

    # Controlled iteration limit
    recursion_limit = (
        max_iterations * 2
    ) + 1

    result = react_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        },
        config={
            "recursion_limit":
                recursion_limit
        }
    )

    return result


# =========================================================
# CONFIGURATION TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\nAdaptive Study Tutor - ReAct Agent"
    )

    print(
        "\nLOCAL_MODE:",
        LOCAL_MODE
    )

    print(
        "\nAvailable tools:"
    )

    for tool in react_tools:

        print(
            f"- {tool.name}"
        )

    print(
        "\nMaximum iterations: 3"
    )

    print(
        "Recursion limit: 7"
    )

    print(
        "\nReAct agent configuration test completed."
    )