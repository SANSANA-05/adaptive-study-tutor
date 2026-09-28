import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# BACKEND IMPORTS
# ============================================================

from graph.workflow import study_tutor_workflow
from agents.guardrails import sanitize_quiz_for_student


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Adaptive Study Tutor",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "evaluation_result" not in st.session_state:
    st.session_state.evaluation_result = None

if "explanation" not in st.session_state:
    st.session_state.explanation = ""

if "weak_topics" not in st.session_state:
    st.session_state.weak_topics = []

if "revision_plan" not in st.session_state:
    st.session_state.revision_plan = ""


# ============================================================
# TITLE
# ============================================================

st.title("📚 Adaptive Study Tutor")

st.markdown(
    """
    ### Personalized AI-powered learning assistant

    Learn concepts from your syllabus, practice through quizzes,
    receive feedback, identify weak topics, and create a
    personalized revision plan.
    """
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Student")

    student_id = st.text_input(
        "Student ID",
        value="student_001"
    )

    st.divider()

    st.header("Learning Options")

    available_time = st.selectbox(
        "Revision duration",
        [
            "3 days",
            "5 days",
            "7 days",
            "14 days"
        ],
        index=2
    )

    st.divider()

    st.caption(
        "Adaptive Study Tutor"
    )

    st.caption(
        "Powered by LangGraph + RAG + MCP + Tavily"
    )


# ============================================================
# MAIN TABS
# ============================================================

tab_explain, tab_quiz, tab_progress, tab_revision = st.tabs(
    [
        "📖 Learn",
        "📝 Quiz",
        "📊 Progress",
        "📅 Revision Plan"
    ]
)


# ============================================================
# TAB 1 — EXPLAIN
# ============================================================

with tab_explain:

    st.header("📖 Learn a Topic")

    st.write(
        "Ask the tutor to explain a syllabus topic."
    )

    explanation_query = st.text_input(
        "What would you like to learn?",
        placeholder=(
            "Example: Explain Newton's third law "
            "with an example."
        ),
        key="explanation_query"
    )

    if st.button(
        "Explain Topic",
        type="primary",
        key="explain_button"
    ):

        if not explanation_query.strip():

            st.warning(
                "Please enter a topic or question."
            )

        else:

            with st.spinner(
                "Finding the relevant textbook content..."
            ):

                result = study_tutor_workflow.invoke(
                    {
                        "student_id": student_id,
                        "user_query": explanation_query
                    }
                )

            st.session_state.explanation = result.get(
                "final_response",
                ""
            )

    if st.session_state.explanation:

        st.divider()

        st.subheader("Explanation")

        st.markdown(
            st.session_state.explanation
        )


# ============================================================
# TAB 2 — QUIZ
# ============================================================

with tab_quiz:

    st.header("📝 Take a Quiz")

    st.write(
        "Generate a quiz and test your understanding."
    )

    quiz_topic = st.text_input(
        "Quiz topic",
        placeholder="Example: Newton's third law",
        key="quiz_topic_input"
    )

    col1, col2 = st.columns(2)

    with col1:

        num_questions = st.selectbox(
            "Number of questions",
            [3, 5, 7, 10],
            index=1
        )

    with col2:

        difficulty = st.selectbox(
            "Difficulty",
            [
                "easy",
                "medium",
                "hard"
            ],
            index=1
        )


    # ========================================================
    # GENERATE QUIZ
    # ========================================================

    if st.button(
        "Generate Quiz",
        type="primary",
        key="generate_quiz_button"
    ):

        if not quiz_topic.strip():

            st.warning(
                "Please enter a quiz topic."
            )

        else:

            with st.spinner(
                "Generating your quiz..."
            ):

                result = study_tutor_workflow.invoke(
                    {
                        "student_id": student_id,
                        "user_query": (
                            f"Quiz me on {quiz_topic}"
                        ),
                        "topic": quiz_topic,
                        "num_questions": num_questions,
                        "difficulty": difficulty,
                        "iteration": 0,
                        "max_iterations": 3,
                        "mastery_threshold": 70.0
                    }
                )

            # ------------------------------------------------
            # Store ORIGINAL quiz internally.
            #
            # This version may contain correct_answer
            # and explanation fields.
            #
            # It is required by the Evaluator Agent.
            # ------------------------------------------------

            st.session_state.quiz = result.get(
                "quiz",
                []
            )

            st.session_state.quiz_topic = quiz_topic

            st.session_state.quiz_submitted = False

            st.session_state.evaluation_result = None


    # ========================================================
    # DISPLAY QUIZ
    # ========================================================

    if st.session_state.quiz:

        st.divider()

        st.subheader(
            f"Quiz: {st.session_state.quiz_topic}"
        )

        st.info(
            "Select one answer for each question."
        )


        # ----------------------------------------------------
        # SECURITY / GUARDRAIL
        # ----------------------------------------------------
        #
        # Create a student-facing copy.
        #
        # The original quiz remains untouched internally.
        #
        # sanitize_quiz_for_student() removes:
        #     correct_answer
        #     explanation
        #
        # Therefore the student cannot see the answer
        # before submitting the quiz.
        # ----------------------------------------------------

        student_quiz = sanitize_quiz_for_student(
            st.session_state.quiz
        )


        quiz_answers = []


        # ====================================================
        # DISPLAY QUESTIONS
        # ====================================================

        for index, question in enumerate(
            student_quiz
        ):

            st.markdown(
                f"### Question {index + 1}"
            )

            st.write(
                question.get(
                    "question",
                    ""
                )
            )

            options = question.get(
                "options",
                []
            )


            # ------------------------------------------------
            # No answer selected initially.
            #
            # This prevents Streamlit from automatically
            # selecting the first option.
            # ------------------------------------------------

            selected_answer = st.radio(
                "Choose your answer:",
                options,
                index=None,
                key=f"quiz_answer_{index}"
            )

            quiz_answers.append(
                selected_answer
            )


        st.divider()


        # ====================================================
        # SUBMIT QUIZ
        # ====================================================

        if st.button(
            "Submit Quiz",
            type="primary",
            key="submit_quiz_button"
        ):

            # -----------------------------------------------
            # Make sure every question has an answer.
            # -----------------------------------------------

            unanswered_questions = [
                index + 1
                for index, answer in enumerate(quiz_answers)
                if answer is None
            ]

            if unanswered_questions:

                st.warning(
                    "Please answer all questions before "
                    "submitting the quiz."
                )

                st.info(
                    "Unanswered questions: "
                    + ", ".join(
                        str(number)
                        for number in unanswered_questions
                    )
                )

            else:

                with st.spinner(
                    "Evaluating your answers..."
                ):

                    result = study_tutor_workflow.invoke(
                        {
                            "student_id": student_id,

                            "user_query": (
                                f"Evaluate my answers for "
                                f"{st.session_state.quiz_topic}."
                            ),

                            "topic": st.session_state.quiz_topic,

                            "action": "quiz",

                            # IMPORTANT:
                            # Send the ORIGINAL quiz internally.
                            #
                            # It still contains correct answers
                            # required by the Evaluator Agent.
                            "quiz": st.session_state.quiz,

                            "student_answers": quiz_answers,

                            "iteration": 0,

                            "max_iterations": 3,

                            "mastery_threshold": 70.0,

                            "difficulty": difficulty
                        }
                    )

                st.session_state.evaluation_result = result

                st.session_state.quiz_submitted = True


        # ====================================================
        # DISPLAY EVALUATION
        # ====================================================

        if st.session_state.quiz_submitted:

            evaluation = (
                st.session_state.evaluation_result
            )

            if evaluation:

                st.divider()

                st.subheader(
                    "📊 Quiz Result"
                )


                # --------------------------------------------
                # SCORE
                # --------------------------------------------

                score = evaluation.get(
                    "score",
                    0
                )

                correct_count = evaluation.get(
                    "correct_count",
                    0
                )

                total_questions = evaluation.get(
                    "total_questions",
                    len(st.session_state.quiz)
                )


                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Score",
                        f"{score}%"
                    )

                with col2:

                    st.metric(
                        "Correct",
                        correct_count
                    )

                with col3:

                    st.metric(
                        "Questions",
                        total_questions
                    )


                # --------------------------------------------
                # GENERAL FEEDBACK
                # --------------------------------------------

                feedback = evaluation.get(
                    "feedback",
                    ""
                )

                if feedback:

                    st.info(
                        feedback
                    )


                # --------------------------------------------
                # QUESTION-WISE FEEDBACK
                # --------------------------------------------

                results = evaluation.get(
                    "evaluation_results",
                    []
                )

                if results:

                    st.subheader(
                        "Question-wise Feedback"
                    )


                    for index, item in enumerate(
                        results
                    ):

                        question_text = item.get(
                            "question",
                            ""
                        )

                        student_answer = item.get(
                            "student_answer",
                            ""
                        )

                        correct_answer = item.get(
                            "correct_answer",
                            ""
                        )

                        is_correct = item.get(
                            "correct",
                            False
                        )


                        st.markdown(
                            f"**Question {index + 1}:** "
                            f"{question_text}"
                        )

                        st.write(
                            f"Your answer: "
                            f"{student_answer}"
                        )

                        # ------------------------------------------------
                        # Correct answer is shown ONLY AFTER submission.
                        # ------------------------------------------------

                        st.write(
                            f"Correct answer: "
                            f"{correct_answer}"
                        )


                        if is_correct:

                            st.success(
                                "Correct"
                            )

                        else:

                            st.error(
                                "Needs review"
                            )


# ============================================================
# TAB 3 — PROGRESS
# ============================================================

with tab_progress:

    st.header("📊 My Progress")

    st.write(
        "View the topics where you need more practice."
    )


    if st.button(
        "Check My Weak Topics",
        type="primary",
        key="weak_topics_button"
    ):

        with st.spinner(
            "Analyzing your quiz history..."
        ):

            result = study_tutor_workflow.invoke(
                {
                    "student_id": student_id,
                    "user_query": (
                        "What topics am I weak in?"
                    )
                }
            )

        st.session_state.weak_topics = result.get(
            "weak_topics",
            []
        )


    if st.session_state.weak_topics:

        st.divider()

        st.subheader(
            "Your Current Weak Topics"
        )


        for item in st.session_state.weak_topics:

            topic = item.get(
                "topic",
                "Unknown"
            )

            average_score = item.get(
                "average_score",
                0
            )

            attempts = item.get(
                "attempts",
                0
            )


            st.markdown(
                f"### {topic}"
            )


            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Average Score",
                    f"{average_score}%"
                )

            with col2:

                st.metric(
                    "Attempts",
                    attempts
                )


            st.divider()


    else:

        st.info(
            "No weak-topic information available yet. "
            "Complete a quiz first."
        )


# ============================================================
# TAB 4 — REVISION PLAN
# ============================================================

with tab_revision:

    st.header("📅 Personalized Revision Plan")

    st.write(
        "Generate a study plan based on your weak topics "
        "and available preparation time."
    )


    if st.button(
        "Create Revision Plan",
        type="primary",
        key="revision_plan_button"
    ):

        with st.spinner(
            "Creating your personalized revision plan..."
        ):

            result = study_tutor_workflow.invoke(
                {
                    "student_id": student_id,

                    "user_query": (
                        "Make me a revision plan "
                        "for my weak topics."
                    ),

                    "available_time": available_time
                }
            )

        st.session_state.revision_plan = result.get(
            "revision_plan",
            ""
        )


    if st.session_state.revision_plan:

        st.divider()

        st.markdown(
            st.session_state.revision_plan
        )

    else:

        st.info(
            "Complete some quizzes first so the tutor "
            "can create a personalized plan."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Adaptive Study Tutor | "
    "RAG + MCP + LangGraph + Tavily"
)