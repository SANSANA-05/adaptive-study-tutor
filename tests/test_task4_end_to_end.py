import sys
from pathlib import Path

# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from graph.workflow import study_tutor_workflow
from agents.quiz_master import quiz_master_agent


# ============================================================
# TEST CONFIGURATION
# ============================================================

STUDENT_ID = "task4_end_to_end_student"

TOPIC = "Newton Third Law"


# ============================================================
# HELPER
# ============================================================

def print_section(title):
    print("\n")
    print("=" * 60)
    print(title)
    print("=" * 60)


# ============================================================
# TEST 1 — EXPLAIN A TOPIC
# ============================================================

def test_explain_topic():

    print_section("TEST 1 - EXPLAIN A TOPIC")

    result = study_tutor_workflow.invoke({
        "student_id": STUDENT_ID,
        "user_query": "Explain Newton's third law with an example."
    })

    final_response = result.get(
        "final_response",
        ""
    )

    print("\nFinal response:")
    print(final_response)

    assert final_response, (
        "Explain workflow did not produce a final response."
    )

    assert (
        "Newton" in final_response
        or "force" in final_response
        or "action" in final_response
        or "reaction" in final_response
    ), (
        "Explanation does not appear to contain "
        "Newton's third-law content."
    )

    print("\n✓ Explanation generated.")
    print("✓ Explain-topic workflow passed.")

    return result


# ============================================================
# TEST 2 — GENERATE A QUIZ
# ============================================================

def test_quiz_generation():

    print_section("TEST 2 - QUIZ GENERATION")

    result = study_tutor_workflow.invoke({
        "student_id": STUDENT_ID,
        "user_query": "Quiz me on Newton's third law."
    })

    quiz = result.get(
        "quiz",
        []
    )

    final_response = result.get(
        "final_response",
        ""
    )

    print("\nGenerated questions:")

    for index, question in enumerate(
        quiz,
        start=1
    ):

        print(
            f"\n{index}. "
            f"{question.get('question', '')}"
        )

        options = question.get(
            "options",
            []
        )

        for option in options:
            print(
                f"   - {option}"
            )

    print("\nFinal response:")
    print(final_response)

    assert quiz, (
        "Quiz was not generated."
    )

    assert len(quiz) == 5, (
        f"Expected 5 questions, got {len(quiz)}."
    )

    print("\n✓ Quiz generated.")
    print("✓ Quiz contains 5 questions.")
    print("✓ Quiz-generation workflow passed.")

    return quiz


# ============================================================
# TEST 3 — EVALUATE A QUIZ
# ============================================================

def test_quiz_evaluation(quiz):

    print_section("TEST 3 - QUIZ EVALUATION")

    # Intentionally answer using the first option
    # for each question.
    #
    # This gives us a deterministic test of the
    # evaluator and progress-saving pipeline.

    student_answers = []

    for question in quiz:

        options = question.get(
            "options",
            []
        )

        if options:
            student_answers.append(
                options[0]
            )
        else:
            student_answers.append(
                ""
            )

    print("\nStudent answers:")

    for index, answer in enumerate(
        student_answers,
        start=1
    ):
        print(
            f"Question {index}: {answer}"
        )

    evaluation_result = study_tutor_workflow.invoke({

        "student_id": STUDENT_ID,

        "user_query": (
            "Evaluate my answers for "
            "Newton's third law."
        ),

        "topic": TOPIC,

        "action": "quiz",

        "quiz": quiz,

        "student_answers": student_answers,

        "iteration": 0,

        "max_iterations": 3,

        "mastery_threshold": 70.0
    })

    score = evaluation_result.get(
        "score",
        None
    )

    correct_count = evaluation_result.get(
        "correct_count",
        None
    )

    total_questions = evaluation_result.get(
        "total_questions",
        None
    )

    print("\nEvaluation:")
    print(
        f"Score: {score}%"
    )
    print(
        f"Correct: "
        f"{correct_count}/{total_questions}"
    )

    assert score is not None, (
        "Evaluator did not produce a score."
    )

    assert correct_count is not None, (
        "Evaluator did not produce correct_count."
    )

    assert total_questions == 5, (
        "Evaluator did not evaluate all 5 questions."
    )

    print("\n✓ Quiz evaluation completed.")
    print("✓ Score calculated.")
    print("✓ Progress-saving workflow executed.")

    return evaluation_result


# ============================================================
# TEST 4 — GET WEAK TOPICS
# ============================================================

def test_weak_topics():

    print_section("TEST 4 - WEAK TOPICS")

    result = study_tutor_workflow.invoke({

        "student_id": STUDENT_ID,

        "user_query": (
            "What topics am I weak in?"
        )
    })

    weak_topics = result.get(
        "weak_topics",
        []
    )

    final_response = result.get(
        "final_response",
        ""
    )

    print("\nWeak topics:")

    for topic in weak_topics:

        print(
            f"- {topic.get('topic')}: "
            f"{topic.get('average_score')}% "
            f"({topic.get('attempts')} attempts)"
        )

    print("\nFinal response:")
    print(final_response)

    assert weak_topics, (
        "No weak topics were returned."
    )

    assert any(
        topic.get("topic") == TOPIC
        for topic in weak_topics
    ), (
        "Newton Third Law was not found "
        "in weak topics."
    )

    print("\n✓ Weak topics retrieved.")
    print("✓ SQLite progress data is being used.")
    print("✓ Weak-topic workflow passed.")

    return result


# ============================================================
# TEST 5 — REVISION PLAN
# ============================================================

def test_revision_plan():

    print_section("TEST 5 - PERSONALIZED REVISION PLAN")

    result = study_tutor_workflow.invoke({

        "student_id": STUDENT_ID,

        "user_query": (
            "Make me a revision plan "
            "for my weak topics."
        ),

        "available_time": "7 days"
    })

    revision_plan = result.get(
        "revision_plan",
        ""
    )

    final_response = result.get(
        "final_response",
        ""
    )

    print("\nRevision plan:")
    print(revision_plan)

    print("\nFinal response:")
    print(final_response)

    assert revision_plan, (
        "Revision planner did not generate a plan."
    )

    assert (
        "Day 1" in revision_plan
        or "day 1" in revision_plan.lower()
    ), (
        "Revision plan does not contain a day-by-day schedule."
    )

    assert (
        "Newton Third Law" in revision_plan
    ), (
        "Revision plan does not use the student's weak topic."
    )

    print("\n✓ Personalized revision plan generated.")
    print("✓ Weak-topic information used.")
    print("✓ Revision-planner workflow passed.")

    return result


# ============================================================
# MAIN
# ============================================================

def main():

    print_section(
        "ADAPTIVE STUDY TUTOR - TASK 4 END-TO-END TEST"
    )

    print(
        "\nTesting the complete Task 4 workflow:"
    )

    print(
        "Explain → Quiz → Evaluate → "
        "Weak Topics → Revision Plan"
    )

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    test_explain_topic()

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    quiz = test_quiz_generation()

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    test_quiz_evaluation(
        quiz
    )

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    test_weak_topics()

    # --------------------------------------------------------
    # TEST 5
    # --------------------------------------------------------

    test_revision_plan()

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print_section(
        "TASK 4 END-TO-END TEST COMPLETED"
    )

    print(
        "\n✓ Explain workflow passed."
    )

    print(
        "✓ Quiz generation workflow passed."
    )

    print(
        "✓ Quiz evaluation workflow passed."
    )

    print(
        "✓ Weak-topic detection workflow passed."
    )

    print(
        "✓ Personalized revision planning passed."
    )

    print(
        "\nAll tested Task 4 user journeys are working "
        "through the LangGraph workflow."
    )


if __name__ == "__main__":
    main()