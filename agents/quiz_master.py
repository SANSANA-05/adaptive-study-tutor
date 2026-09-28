from mcp_server.client import call_tool
import json


def quiz_master_agent(
    topic: str,
    num_questions: int = 5,
    difficulty: str = "medium",
    attempt: int = 0
):
    """
    Quiz Master Agent.

    Generates a quiz using the custom MCP
    generate_quiz tool.

    attempt = 0
        First quiz.

    attempt > 0
        Adaptive quiz with different questions.
    """

    result = call_tool(
        "quiz_generator",
        {
            "topic": topic,
            "num_questions": num_questions,
            "difficulty": difficulty,
            "attempt": attempt
        }
    )

    if result.is_error:

        raise RuntimeError(
            "MCP quiz_generator tool failed."
        )

    for content_item in result.content:

        if hasattr(
            content_item,
            "text"
        ):

            try:

                data = json.loads(
                    content_item.text
                )

                return data.get(
                    "questions",
                    []
                )

            except json.JSONDecodeError:

                continue

    return []