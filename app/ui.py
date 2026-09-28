import sys
import json
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# STREAMLIT PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Adaptive Study Tutor",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

if "student_id" not in st.session_state:
    st.session_state.student_id = "student_001"

if "general_result" not in st.session_state:
    st.session_state.general_result = None

if "adaptive_iteration" not in st.session_state:
    st.session_state.adaptive_iteration = 0

if "adaptive_explanation" not in st.session_state:
    st.session_state.adaptive_explanation = ""


# =========================================================
# APPLICATION TITLE
# =========================================================

st.title("📚 Adaptive Study Tutor")

st.write(
    "An AI-powered personalized learning assistant that "
    "explains concepts, quizzes students, tracks progress, "
    "and creates revision plans."
)

st.divider()


# =========================================================
# STUDENT INFORMATION
# =========================================================

st.subheader("👨‍🎓 Student Information")

student_id = st.text_input(
    "Student ID",
    value=st.session_state.student_id
)

st.session_state.student_id = student_id


# =========================================================
# ACTION SELECTION
# =========================================================

st.subheader("🎯 What would you like to do?")

action = st.selectbox(
    "Choose an action",
    [
        "Explain a topic",
        "Take a quiz",
        "Review my weak topics",
        "Create a revision plan"
    ]
)


# =========================================================
# QUESTION / TOPIC INPUT
# =========================================================

if action == "Explain a topic":

    question = st.text_area(
        "What would you like to learn?",
        placeholder=(
            "Example: Explain Newton's third law "
            "with an example."
        )
    )

elif action == "Take a quiz":

    question = st.text_input(
        "Enter the quiz topic",
        placeholder=(
            "Example: Newton's Laws of Motion"
        )
    )

elif action == "Review my weak topics":

    question = "What topics am I weak in?"

else:

    question = st.text_input(
        "What subject/topic should the plan focus on?",
        placeholder="Example: Physics"
    )


# =========================================================
# AVAILABLE STUDY TIME
# =========================================================

if action == "Create a revision plan":

    available_time = st.text_input(
        "Available study time",
        value="7 days"
    )

else:

    available_time = "7 days"


st.divider()


# =========================================================
# START LEARNING
# =========================================================

if st.button(
    "🚀 Start Learning",
    type="primary"
):

    # -----------------------------------------------------
    # VALIDATE STUDENT ID
    # -----------------------------------------------------

    if not student_id.strip():

        st.error(
            "Please enter a Student ID."
        )

        st.stop()


    # =====================================================
    # REVIEW WEAK TOPICS THROUGH MCP
    # =====================================================

    if action == "Review my weak topics":

        try:

            # Import MCP client
            from mcp_server.client import call_tool

            # Call custom MCP server
            mcp_result = call_tool(
                "weak_topics",
                {
                    "student_id": student_id,
                    "limit": 5
                }
            )


            # Check MCP error
            if mcp_result.is_error:

                raise RuntimeError(
                    "MCP weak_topics tool failed."
                )


            weak_topics = []


            # -------------------------------------------------
            # Read MCP response
            # -------------------------------------------------

            for content_item in mcp_result.content:

                if hasattr(
                    content_item,
                    "text"
                ):

                    data = json.loads(
                        content_item.text
                    )

                    weak_topics.append(
                        data
                    )


            # -------------------------------------------------
            # Store result
            # -------------------------------------------------

            st.session_state.general_result = {

                "action": "review",

                "topic": "",

                "weak_topics":
                    weak_topics
            }


            st.session_state.quiz = None

            st.session_state.quiz_result = None


            st.rerun()


        except Exception as error:

            st.error(
                "Could not retrieve your learning progress "
                "through the MCP server."
            )

            st.exception(error)

            st.stop()


    # =====================================================
    # VALIDATE QUESTION
    # =====================================================

    if not question.strip():

        st.error(
            "Please enter a topic or question."
        )

        st.stop()


    # =====================================================
    # TAKE QUIZ
    # =====================================================

    if action == "Take a quiz":

        try:

            from graph.workflow import (
                study_tutor_workflow
            )

        except Exception as error:

            st.error(
                "The Adaptive Study Tutor workflow "
                "could not be loaded."
            )

            st.exception(error)

            st.stop()


        with st.spinner(
            "🤖 Quiz Master is preparing your quiz..."
        ):

            try:

                quiz_state = {

                    "student_id":
                        student_id,

                    "user_query":
                        question,

                    "available_time":
                        available_time,

                    "iteration":
                        0,

                    "max_iterations":
                        3,

                    "mastery_threshold":
                        80
                }


                result = (
                    study_tutor_workflow.invoke(
                        quiz_state
                    )
                )


            except Exception as error:

                st.error(
                    "An error occurred while "
                    "generating the quiz."
                )

                st.exception(error)

                st.stop()


        quiz = result.get(
            "quiz",
            []
        )


        if not quiz:

            st.error(
                "No quiz questions were generated."
            )

            st.stop()


        # -------------------------------------------------
        # Store quiz
        # -------------------------------------------------

        st.session_state.quiz = quiz

        st.session_state.quiz_topic = question

        st.session_state.quiz_result = None

        st.session_state.general_result = None

        st.session_state.adaptive_iteration = 0

        st.session_state.adaptive_explanation = ""


        st.success(
            "🎯 Your quiz is ready!"
        )

        st.rerun()


    # =====================================================
    # EXPLAIN TOPIC / REVISION PLAN
    # =====================================================

    else:

        try:

            from graph.workflow import (
                study_tutor_workflow
            )

        except Exception as error:

            st.error(
                "The Adaptive Study Tutor workflow "
                "could not be loaded."
            )

            st.exception(error)

            st.stop()


        initial_state = {

            "student_id":
                student_id,

            "user_query":
                question,

            "available_time":
                available_time,

            "iteration":
                0,

            "max_iterations":
                3,

            "mastery_threshold":
                80
        }


        with st.spinner(
            "🤖 Adaptive Study Tutor is thinking..."
        ):

            try:

                result = (
                    study_tutor_workflow.invoke(
                        initial_state
                    )
                )

            except Exception as error:

                st.error(
                    "An error occurred while running "
                    "the Adaptive Study Tutor."
                )

                st.exception(error)

                st.stop()


        st.session_state.general_result = result

        st.session_state.quiz_result = None

        st.session_state.quiz = None


# =========================================================
# DISPLAY QUIZ
# =========================================================

if st.session_state.quiz:

    st.divider()


    # =====================================================
    # ADAPTIVE EXPLANATION
    # =====================================================

    if st.session_state.adaptive_explanation:

        st.subheader(
            "📖 Let's Review This Topic Again"
        )

        st.info(
            "Your previous score was below the "
            "mastery threshold. The tutor has "
            "identified concepts that need more "
            "practice."
        )

        st.write(
            st.session_state.adaptive_explanation
        )

        st.divider()


    # =====================================================
    # QUIZ HEADER
    # =====================================================

    st.subheader("📝 Quiz")

    st.write(
        f"**Topic:** "
        f"{st.session_state.quiz_topic}"
    )

    st.caption(
        f"Adaptive attempt: "
        f"{st.session_state.adaptive_iteration + 1} "
        f"of 3"
    )

    st.write(
        "Choose one answer for each question."
    )

    st.info(
        "💡 The correct answers will be shown "
        "only after you submit the quiz."
    )


    selected_answers = []


    # =====================================================
    # QUESTIONS
    # =====================================================

    for index, question_data in enumerate(
        st.session_state.quiz
    ):

        st.markdown(
            f"### Question {index + 1}"
        )

        st.write(
            question_data["question"]
        )


        options = question_data.get(
            "options",
            []
        )


        answer = st.radio(
            "Select your answer:",
            options,
            key=f"quiz_answer_{index}",
            index=None
        )


        selected_answers.append(
            answer
            if answer is not None
            else ""
        )


        st.divider()


    # =====================================================
    # SUBMIT QUIZ
    # =====================================================

    if st.button(
        "✅ Submit Quiz",
        type="primary"
    ):

        unanswered = [

            index + 1

            for index, answer
            in enumerate(selected_answers)

            if not answer
        ]


        if unanswered:

            st.warning(
                "Please answer all questions "
                "before submitting the quiz."
            )


        else:

            try:

                from graph.workflow import (
                    study_tutor_workflow
                )

            except Exception as error:

                st.error(
                    "The Adaptive Study Tutor workflow "
                    "could not be loaded."
                )

                st.exception(error)

                st.stop()


            # -------------------------------------------------
            # Evaluation state
            # -------------------------------------------------

            evaluation_state = {

                "student_id":
                    st.session_state.student_id,

                "user_query":
                    st.session_state.quiz_topic,

                "action":
                    "quiz",

                "topic":
                    st.session_state.quiz_topic,

                "quiz":
                    st.session_state.quiz,

                "student_answers":
                    selected_answers,

                "available_time":
                    available_time,

                "iteration":
                    st.session_state.adaptive_iteration,

                "max_iterations":
                    3,

                "mastery_threshold":
                    80
            }


            with st.spinner(
                "🧑‍🏫 Evaluating your answers..."
            ):

                try:

                    result = (
                        study_tutor_workflow.invoke(
                            evaluation_state
                        )
                    )

                except Exception as error:

                    st.error(
                        "An error occurred while "
                        "evaluating the quiz."
                    )

                    st.exception(error)

                    st.stop()


            # -------------------------------------------------
            # Get result
            # -------------------------------------------------

            score = result.get(
                "score",
                0
            )


            new_quiz = result.get(
                "quiz",
                []
            )


            new_iteration = result.get(
                "iteration",
                st.session_state.adaptive_iteration + 1
            )


            # =================================================
            # ADAPTIVE LOOP
            # =================================================

            if new_quiz and score < 80:

                st.session_state.adaptive_iteration = (
                    new_iteration
                )


                st.session_state.quiz = new_quiz


                st.session_state.quiz_topic = (
                    st.session_state.quiz_topic
                )


                st.session_state.adaptive_explanation = (
                    result.get(
                        "explanation",
                        ""
                    )
                )


                st.session_state.quiz_result = None

                st.session_state.general_result = None


                st.rerun()


            # =================================================
            # MASTERY / ITERATION LIMIT
            # =================================================

            else:

                st.session_state.adaptive_iteration = (
                    new_iteration
                )


                st.session_state.quiz_result = result

                st.session_state.quiz = None

                st.session_state.general_result = None

                st.session_state.adaptive_explanation = ""


                st.rerun()


# =========================================================
# DISPLAY QUIZ RESULT
# =========================================================

if st.session_state.quiz_result:

    result = (
        st.session_state.quiz_result
    )


    st.divider()

    st.subheader(
        "📊 Quiz Result"
    )


    score = result.get(
        "score",
        0
    )


    correct_count = result.get(
        "correct_count",
        0
    )


    total_questions = result.get(
        "total_questions",
        0
    )


    # -----------------------------------------------------
    # SCORE
    # -----------------------------------------------------

    st.metric(
        "Score",
        f"{score}%"
    )


    st.write(
        f"**Correct Answers:** "
        f"{correct_count} / "
        f"{total_questions}"
    )


    # -----------------------------------------------------
    # FEEDBACK
    # -----------------------------------------------------

    feedback = result.get(
        "feedback",
        ""
    )


    if feedback:

        st.info(
            f"💬 {feedback}"
        )


    # -----------------------------------------------------
    # ADAPTIVE EXPLANATION
    # -----------------------------------------------------

    explanation = result.get(
        "explanation",
        ""
    )


    if explanation:

        st.subheader(
            "📖 Additional Explanation"
        )

        st.write(
            explanation
        )


    # -----------------------------------------------------
    # ANSWER REVIEW
    # -----------------------------------------------------

    evaluation_results = result.get(
        "evaluation_results",
        []
    )


    if evaluation_results:

        st.subheader(
            "📋 Answer Review"
        )


        for item in evaluation_results:

            question_number = item.get(
                "question_number"
            )

            student_answer = item.get(
                "student_answer",
                ""
            )

            correct_answer = item.get(
                "correct_answer",
                ""
            )

            explanation = item.get(
                "explanation",
                ""
            )

            is_correct = item.get(
                "is_correct",
                False
            )


            st.markdown(
                f"### Question "
                f"{question_number}"
            )


            if is_correct:

                st.success(
                    f"✅ Correct: "
                    f"{student_answer}"
                )

            else:

                st.error(
                    f"❌ Your answer: "
                    f"{student_answer}"
                )

                st.write(
                    f"**Correct answer:** "
                    f"{correct_answer}"
                )


            if explanation:

                st.write(
                    f"**Explanation:** "
                    f"{explanation}"
                )


            st.divider()


    # =====================================================
    # MASTERY STATUS
    # =====================================================

    if score < 80:

        st.warning(
            "📚 Your score is below the mastery "
            "threshold of 80%. The tutor has identified "
            "that this topic needs additional practice."
        )

    else:

        st.success(
            "🎉 You reached the mastery threshold!"
        )


    # =====================================================
    # TAKE ANOTHER QUIZ
    # =====================================================

    if st.button(
        "🔄 Take Another Quiz"
    ):

        st.session_state.quiz_result = None

        st.session_state.quiz = None

        st.session_state.adaptive_iteration = 0

        st.session_state.adaptive_explanation = ""

        st.rerun()


# =========================================================
# DISPLAY GENERAL RESULT
# =========================================================

if st.session_state.general_result:

    result = (
        st.session_state.general_result
    )


    st.divider()


    # =====================================================
    # REVIEW WEAK TOPICS
    # =====================================================

    if result.get("action") == "review":

        st.subheader(
            "📊 Your Learning Progress"
        )


        weak_topics = result.get(
            "weak_topics",
            []
        )


        if weak_topics:

            st.write(
                "Based on your previous quiz "
                "performance, these are the topics "
                "that currently need more practice:"
            )


            for index, item in enumerate(
                weak_topics,
                start=1
            ):

                topic = item.get(
                    "topic",
                    "Unknown topic"
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
                    f"### {index}. {topic}"
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


                if average_score < 50:

                    st.error(
                        "🔴 Needs significant practice"
                    )

                elif average_score < 80:

                    st.warning(
                        "🟡 Needs additional revision"
                    )

                else:

                    st.success(
                        "🟢 Good performance"
                    )


                st.divider()


        else:

            st.info(
                "📚 No quiz history is available yet. "
                "Complete a quiz first so the tutor "
                "can identify your weak topics."
            )


    # =====================================================
    # NORMAL TUTOR RESPONSE
    # =====================================================

    else:

        st.subheader(
            "📖 Tutor Response"
        )


        final_response = result.get(
            "final_response",
            "No response was generated."
        )


        st.write(
            final_response
        )


        # -------------------------------------------------
        # PLANNER INFORMATION
        # -------------------------------------------------

        if result.get("action"):

            st.caption(
                "Action selected by Planner: "
                f"{result['action']}"
            )


        if result.get("topic"):

            st.caption(
                "Topic identified: "
                f"{result['topic']}"
            )


        # -------------------------------------------------
        # TEXTBOOK CITATIONS
        # -------------------------------------------------

        citations = result.get(
            "citations",
            []
        )


        if citations:

            st.subheader(
                "📚 Textbook Sources"
            )


            for citation in citations:

                st.write(
                    f"- {citation}"
                )


        # -------------------------------------------------
        # TAVILY STATUS
        # -------------------------------------------------

        if result.get(
            "used_web_search",
            False
        ):

            st.info(
                "🌐 Supplementary information "
                "was retrieved using Tavily."
            )