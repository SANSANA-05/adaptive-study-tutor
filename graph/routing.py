from graph.state import StudyTutorState


def route_after_planner(state: StudyTutorState) -> str:
    """
    Decide which agent should handle the student's request
    after the Planner Agent.
    """

    action = state.get("action", "explain")

    # If a quiz already exists and the student has submitted
    # answers, evaluate that quiz.
    if (
        action == "quiz"
        and state.get("quiz")
        and state.get("student_answers")
    ):
        return "evaluator"

    if action == "explain":
        return "explainer"

    if action == "quiz":
        return "quiz_master"

    if action == "review":
        return "review"

    if action == "plan":
        return "revision_planner"

    return "explainer"


def route_after_quiz_master(state: StudyTutorState) -> str:
    """
    Decide what happens after Quiz Master generates a quiz.

    If answers are already available, evaluate immediately.
    Otherwise, pause at quiz_ready so the quiz can be shown
    to the student.
    """

    student_answers = state.get(
        "student_answers",
        []
    )

    if student_answers:
        return "evaluator"

    return "quiz_ready"


def route_after_evaluator(state: StudyTutorState) -> str:
    """
    Decide what happens after the Evaluator grades a quiz.

    Low score:
        Evaluator → Adaptive Explainer → New Quiz

    Mastery:
        Evaluator → Final

    Maximum iterations:
        Evaluator → Final
    """

    score = state.get(
        "score",
        0
    )

    mastery_threshold = state.get(
        "mastery_threshold",
        70.0
    )

    iteration = state.get(
        "iteration",
        0
    )

    max_iterations = state.get(
        "max_iterations",
        3
    )

    # -----------------------------------------------------
    # MAXIMUM ITERATION CHECK
    # -----------------------------------------------------

    if iteration >= max_iterations:
        return "finish"

    # -----------------------------------------------------
    # LOW SCORE
    # -----------------------------------------------------

    if score < mastery_threshold:
        return "adaptive_explainer"

    # -----------------------------------------------------
    # MASTERY ACHIEVED
    # -----------------------------------------------------

    return "finish"