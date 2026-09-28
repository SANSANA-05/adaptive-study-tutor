from mcp_server.client import call_tool


def evaluator_agent(
    student_id: str,
    topic: str,
    quiz: list,
    student_answers: list,
    difficulty: str = "medium"
):
    """
    Evaluator Agent.

    Evaluates the student's quiz answers,
    calculates the score, identifies weak questions,
    and saves the result through the custom MCP server.
    """

    # =====================================================
    # EVALUATE ANSWERS
    # =====================================================

    total_questions = len(quiz)
    correct_count = 0
    results = []

    for index, question in enumerate(quiz):

        # Get correct answer
        correct_answer = question.get(
            "correct_answer",
            ""
        )

        # Get student's answer
        if index < len(student_answers):
            student_answer = student_answers[index]
        else:
            student_answer = ""

        # Make sure values are strings
        student_answer = str(student_answer).strip()
        correct_answer = str(correct_answer).strip()

        # Compare answers
        is_correct = (
            student_answer.lower()
            == correct_answer.lower()
        )

        if is_correct:
            correct_count += 1

        # Question number can be either "question_number"
        # or "id", depending on the quiz generator.
        question_number = question.get(
            "question_number",
            question.get("id", index + 1)
        )

        # Store complete evaluation result
        results.append(
            {
                "question_number": question_number,

                "question":
                    question.get(
                        "question",
                        ""
                    ),

                "student_answer":
                    student_answer,

                "correct_answer":
                    correct_answer,

                # Main field used by the workflow
                "correct":
                    is_correct,

                # Keep is_correct as well
                # for compatibility/debugging
                "is_correct":
                    is_correct,

                "explanation":
                    question.get(
                        "short_explanation",
                        ""
                    )
            }
        )

    # =====================================================
    # CALCULATE SCORE
    # =====================================================

    if total_questions > 0:
        score = (
            correct_count
            / total_questions
        ) * 100
    else:
        score = 0.0

    score = round(score, 2)

    # =====================================================
    # IDENTIFY WEAK QUESTIONS
    # =====================================================

    weak_questions = [
        result
        for result in results
        if not result["correct"]
    ]

    # =====================================================
    # GENERATE FEEDBACK
    # =====================================================

    if score >= 80:

        feedback = (
            "Excellent work! You have demonstrated "
            "a strong understanding of this topic."
        )

    elif score >= 70:

        feedback = (
            "Good work! You understand most of the "
            "topic, but a few areas may need more practice."
        )

    elif score >= 50:

        feedback = (
            "You have a basic understanding of the topic, "
            "but some concepts need additional revision."
        )

    else:

        feedback = (
            "This topic needs more practice. The tutor "
            "should explain the weak concepts again "
            "before giving you another quiz."
        )

    # =====================================================
    # SAVE PROGRESS THROUGH MCP
    # =====================================================

    mcp_result = call_tool(
        "save_student_progress",
        {
            "student_id": student_id,
            "topic": topic,
            "score": correct_count,
            "total_questions": total_questions,
            "difficulty": difficulty
        }
    )

    # =====================================================
    # CHECK MCP RESULT
    # =====================================================

    if mcp_result.is_error:
        raise RuntimeError(
            "MCP save_student_progress tool failed."
        )

    progress_saved = True

    # =====================================================
    # RETURN EVALUATION
    # =====================================================

    return {
        "score": score,

        "correct_count":
            correct_count,

        "total_questions":
            total_questions,

        "feedback":
            feedback,

        "results":
            results,

        "weak_questions":
            weak_questions,

        "progress_saved":
            progress_saved
    }