from mcp.server.mcpserver import MCPServer

from quiz_tools import generate_quiz
from progress_tools import save_progress, get_weak_topics


# ---------------------------------------------------------
# CREATE MCP SERVER
# ---------------------------------------------------------

mcp = MCPServer("Adaptive Study Tutor")


# ---------------------------------------------------------
# TOOL 1: GENERATE QUIZ
# ---------------------------------------------------------

@mcp.tool()
def quiz_generator(
    topic: str,
    num_questions: int = 5,
    difficulty: str = "medium",
    attempt: int = 0
):
    """
    Generate multiple-choice quiz questions for a topic.

    attempt = 0
        First quiz.

    attempt > 0
        Adaptive quiz using different questions.
    """

    return generate_quiz(
        topic=topic,
        num_questions=num_questions,
        difficulty=difficulty,
        attempt=attempt
    )


# ---------------------------------------------------------
# TOOL 2: SAVE PROGRESS
# ---------------------------------------------------------

@mcp.tool()
def save_student_progress(
    student_id: str,
    topic: str,
    score: float,
    total_questions: int,
    difficulty: str = "medium"
):
    """
    Save a student's quiz progress.
    """

    return save_progress(
        student_id=student_id,
        topic=topic,
        score=score,
        total_questions=total_questions,
        difficulty=difficulty
    )


# ---------------------------------------------------------
# TOOL 3: GET WEAK TOPICS
# ---------------------------------------------------------

@mcp.tool()
def weak_topics(
    student_id: str,
    limit: int = 3
):
    """
    Get the student's lowest-scoring topics.
    """

    return get_weak_topics(
        student_id=student_id,
        limit=limit
    )


# ---------------------------------------------------------
# START MCP SERVER
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()