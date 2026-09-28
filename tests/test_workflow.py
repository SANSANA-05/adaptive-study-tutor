import sys
from pathlib import Path

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Import the compiled LangGraph workflow
# ---------------------------------------------------------

from graph.workflow import study_tutor_workflow


# ---------------------------------------------------------
# Initial test state
# ---------------------------------------------------------

initial_state = {
    "student_id": "adaptive_test",
    "user_query": "Quiz me on Newton's third law",
    "action": "quiz",
    "topic": "Newton's third law",

    # Empty initially — Quiz Master will generate the quiz
    "quiz": [],

    # No answers initially
    "student_answers": [],

    # Adaptive learning settings
    "iteration": 0,
    "max_iterations": 3,
    "mastery_threshold": 70.0,

    # Web search tracking
    "used_web_search": False,
}


# ---------------------------------------------------------
# Run the workflow
# ---------------------------------------------------------

print("=" * 60)
print("ADAPTIVE STUDY TUTOR - WORKFLOW TEST")
print("=" * 60)

print("\nStarting workflow...")
print("Student ID:", initial_state["student_id"])
print("Query:", initial_state["user_query"])
print("Topic:", initial_state["topic"])

print("\nRunning LangGraph workflow...\n")


result = study_tutor_workflow.invoke(initial_state)


# ---------------------------------------------------------
# Display final result
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("WORKFLOW COMPLETED")
print("=" * 60)


print("\nFinal response:")
print("-" * 60)

print(result.get("final_response", "No final response generated."))


# ---------------------------------------------------------
# Display important workflow information
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("WORKFLOW RESULT DETAILS")
print("=" * 60)

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
# Display quiz if generated
# ---------------------------------------------------------

quiz = result.get("quiz", [])

if quiz:
    print("\n" + "=" * 60)
    print("GENERATED QUIZ")
    print("=" * 60)

    for index, question in enumerate(quiz, start=1):
        print(f"\nQuestion {index}:")

        if isinstance(question, dict):
            print(question.get("question", question))
        else:
            print(question)


# ---------------------------------------------------------
# Display citations if available
# ---------------------------------------------------------

citations = result.get("citations", [])

if citations:
    print("\n" + "=" * 60)
    print("CITATIONS")
    print("=" * 60)

    for citation in citations:
        print("-", citation)


# ---------------------------------------------------------
# Display weak topics if available
# ---------------------------------------------------------

weak_topics = result.get("weak_topics", [])

if weak_topics:
    print("\n" + "=" * 60)
    print("WEAK TOPICS")
    print("=" * 60)

    for topic in weak_topics:
        print("-", topic)


# ---------------------------------------------------------
# Final status
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("TEST FINISHED SUCCESSFULLY")
print("=" * 60)