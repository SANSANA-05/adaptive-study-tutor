import sqlite3
from pathlib import Path


# ---------------------------------------------------------
# DATABASE LOCATION
# ---------------------------------------------------------

DATABASE_PATH = Path("database/progress.db")


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

def get_connection():
    """Create a connection to the SQLite database."""

    return sqlite3.connect(DATABASE_PATH)


# ---------------------------------------------------------
# TOOL 1: SAVE PROGRESS
# ---------------------------------------------------------

def save_progress(
    student_id: str,
    topic: str,
    score: float,
    total_questions: int,
    difficulty: str = "medium"
):
    """
    Save a student's quiz result.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO progress (
            student_id,
            topic,
            score,
            total_questions,
            difficulty
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            student_id,
            topic,
            score,
            total_questions,
            difficulty
        )
    )

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Progress saved successfully.",
        "student_id": student_id,
        "topic": topic,
        "score": score,
        "total_questions": total_questions,
        "difficulty": difficulty
    }


# ---------------------------------------------------------
# TOOL 2: GET WEAK TOPICS
# ---------------------------------------------------------

def get_weak_topics(
    student_id: str,
    limit: int = 3
):
    """
    Return the topics with the lowest average quiz scores.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            topic,
            AVG(score * 1.0 / total_questions) AS average_score,
            COUNT(*) AS attempts
        FROM progress
        WHERE student_id = ?
        GROUP BY topic
        ORDER BY average_score ASC
        LIMIT ?
        """,
        (student_id, limit)
    )

    rows = cursor.fetchall()

    connection.close()

    weak_topics = []

    for row in rows:

        topic = row[0]
        average_score = row[1]
        attempts = row[2]

        weak_topics.append({
            "topic": topic,
            "average_score": round(average_score * 100, 2),
            "attempts": attempts
        })

    return weak_topics


# ---------------------------------------------------------
# TEST THE TOOLS
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nTesting save_progress...\n")

    result = save_progress(
        student_id="student_001",
        topic="Newton's Laws of Motion",
        score=2,
        total_questions=5,
        difficulty="easy"
    )

    print(result)

    print("\nTesting get_weak_topics...\n")

    weak_topics = get_weak_topics(
        student_id="student_001"
    )

    print(weak_topics)