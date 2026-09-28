from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from tools.tavily_tool import web_search
from tools.date_tool import get_current_date

load_dotenv()


# ------------------------------------------------------------
# Gemini model
# ------------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


# ------------------------------------------------------------
# Tools
# ------------------------------------------------------------

tools = [
    web_search,
    get_current_date
]


# ------------------------------------------------------------
# Create ReAct Agent
# ------------------------------------------------------------

react_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a helpful educational research assistant.

Your job is to answer the student's question accurately.

Available tools:

1. web_search
   Use this when supplementary web information,
   examples, articles, or educational resources
   are needed.

2. get_current_date
   Use this when the question depends on today's date.

Rules:

- Do not use tools unnecessarily.
- Give clear educational answers.
- Do not invent information.
- If web information is used, base the answer
  on the retrieved information.
"""
)


# ------------------------------------------------------------
# Run ReAct Tutor
# ------------------------------------------------------------

def react_tutor_agent(
    question: str,
    max_iterations: int = 3
):
    """
    Run the ReAct tutor with a maximum number
    of reasoning/tool iterations.
    """

    result = react_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config={
            "recursion_limit": max_iterations * 2 + 1
        }
    )

    messages = result.get(
        "messages",
        []
    )

    # Count tool calls
    tool_iterations = 0

    for message in messages:

        tool_calls = getattr(
            message,
            "tool_calls",
            None
        )

        if tool_calls:
            tool_iterations += len(
                tool_calls
            )

    # Find final AI response
    final_message = None

    for message in reversed(messages):

        if getattr(
            message,
            "type",
            ""
        ) == "ai":

            final_message = message
            break

    if final_message is None:

        return {
            "answer": "No answer was generated.",
            "iterations": tool_iterations
        }

    content = final_message.content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

            elif isinstance(item, str):

                text_parts.append(item)

        content = "\n".join(
            text_parts
        )

    return {
        "answer": content,
        "iterations": tool_iterations
    }


# ------------------------------------------------------------
# Test
# ------------------------------------------------------------

if __name__ == "__main__":

    print(
        "\nTesting ReAct Tutor Agent...\n"
    )

    result = react_tutor_agent(
        question=(
            "Find one real-world example of "
            "Newton's third law."
        ),
        max_iterations=3
    )

    print("ANSWER")
    print("=" * 60)

    print(result["answer"])

    print("\nTOOL ITERATIONS")
    print("=" * 60)

    print(result["iterations"])