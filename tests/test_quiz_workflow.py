import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from graph.workflow import study_tutor_workflow


print("\n============================================")
print("Adaptive Study Tutor - Quiz Workflow Test")
print("============================================\n")


result = study_tutor_workflow.invoke(
    {
        "student_id": "student_test",
        "user_query": "Quiz me on Newton's Laws of Motion",
        "iteration": 0,
        "max_iterations": 3,
        "mastery_threshold": 80
    }
)


print("ACTION:")
print(result.get("action"))

print("\nTOPIC:")
print(result.get("topic"))

print("\nNUMBER OF QUESTIONS:")
print(len(result.get("quiz", [])))

print("\nQUIZ:")
print("-" * 60)


for index, question in enumerate(
    result.get("quiz", []),
    start=1
):
    print(f"\nQuestion {index}:")
    print(question["question"])

    for option_index, option in enumerate(
        question["options"],
        start=1
    ):
        print(f"  {option_index}. {option}")


print("\n" + "=" * 60)
print("FINAL RESPONSE:")
print("=" * 60)

print(result.get("final_response"))


print("\n============================================")
print("Quiz workflow test completed!")
print("============================================")