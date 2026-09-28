import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.workflow import study_tutor_workflow


print("=" * 70)
print("ADAPTIVE STUDY TUTOR - ADAPTIVE WORKFLOW TEST")
print("=" * 70)

# ---------------------------------------------------------
# Initial student state
# ---------------------------------------------------------

initial_state = {
    "student_id": "adaptive_student_001",
    "user_query": "Quiz me on Newton's third law",
    "action": "quiz",
    "topic": "Newton's third law",

    # Quiz state
    "quiz": [],

    # Deliberately leave answers empty.
    # This first test checks the workflow structure.
    "student_answers": [],

    # Adaptive learning settings
    "iteration": 0,
    "max_iterations": 3,
    "mastery_threshold": 70.0,

    # Web search state
    "used_web_search": False,
}


print("\nStudent ID:")
print(initial_state["student_id"])

print("\nTopic:")
print(initial_state["topic"])

print("\nMastery threshold:")
print(initial_state["mastery_threshold"], "%")

print("\nMaximum iterations:")
print(initial_state["max_iterations"])

print("\nStarting adaptive workflow...\n")


# ---------------------------------------------------------
# Run LangGraph
# ---------------------------------------------------------

result = study_tutor_workflow.invoke(initial_state)


# ---------------------------------------------------------
# Display result
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("ADAPTIVE WORKFLOW COMPLETED")
print("=" * 70)

print("\nAction:")
print(result.get("action"))

print("\nTopic:")
print(result.get("topic"))

print("\nIteration:")
print(result.get("iteration"))

print("\nScore:")
print(result.get("score"))

print("\nCorrect answers:")
print(result.get("correct_count"))

print("\nTotal questions:")
print(result.get("total_questions"))

print("\nMastery threshold:")
print(result.get("mastery_threshold"))

print("\nUsed web search:")
print(result.get("used_web_search"))


# ---------------------------------------------------------
# Final response
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("FINAL RESPONSE")
print("=" * 70)

print(result.get(
    "final_response",
    "No final response generated."
))


# ---------------------------------------------------------
# Quiz information
# ---------------------------------------------------------

quiz = result.get("quiz", [])

if quiz:

    print("\n" + "=" * 70)
    print("QUIZ GENERATED")
    print("=" * 70)

    for index, question in enumerate(quiz, start=1):

        print(f"\nQuestion {index}:")

        if isinstance(question, dict):

            print(
                question.get(
                    "question",
                    "No question text"
                )
            )

            print("\nOptions:")

            options = question.get("options", [])

            for option in options:
                print("-", option)

            print(
                "\nCorrect answer:",
                question.get("correct_answer")
            )

            print(
                "Explanation:",
                question.get("short_explanation")
            )

        else:

            print(question)


# ---------------------------------------------------------
# Weak topics
# ---------------------------------------------------------

weak_topics = result.get("weak_topics", [])

if weak_topics:

    print("\n" + "=" * 70)
    print("WEAK TOPICS")
    print("=" * 70)

    for topic in weak_topics:
        print("-", topic)


# ---------------------------------------------------------
# Citations
# ---------------------------------------------------------

citations = result.get("citations", [])

if citations:

    print("\n" + "=" * 70)
    print("CITATIONS")
    print("=" * 70)

    for citation in citations:
        print("-", citation)


print("\n" + "=" * 70)
print("TEST FINISHED")
print("=" * 70)