import sys
from pathlib import Path

# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# IMPORT WORKFLOW
# =========================================================

from graph.workflow import study_tutor_workflow


# =========================================================
# TEST ADAPTIVE QUIZ FLOW
# =========================================================

def main():

    print("\n" + "=" * 60)
    print("ADAPTIVE STUDY TUTOR - TWO-ROUND ADAPTIVE TEST")
    print("=" * 60)

    # =====================================================
    # ROUND 1
    # =====================================================

    initial_state = {

        "student_id":
            "adaptive_test_student",

        "user_query":
            "Quiz me on Newton's third law",

        "action":
            "quiz",

        "topic":
            "Newton's Third Law of Motion",

        "difficulty":
            "medium",

        "num_questions":
            5,

        "student_answers":
            [],

        "iteration":
            0,

        "max_iterations":
            3,

        "mastery_threshold":
            70.0
    }

    print("\nStarting Round 1...")
    print("-" * 60)

    round1 = study_tutor_workflow.invoke(
        initial_state
    )

    quiz1 = round1.get(
        "quiz",
        []
    )

    if not quiz1:

        print(
            "\nERROR: Round 1 quiz was not generated."
        )

        return

    print(
        f"\nRound 1 generated "
        f"{len(quiz1)} questions."
    )

    # =====================================================
    # DISPLAY ROUND 1 QUESTIONS
    # =====================================================

    print("\nROUND 1 QUESTIONS")
    print("-" * 60)

    for index, question in enumerate(
        quiz1,
        start=1
    ):

        question_number = (
            question.get("id")
            or question.get("question_number")
            or index
        )

        print(
            f"\n{question_number}. "
            f"{question.get('question', '')}"
        )

        for option in question.get(
            "options",
            []
        ):

            print(
                f"   - {option}"
            )

    # =====================================================
    # ROUND 1 STUDENT ANSWERS
    # =====================================================
    #
    # Intentionally poor performance:
    #
    # Question 1 → Correct
    # Question 2 → Correct
    # Question 3 → Wrong
    # Question 4 → Wrong
    # Question 5 → Wrong
    #
    # Expected score = 2 / 5 = 40%
    #
    # This should trigger:
    #
    # Evaluator
    #     ↓
    # Score < 70%
    #     ↓
    # Adaptive Explainer
    #     ↓
    # New Quiz
    #
    # =====================================================

    round1_answers = [

        "Newton's third law",

        "Equal and opposite pairs",

        "No force",

        "The same object",

        "No"
    ]

    print("\n" + "-" * 60)
    print("SUBMITTING ROUND 1 ANSWERS")
    print("-" * 60)

    for index, answer in enumerate(
        round1_answers,
        start=1
    ):

        print(
            f"Question {index}: {answer}"
        )

    # =====================================================
    # ROUND 1 → EVALUATOR
    # =====================================================

    state_after_round1 = dict(
        round1
    )

    state_after_round1[
        "student_answers"
    ] = round1_answers

    print("\nEvaluating Round 1...")

    evaluation1 = study_tutor_workflow.invoke(
        state_after_round1
    )

    # =====================================================
    # ROUND 1 EVALUATION
    # =====================================================

    score1 = evaluation1.get(
        "score",
        0
    )

    correct1 = evaluation1.get(
        "correct_count",
        0
    )

    total1 = evaluation1.get(
        "total_questions",
        len(quiz1)
    )

    iteration1 = evaluation1.get(
        "iteration",
        0
    )

    print("\n" + "-" * 60)
    print("ROUND 1 EVALUATION")
    print("-" * 60)

    print(
        f"Score: {score1}%"
    )

    print(
        f"Correct: {correct1}/{total1}"
    )

    print(
        f"Iteration: {iteration1}"
    )

    print(
        f"Feedback: "
        f"{evaluation1.get('feedback', '')}"
    )

    # =====================================================
    # CHECK ADAPTIVE ROUTING
    # =====================================================

    print("\n" + "-" * 60)
    print("CHECKING ADAPTIVE ROUTING")
    print("-" * 60)

    if score1 < 70:

        print(
            "✓ Score is below the 70% mastery threshold."
        )

        print(
            "✓ Adaptive learning should be triggered."
        )

    else:

        print(
            "ERROR: Score was not below the mastery threshold."
        )

        return

    # =====================================================
    # CHECK NEW QUIZ
    # =====================================================

    quiz2 = evaluation1.get(
        "quiz",
        []
    )

    explanation = evaluation1.get(
        "explanation",
        ""
    )

    print("\n" + "-" * 60)
    print("ADAPTIVE ROUND RESULT")
    print("-" * 60)

    print(
        evaluation1.get(
            "final_response",
            ""
        )
    )

    # =====================================================
    # VERIFY ADAPTIVE EXPLANATION
    # =====================================================

    if explanation:

        print(
            "\n✓ Adaptive explanation was generated."
        )

    else:

        print(
            "\nWARNING: No adaptive explanation was found."
        )

    # =====================================================
    # VERIFY NEW QUIZ
    # =====================================================

    if quiz2:

        print(
            f"✓ New quiz generated with "
            f"{len(quiz2)} questions."
        )

    else:

        print(
            "WARNING: New quiz was not found "
            "in the returned state."
        )

    # =====================================================
    # DISPLAY ADAPTIVE QUIZ
    # =====================================================

    if quiz2:

        print("\n" + "-" * 60)
        print("ADAPTIVE ROUND QUESTIONS")
        print("-" * 60)

        for index, question in enumerate(
            quiz2,
            start=1
        ):

            question_number = (
                question.get("id")
                or question.get("question_number")
                or index
            )

            print(
                f"\n{question_number}. "
                f"{question.get('question', '')}"
            )

            for option in question.get(
                "options",
                []
            ):

                print(
                    f"   - {option}"
                )

    # =====================================================
    # FINAL TEST STATUS
    # =====================================================

    print("\n" + "=" * 60)
    print("ADAPTIVE FLOW TEST COMPLETED")
    print("=" * 60)

    print("\nExpected adaptive flow:")

    print(
        "Round 1 Quiz"
        " → Evaluator"
        " → Low Score"
        " → Adaptive Explainer"
        " → New Quiz"
    )

    print("\nActual Round 1 score:")

    print(
        f"{score1}%"
    )

    print(
        "\nMastery threshold:"
    )

    print(
        "70%"
    )

    if score1 < 70 and explanation:

        print(
            "\n✓ Adaptive explanation detected."
        )

        print(
            "✓ Low-score condition detected."
        )

        print(
            "✓ Adaptive learning flow is working."
        )

    else:

        print(
            "\n⚠ Adaptive flow needs further debugging."
        )

    print("\n" + "=" * 60)


# =========================================================
# RUN TEST
# =========================================================

if __name__ == "__main__":
    main()