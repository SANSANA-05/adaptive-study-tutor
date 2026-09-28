import sys
import json
from pathlib import Path

# ---------------------------------------------------------
# PROJECT ROOT FIX
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# MCP IMPORT
# ---------------------------------------------------------

from mcp_server.client import call_tool


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

student_id = "student_test"

print("\nGetting weak topics from MCP...\n")


result = call_tool(
    "weak_topics",
    {
        "student_id": student_id,
        "limit": 5
    }
)


# ---------------------------------------------------------
# CHECK MCP RESULT
# ---------------------------------------------------------

if result.is_error:
    raise RuntimeError(
        "MCP weak_topics tool failed."
    )


# ---------------------------------------------------------
# PARSE WEAK TOPICS
# ---------------------------------------------------------

weak_topics = []

for content_item in result.content:

    if hasattr(
        content_item,
        "text"
    ):

        try:

            data = json.loads(
                content_item.text
            )

            weak_topics.append(
                data
            )

        except json.JSONDecodeError:

            continue


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print(
    "Weak topics retrieved:\n"
)

for item in weak_topics:

    print(
        f"- {item['topic']}: "
        f"{item['average_score']}% "
        f"average score "
        f"({item['attempts']} attempts)"
    )


print(
    "\nRevision Planner input is ready."
)


print(
    "\nData that will be given to "
    "the Revision Planner:"
)


for item in weak_topics:

    print(
        f"\nTopic: {item['topic']}"
    )

    print(
        f"Average Score: "
        f"{item['average_score']}%"
    )

    print(
        f"Attempts: "
        f"{item['attempts']}"
    )


print(
    "\nMCP → Revision Planner data test successful!"
)