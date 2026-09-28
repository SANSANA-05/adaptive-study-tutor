import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from graph.workflow import study_tutor_workflow


def main():

    print("\n" + "=" * 60)
    print("ADAPTIVE STUDY TUTOR - MAXIMUM ITERATION TEST")
    print("=" * 60)

    initial_state = {
        "student_id": "max_iteration_student",
        "user_query": "Quiz me on Newton's third law",
        "action": "quiz",
        "topic": "Newton's Third Law of Motion",
        "difficulty": "medium",
        "num_questions": 5,
        "student_answers": [],
        "iteration": 0,
        "max_iterations": 3,
        "mastery_threshold": 70.0
    }

    print("\nStarting adaptive workflow...")
    print("-" * 60)

    state = study_tutor_workflow.invoke(initial_state)

    print("\nInitial quiz generated.")

    # ---------------------------------------------------------
    # SIMULATE THREE LOW-SCORE ATTEMPTS
    # ---------------------------------------------------------

    for attempt in range(1, 4):

        quiz = state.get("quiz", [])

        if not quiz:
            print("\nERROR: No quiz available.")
            return

        print("\n" + "=" * 60)
        print(f"ATTEMPT {attempt}")
        print("=" * 60)

        print(f"Questions: {len(quiz)}")
        print(f"Current iteration: {state.get('iteration', 0)}")

        # Deliberately submit incorrect answers
        wrong_answers = [
            "Wrong answer",
            "Wrong answer",
            "Wrong answer",
            "Wrong answer",
            "Wrong answer"
        ]

        state_with_answers = dict(state)
        state_with_answers["student_answers"] = wrong_answers

        print("\nSubmitting intentionally incorrect answers...")

        state = study_tutor_workflow.invoke(
            state_with_answers
        )

        score = state.get("score", 0)
        iteration = state.get("iteration", 0)

        print(f"Score: {score}%")
        print(f"Iteration: {iteration}")

        print(
            f"Maximum iterations: "
            f"{state.get('max_iterations', 3)}"
        )

        if score < state.get("mastery_threshold", 70):
            print("✓ Score is below mastery threshold.")
        else:
            print("✓ Mastery reached.")

        # -----------------------------------------------------
        # CHECK FINAL TERMINATION
        # -----------------------------------------------------

        if iteration >= state.get("max_iterations", 3):

            print("\n" + "-" * 60)
            print("MAXIMUM ITERATION CHECK")
            print("-" * 60)

            print("✓ Maximum iteration limit reached.")
            print("✓ Adaptive loop should terminate.")
            break

        # -----------------------------------------------------
        # CHECK ADAPTIVE ROUTING
        # -----------------------------------------------------

        if state.get("quiz"):

            print("✓ Another quiz is available.")
            print("✓ Adaptive loop continues.")

        else:

            print("WARNING: No next quiz found.")

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL WORKFLOW STATE")
    print("=" * 60)

    print(f"Final score: {state.get('score', 0)}%")
    print(f"Final iteration: {state.get('iteration', 0)}")
    print(
        f"Maximum iterations: "
        f"{state.get('max_iterations', 3)}"
    )

    print("\nFinal response:")
    print(state.get("final_response", ""))

    print("\n" + "=" * 60)
    print("MAXIMUM ITERATION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()