from dotenv import load_dotenv
from mcp_server.client import call_tool

import json
import os


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

LOCAL_MODE = os.getenv("LOCAL_MODE", "false").lower() == "true"


# =========================================================
# LOCAL REVISION PLAN GENERATOR
# =========================================================

def create_local_revision_plan(
    weak_topics,
    available_time
):
    """
    Create a deterministic revision plan locally.

    Topics with lower scores receive more attention.
    """

    # Convert available time into a simple number of days
    try:
        days = int(
            str(available_time)
            .split()[0]
        )
    except (ValueError, IndexError):
        days = 7

    if days <= 0:
        days = 7

    # Sort topics from weakest to strongest
    sorted_topics = sorted(
        weak_topics,
        key=lambda item: float(
            item.get("average_score", 100)
        )
    )

    plan_lines = []

    plan_lines.append(
        f"Personalized Revision Plan ({days} days)"
    )

    plan_lines.append(
        ""
    )

    plan_lines.append(
        "Focus areas:"
    )

    for item in sorted_topics:

        topic = item.get(
            "topic",
            "Unknown topic"
        )

        score = item.get(
            "average_score",
            0
        )

        attempts = item.get(
            "attempts",
            0
        )

        plan_lines.append(
            f"- {topic}: {score}% average "
            f"({attempts} attempts)"
        )

    plan_lines.append(
        ""
    )

    # =====================================================
    # DAY-BY-DAY PLAN
    # =====================================================

    for day in range(1, days + 1):

        # Rotate through weak topics
        topic_index = (day - 1) % len(
            sorted_topics
        )

        topic = sorted_topics[
            topic_index
        ].get(
            "topic",
            "weak topic"
        )

        score = float(
            sorted_topics[
                topic_index
            ].get(
                "average_score",
                0
            )
        )

        plan_lines.append(
            f"Day {day}: {topic}"
        )

        if score < 50:

            plan_lines.append(
                "  - Review the basic concepts."
            )

            plan_lines.append(
                "  - Study examples and important points."
            )

            plan_lines.append(
                "  - Practice questions on this topic."
            )

            plan_lines.append(
                "  - Take a short quiz to check understanding."
            )

        elif score < 70:

            plan_lines.append(
                "  - Review the concepts you previously found difficult."
            )

            plan_lines.append(
                "  - Practice application-based questions."
            )

            plan_lines.append(
                "  - Take a short quiz and review mistakes."
            )

        else:

            plan_lines.append(
                "  - Quickly revise the main concepts."
            )

            plan_lines.append(
                "  - Practice a few questions."
            )

            plan_lines.append(
                "  - Review any mistakes from previous quizzes."
            )

        plan_lines.append(
            ""
        )

    # =====================================================
    # FINAL REVISION
    # =====================================================

    plan_lines.append(
        "Final Review:"
    )

    plan_lines.append(
        "- Review all weak topics."
    )

    plan_lines.append(
        "- Revisit questions answered incorrectly."
    )

    plan_lines.append(
        "- Take a final mixed quiz."
    )

    plan_lines.append(
        "- Focus on improving the lowest-scoring topic."
    )

    return "\n".join(
        plan_lines
    )


# =========================================================
# REVISION PLANNER AGENT
# =========================================================

def revision_planner_agent(
    student_id: str,
    available_time: str = "7 days"
):
    """
    Revision Planner Agent.

    Gets the student's weak topics through the
    custom MCP server and creates a personalized
    revision plan.

    LOCAL_MODE=true:
        Uses deterministic local planning.

    LOCAL_MODE=false:
        Gemini can be used later for richer plans.
    """

    # =====================================================
    # STEP 1 — GET WEAK TOPICS THROUGH MCP
    # =====================================================

    mcp_result = call_tool(
        "weak_topics",
        {
            "student_id": student_id,
            "limit": 5
        }
    )

    # =====================================================
    # CHECK MCP RESULT
    # =====================================================

    if mcp_result.is_error:

        raise RuntimeError(
            "MCP weak_topics tool failed."
        )

    # =====================================================
    # PARSE MCP RESPONSE
    # =====================================================

    weak_topics = []

    for content_item in mcp_result.content:

        if hasattr(
            content_item,
            "text"
        ):

            try:

                data = json.loads(
                    content_item.text
                )

                if isinstance(
                    data,
                    list
                ):

                    weak_topics.extend(
                        data
                    )

                elif isinstance(
                    data,
                    dict
                ):

                    weak_topics.append(
                        data
                    )

            except json.JSONDecodeError:

                continue

    # =====================================================
    # NO QUIZ HISTORY
    # =====================================================

    if not weak_topics:

        return {
            "weak_topics": [],
            "revision_plan": (
                "No quiz history is available yet. "
                "Complete some quizzes first so the "
                "tutor can create a personalized "
                "revision plan."
            )
        }

    # =====================================================
    # LOCAL MODE
    # =====================================================

    if LOCAL_MODE:

        revision_plan = create_local_revision_plan(
            weak_topics=weak_topics,
            available_time=available_time
        )

        return {
            "weak_topics": weak_topics,
            "revision_plan": revision_plan
        }

    # =====================================================
    # GEMINI MODE
    # =====================================================

    from langchain_google_genai import (
        ChatGoogleGenerativeAI
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0
    )

    weak_topic_text = "\n".join(
        [
            (
                f"- {item['topic']}: "
                f"{item['average_score']}% average "
                f"({item['attempts']} attempts)"
            )
            for item in weak_topics
        ]
    )

    prompt = f"""
You are the Revision Planner Agent of an
Adaptive Study Tutor.

Create a personalized study revision plan.

Student available time:
{available_time}

Student's weak topics:
{weak_topic_text}

Requirements:

1. Prioritize topics with lower scores.
2. Allocate more study time to weaker topics.
3. Include revision and practice.
4. Include quiz practice.
5. Make the plan realistic.
6. Use a clear day-by-day or session-by-session structure.
7. Do not invent academic topics that are not in
   the weak-topic list.
8. Focus on helping the student improve weak areas.
9. Keep the plan simple and easy for a student to follow.

Return only the study plan.
"""

    response = llm.invoke(
        prompt
    )

    content = response.content

    if isinstance(
        content,
        list
    ):

        text_parts = []

        for item in content:

            if isinstance(
                item,
                dict
            ):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get(
                            "text",
                            ""
                        )
                    )

            elif isinstance(
                item,
                str
            ):

                text_parts.append(
                    item
                )

        content = "\n".join(
            text_parts
        )

    return {
        "weak_topics": weak_topics,
        "revision_plan": content
    }