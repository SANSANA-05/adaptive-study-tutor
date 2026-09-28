import os
import re
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


LOCAL_MODE = os.getenv("LOCAL_MODE", "true").lower() == "true"


class PlannerDecision(BaseModel):
    action: str = Field(
        description="One of: explain, quiz, review, plan"
    )
    topic: str = Field(
        description="The main study topic from the user's request"
    )
    reason: str = Field(
        description="Short explanation for the planning decision"
    )


def create_gemini_llm():
    """
    Create the Gemini model used by the planner
    when LOCAL_MODE is disabled.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0
    )


def extract_topic(query: str) -> str:
    """
    Extract a cleaner topic from common user request patterns.
    """

    query = query.strip()

    patterns = [
        r"explain\s+(.+?)(?:\s+with\s+an\s+example)?[.!?]?$",
        r"teach\s+me\s+(.+?)[.!?]?$",
        r"quiz\s+me\s+on\s+(.+?)[.!?]?$",
        r"test\s+me\s+on\s+(.+?)[.!?]?$",
        r"quiz\s+me\s+about\s+(.+?)[.!?]?$",
        r"questions?\s+on\s+(.+?)[.!?]?$",
        r"questions?\s+about\s+(.+?)[.!?]?$",
        r"revise\s+(.+?)[.!?]?$",
        r"revision\s+on\s+(.+?)[.!?]?$",
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)

        if match:
            topic = match.group(1).strip()

            topic = re.sub(
                r"\s+with\s+an?\s+example$",
                "",
                topic,
                flags=re.IGNORECASE
            )

            topic = topic.strip(" .!?")

            if topic:
                return topic

    return query


def local_planner(query: str) -> PlannerDecision:
    """
    Local keyword-based planner.

    Used when LOCAL_MODE=true so the project can run
    without consuming Gemini API quota.

    Priority:
    1. Revision/study plan
    2. Quiz
    3. Review/weak topics
    4. Explain
    """

    query_lower = query.lower().strip()

    # ---------------------------------------------------------
    # 1. REVISION / STUDY PLAN
    # ---------------------------------------------------------
    # IMPORTANT:
    # This check must happen BEFORE the review/weak-topic check.
    #
    # Example:
    # "Make me a revision plan for my weak topics."
    #
    # contains both "revision plan" and "weak topics".
    # The intended action is PLAN.
    # ---------------------------------------------------------

    plan_keywords = [
        "revision plan",
        "revision schedule",
        "study plan",
        "study schedule",
        "study timetable",
        "revision timetable",
        "make a plan",
        "make me a plan",
        "create a plan",
        "create me a plan",
        "plan my study",
        "plan my revision",
        "plan for my exam",
        "study plan for",
        "revision plan for",
        "prepare a plan",
        "prepare me a plan",
        "schedule my study",
        "schedule my revision",
    ]

    if any(keyword in query_lower for keyword in plan_keywords):
        return PlannerDecision(
            action="plan",
            topic=extract_topic(query),
            reason=(
                "Local planner selected the plan action "
                "because the request asks for a revision, "
                "study plan, or schedule."
            )
        )

    # ---------------------------------------------------------
    # 2. QUIZ
    # ---------------------------------------------------------

    quiz_keywords = [
        "quiz",
        "test me",
        "give me a test",
        "give me questions",
        "ask me questions",
        "practice questions",
        "mcq",
        "multiple choice",
    ]

    if any(keyword in query_lower for keyword in quiz_keywords):
        return PlannerDecision(
            action="quiz",
            topic=extract_topic(query),
            reason=(
                "Local planner selected the quiz action "
                "because the request asks for questions "
                "or a quiz."
            )
        )

    # ---------------------------------------------------------
    # 3. REVIEW / WEAK TOPICS / PROGRESS
    # ---------------------------------------------------------

    review_keywords = [
        "weak topics",
        "weak topic",
        "weak areas",
        "weak area",
        "what am i weak in",
        "what topics am i weak in",
        "which topics am i weak in",
        "my weak topics",
        "my weak areas",
        "show my progress",
        "my progress",
        "progress report",
        "review my progress",
        "review my performance",
        "performance",
        "previous scores",
        "quiz history",
        "score history",
    ]

    if any(keyword in query_lower for keyword in review_keywords):
        return PlannerDecision(
            action="review",
            topic=extract_topic(query),
            reason=(
                "Local planner selected the review action "
                "because the request asks about weak topics, "
                "progress, performance, or quiz history."
            )
        )

    # ---------------------------------------------------------
    # 4. EXPLAIN
    # ---------------------------------------------------------

    return PlannerDecision(
        action="explain",
        topic=extract_topic(query),
        reason=(
            "Local planner selected the explain action "
            "because the request does not match quiz, "
            "review, or revision-plan keywords."
        )
    )


def gemini_planner(query: str) -> PlannerDecision:
    """
    Gemini-powered planner used when LOCAL_MODE=false.
    """

    llm = create_gemini_llm()

    structured_llm = llm.with_structured_output(
        PlannerDecision
    )

    prompt = f"""
You are the Planner Agent for an Adaptive Study Tutor.

Decide what the tutor should do based on the student's request.

Allowed actions:

1. explain
   - Explain or teach a concept.

2. quiz
   - Generate a quiz or practice questions.

3. review
   - Show weak topics, progress, previous performance,
     or quiz history.

4. plan
   - Create a revision plan, study plan, study schedule,
     or exam preparation schedule.

Important:
If a request contains both a planning phrase and a weak-topic
phrase, choose "plan" when the user is asking for a plan.

For example:
"Make me a revision plan for my weak topics."
must be classified as:
action = "plan"

Student request:
{query}

Return:
- action
- topic
- reason
"""

    result = structured_llm.invoke(prompt)

    return result


def planner_agent(query: str) -> PlannerDecision:
    """
    Main Planner Agent.

    LOCAL_MODE=true:
        Uses deterministic keyword routing.

    LOCAL_MODE=false:
        Uses Gemini structured output.
    """

    if not query or not query.strip():
        return PlannerDecision(
            action="explain",
            topic="",
            reason="Empty query received; defaulting to explain."
        )

    if LOCAL_MODE:
        return local_planner(query)

    return gemini_planner(query)


if __name__ == "__main__":

    print("\n============================================")
    print("Adaptive Study Tutor - Planner Agent")
    print("============================================")

    test_queries = [
        "Explain Newton's third law with an example.",
        "Quiz me on Newton's third law.",
        "What topics am I weak in?",
        "Show my progress.",
        "Make me a revision plan for my weak topics.",
        "Create a study schedule for my exam.",
        "Teach me Newton's second law.",
    ]

    for query in test_queries:

        decision = planner_agent(query)

        print("\nUser:")
        print(query)

        print("\nPlanner Decision:")
        print(f"Action : {decision.action}")
        print(f"Topic  : {decision.topic}")
        print(f"Reason : {decision.reason}")

    print("\n============================================")
    print("Planner test completed.")
    print("============================================")