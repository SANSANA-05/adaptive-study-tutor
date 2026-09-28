import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.workflow import study_tutor_workflow


print("=" * 70)
print("ADAPTIVE STUDY TUTOR - TWO ROUND ADAPTIVE TEST")
print("=" * 70)


# =========================================================
# ROUND 1
# =========================================================

round1_answers = [
    "Newton's third law",
    "Equal and opposite pairs",
    "No force",
    "Different objects",
    "No"
]


initial_state = {
    "student_id": "adaptive_student_two_round",
    "user_query": "Quiz me on Newton's third law",
    "action": "quiz",
    "topic": "Newton's third law",
    "quiz": [],

    # Round 1 answers
    "student_answers": round1_answers,

    "iteration": 0,
    "max_iterations": 3,
    "mastery_threshold": 70.0,
    "used_web_search": False,
}


print("\nROUND 1")
print("-" * 70)

print("Student answers:")

for index, answer in enumerate(round1_answers, start=1):
    print(f"{index}. {answer}")


print("\nExpected Round 1 score: 60%")


# =========================================================
# RUN ROUND 1
# =========================================================

print("\nStarting Round 1 workflow...")

result = study_tutor_workflow.invoke(initial_state)


print("\nRound 1 completed.")

print("Score:", result.get("score"))
print("Correct:", result.get("correct_count"))
print("Total:", result.get("total_questions"))
print("Iteration:", result.get("iteration"))


# =========================================================
# DISPLAY ROUND 1 EVALUATION
# =========================================================

evaluation_results = result.get(
    "evaluation_results",
    []
)

print("\nRound 1 Evaluation:")

for item in evaluation_results:

    print("\nQuestion:")
    print(item.get("question"))

    print("Student answer:")
    print(item.get("student_answer"))

    print("Correct answer:")
    print(item.get("correct_answer"))

    print("Correct:")
    print(item.get("correct"))


# =========================================================
# CHECK WHETHER ADAPTIVE ROUTING WAS TRIGGERED
# =========================================================

score = result.get("score", 0)

threshold = result.get(
    "mastery_threshold",
    70.0
)

if score < threshold:

    print("\n" + "=" * 70)
    print("ADAPTIVE ROUTING TRIGGERED")
    print("=" * 70)

    print(
        f"\nRound 1 score {score}% is below "
        f"the mastery threshold of {threshold}%."
    )

    print("\nThe tutor should now:")
    print("1. Identify weak concepts")
    print("2. Explain the weak concepts")
    print("3. Generate a fresh quiz")
    print("4. Wait for new student answers")


else:

    print("\nMastery already achieved.")

    print(
        f"Score {score}% >= "
        f"threshold {threshold}%"
    )

    sys.exit(0)


# =========================================================
# ROUND 2
# =========================================================

print("\n" + "=" * 70)
print("ROUND 2")
print("=" * 70)


# Simulate a student who improved after the explanation.
#
# 4/5 correct = 80%
#
# Question 3 is now corrected.
# Question 5 is now corrected.

round2_answers = [
    "Newton's third law",
    "Equal and opposite pairs",
    "An equal and opposite force",
    "Different objects",
    "Yes"
]


print("\nSimulated Round 2 answers:")

for index, answer in enumerate(
    round2_answers,
    start=1
):
    print(f"{index}. {answer}")


print("\nExpected Round 2 score: 100%")


# =========================================================
# PREPARE ROUND 2 STATE
# =========================================================

round2_state = dict(result)

# Replace the student's answers with the
# answers for the fresh quiz.
round2_state["student_answers"] = round2_answers

# Keep the adaptive iteration count.
round2_state["iteration"] = (
    result.get("iteration", 0)
)

# Make sure the action remains quiz.
round2_state["action"] = "quiz"


# =========================================================
# RUN ROUND 2
# =========================================================

print("\nStarting Round 2 workflow...")

result2 = study_tutor_workflow.invoke(
    round2_state
)


print("\nRound 2 completed.")


# =========================================================
# ROUND 2 RESULTS
# =========================================================

print("\n" + "=" * 70)
print("ROUND 2 RESULTS")
print("=" * 70)

print("\nScore:")
print(result2.get("score"))

print("\nCorrect answers:")
print(result2.get("correct_count"))

print("\nTotal questions:")
print(result2.get("total_questions"))

print("\nIteration:")
print(result2.get("iteration"))

print("\nMastery threshold:")
print(result2.get("mastery_threshold"))


# =========================================================
# ROUND 2 EVALUATION
# =========================================================

evaluation_results2 = result2.get(
    "evaluation_results",
    []
)

if evaluation_results2:

    print("\n" + "=" * 70)
    print("ROUND 2 QUESTION EVALUATION")
    print("=" * 70)

    for item in evaluation_results2:

        print("\nQuestion:")
        print(item.get("question"))

        print("Student answer:")
        print(item.get("student_answer"))

        print("Correct answer:")
        print(item.get("correct_answer"))

        print("Correct:")
        print(item.get("correct"))


# =========================================================
# FINAL RESPONSE
# =========================================================

print("\n" + "=" * 70)
print("FINAL RESPONSE")
print("=" * 70)

print(
    result2.get(
        "final_response",
        "No final response generated."
    )
)


# =========================================================
# FINAL ADAPTIVE STATUS
# =========================================================

final_score = result2.get(
    "score",
    0
)

final_threshold = result2.get(
    "mastery_threshold",
    70.0
)


print("\n" + "=" * 70)
print("ADAPTIVE LEARNING STATUS")
print("=" * 70)

if final_score >= final_threshold:

    print("\nMASTERY ACHIEVED")

    print(
        f"Final score: {final_score}%"
    )

    print(
        f"Mastery threshold: {final_threshold}%"
    )

    print(
        "\nThe student improved after "
        "the adaptive explanation."
    )

else:

    print("\nMASTERY NOT YET ACHIEVED")

    print(
        f"Final score: {final_score}%"
    )

    print(
        f"Mastery threshold: {final_threshold}%"
    )


# =========================================================
# CITATIONS
# =========================================================

citations = result2.get(
    "citations",
    []
)

if citations:

    print("\n" + "=" * 70)
    print("TEXTBOOK CITATIONS")
    print("=" * 70)

    for citation in citations:
        print("-", citation)


print("\n" + "=" * 70)
print("TWO ROUND ADAPTIVE TEST FINISHED")
print("=" * 70)