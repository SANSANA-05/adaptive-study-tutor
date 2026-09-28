import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.quiz_master import quiz_master_agent
from agents.evaluator import evaluator_agent
from mcp_server.client import call_tool


print("\n============================================")
print("Adaptive Study Tutor - Evaluator Test")
print("============================================\n")


# --------------------------------------------------
# STEP 1: Generate Quiz
# --------------------------------------------------

print("STEP 1: Generating quiz...\n")

quiz = quiz_master_agent(
    topic="Newton's Laws of Motion",
    num_questions=5,
    difficulty="medium"
)

print(f"Quiz generated with {len(quiz)} questions.")


# --------------------------------------------------
# STEP 2: Display Quiz Answers
# --------------------------------------------------

print("\nCorrect answers in the generated quiz:")

for index, question in enumerate(quiz, start=1):
    print(
        f"Question {index}: "
        f"{question['correct_answer']}"
    )


# --------------------------------------------------
# STEP 3: Simulate Student Answers
# --------------------------------------------------

# We intentionally make some answers wrong
# so that we can test the evaluator.

student_answers = []

for index, question in enumerate(quiz):

    correct_answer = question["correct_answer"]

    if index in [1, 3]:
        # Intentionally wrong answers
        student_answers.append(
            "Wrong answer for testing"
        )
    else:
        # Correct answer
        student_answers.append(
            correct_answer
        )


print("\nStudent answers:")

for index, answer in enumerate(student_answers, start=1):
    print(f"Question {index}: {answer}")


# --------------------------------------------------
# STEP 4: Evaluate Answers
# --------------------------------------------------

print("\nEvaluating answers...\n")

evaluation = evaluator_agent(
    student_id="student_evaluator_test",
    topic="Newton's Laws of Motion",
    quiz=quiz,
    student_answers=student_answers,
    difficulty="medium"
)


# --------------------------------------------------
# STEP 5: Display Result
# --------------------------------------------------

print("============================================")
print("EVALUATION RESULT")
print("============================================")

print(f"\nScore: {evaluation['score']}%")

print(
    f"Correct Answers: "
    f"{evaluation['correct_count']}/"
    f"{evaluation['total_questions']}"
)

print("\nFeedback:")
print(evaluation["feedback"])


# --------------------------------------------------
# STEP 6: Question-by-Question Review
# --------------------------------------------------

print("\nQuestion Review:")
print("-" * 60)

for result in evaluation["results"]:

    status = "CORRECT" if result["is_correct"] else "INCORRECT"

    print(
        f"\nQuestion {result['question_number']}: "
        f"{status}"
    )

    print(
        f"Your Answer: "
        f"{result['student_answer']}"
    )

    print(
        f"Correct Answer: "
        f"{result['correct_answer']}"
    )

    print(
        f"Explanation: "
        f"{result['explanation']}"
    )


# --------------------------------------------------
# STEP 7: Verify SQLite Progress
# --------------------------------------------------

print("\n============================================")
print("CHECKING SAVED PROGRESS")
print("============================================\n")

result = call_tool(
    "weak_topics",
    {
        "student_id": "student_evaluator_test",
        "limit": 5
    }
)

if result.is_error:
    raise RuntimeError(
        "MCP weak_topics tool failed."
    )


response_text = result.content[0].text

print("Raw MCP response:")
print(response_text)

progress_data = json.loads(response_text)


# --------------------------------------------------
# STEP 8: Display Progress
# --------------------------------------------------

print("\nSaved progress:")

if isinstance(progress_data, dict):

    print(
        f"Topic: "
        f"{progress_data.get('topic')}"
    )

    print(
        f"Average Score: "
        f"{progress_data.get('average_score')}%"
    )

    print(
        f"Attempts: "
        f"{progress_data.get('attempts')}"
    )

elif isinstance(progress_data, list):

    for topic in progress_data:

        print(
            f"- {topic.get('topic')}: "
            f"{topic.get('average_score')}% "
            f"({topic.get('attempts')} attempts)"
        )


print("\n============================================")
print("Evaluator workflow test completed!")
print("============================================")