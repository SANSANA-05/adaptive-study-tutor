import sys
import json
from pathlib import Path


# ---------------------------------------------------------
# PROJECT ROOT FIX
# Allows this file to be run directly using:
# python graph\workflow.py
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------

from langgraph.graph import StateGraph, START, END

from graph.state import StudyTutorState

from graph.routing import (
    route_after_planner,
    route_after_quiz_master,
    route_after_evaluator
)

from agents.planner import planner_agent
from agents.explainer import explainer_agent
from agents.quiz_master import quiz_master_agent
from agents.evaluator import evaluator_agent
from agents.revision_planner import revision_planner_agent

from mcp_server.client import call_tool


# ---------------------------------------------------------
# 1. PLANNER NODE
# ---------------------------------------------------------

def planner_node(state: StudyTutorState):
    """
    Planner Agent decides what the tutor should do:

    explain
    quiz
    review
    plan

    If quiz data and student answers are already present,
    preserve the existing quiz action so the graph can
    continue directly to the Evaluator.
    """

    # -----------------------------------------------------
    # IMPORTANT:
    # If the caller already supplied a quiz and answers,
    # this is an evaluation request.
    #
    # Do not let the natural-language planner overwrite
    # the explicit evaluation state.
    # -----------------------------------------------------

    existing_action = state.get(
        "action",
        ""
    )

    existing_quiz = state.get(
        "quiz",
        []
    )

    existing_answers = state.get(
        "student_answers",
        []
    )

    if (
        existing_action == "quiz"
        and existing_quiz
        and existing_answers
    ):
        return {
            "action": "quiz",
            "topic": state.get(
                "topic",
                ""
            )
        }

    # -----------------------------------------------------
    # NORMAL PLANNER FLOW
    # -----------------------------------------------------

    user_query = state.get(
        "user_query",
        ""
    )

    decision = planner_agent(
        user_query
    )

    return {
        "action": decision.action,
        "topic": decision.topic
    }


# ---------------------------------------------------------
# 2. EXPLAINER NODE
# ---------------------------------------------------------

def explainer_node(state: StudyTutorState):
    """
    Explainer Agent explains the requested topic
    using the RAG knowledge base and, when required,
    supplementary ReAct web research.
    """

    topic = state.get(
        "topic",
        ""
    )

    question = state.get(
        "user_query",
        ""
    )

    result = explainer_agent(
        topic=topic,
        question=question
    )

    return {
        "explanation": result.get(
            "explanation",
            ""
        ),

        "citations": result.get(
            "citations",
            []
        ),

        "used_web_search": result.get(
            "used_web_search",
            False
        )
    }


# ---------------------------------------------------------
# 3. ADAPTIVE EXPLAINER NODE
# ---------------------------------------------------------

def adaptive_explainer_node(
    state: StudyTutorState
):
    """
    Explains the student's weak topic again
    after a low quiz score.

    Adaptive learning loop:

    Evaluator
        ↓
    Low Score
        ↓
    Adaptive Explainer
        ↓
    New Quiz
    """

    topic = state.get(
        "topic",
        ""
    )

    # -----------------------------------------------------
    # Build mistake-focused explanation request
    # -----------------------------------------------------

    evaluation_results = state.get(
        "evaluation_results",
        []
    )

    incorrect_summary = []

    for item in evaluation_results:

        if not item.get("correct", False):

            incorrect_summary.append(
                {
                    "question": item.get(
                        "question",
                        ""
                    ),
                    "student_answer": item.get(
                        "student_answer",
                        ""
                    ),
                    "correct_answer": item.get(
                        "correct_answer",
                        ""
                    )
                }
            )

    question = (
        f"Explain {topic} again in a simple way. "
        f"Focus especially on the concepts that the "
        f"student misunderstood."
    )

    if incorrect_summary:

        question += (
            "\n\nThe student's incorrect responses were:"
        )

        for item in incorrect_summary:

            question += (
                f"\n\nQuestion: "
                f"{item['question']}"
            )

            question += (
                f"\nStudent answer: "
                f"{item['student_answer']}"
            )

            question += (
                f"\nCorrect answer: "
                f"{item['correct_answer']}"
            )

    # -----------------------------------------------------
    # Run Explainer
    # -----------------------------------------------------

    result = explainer_agent(
        topic=topic,
        question=question
    )

    current_iteration = state.get(
        "iteration",
        0
    )

    return {

        "explanation": result.get(
            "explanation",
            ""
        ),

        "citations": result.get(
            "citations",
            []
        ),

        "used_web_search": result.get(
            "used_web_search",
            False
        ),

        # -------------------------------------------------
        # Clear previous quiz and answers.
        #
        # A fresh adaptive quiz will be generated.
        # -------------------------------------------------

        "quiz": [],

        "student_answers": [],

        # -------------------------------------------------
        # Increase adaptive iteration count.
        # -------------------------------------------------

        "iteration": current_iteration + 1
    }


# ---------------------------------------------------------
# 4. QUIZ MASTER NODE
# ---------------------------------------------------------

def quiz_master_node(
    state: StudyTutorState
):
    """
    Quiz Master Agent generates a quiz through
    the custom MCP server.
    """

    topic = state.get(
        "topic",
        ""
    )

    num_questions = state.get(
        "num_questions",
        5
    )

    difficulty = state.get(
        "difficulty",
        "medium"
    )

    iteration = state.get(
        "iteration",
        0
    )

    quiz = quiz_master_agent(
        topic=topic,
        num_questions=num_questions,
        difficulty=difficulty,
        attempt=iteration
    )

    return {
        "quiz": quiz
    }


# ---------------------------------------------------------
# 5. QUIZ READY NODE
# ---------------------------------------------------------

def quiz_ready_node(
    state: StudyTutorState
):
    """
    Marks that the quiz has been generated
    and is ready for the student.
    """

    return {
        "final_response": (
            "Quiz generated successfully. "
            "Please answer the questions."
        )
    }


# ---------------------------------------------------------
# 6. EVALUATOR NODE
# ---------------------------------------------------------

def evaluator_node(
    state: StudyTutorState
):
    """
    Evaluator Agent:

    1. Checks student answers.
    2. Calculates score.
    3. Generates feedback.
    4. Saves progress through MCP.
    """

    student_id = state.get(
        "student_id",
        "student_001"
    )

    topic = state.get(
        "topic",
        ""
    )

    quiz = state.get(
        "quiz",
        []
    )

    student_answers = state.get(
        "student_answers",
        []
    )

    difficulty = state.get(
        "difficulty",
        "medium"
    )

    result = evaluator_agent(
        student_id=student_id,
        topic=topic,
        quiz=quiz,
        student_answers=student_answers,
        difficulty=difficulty
    )

    return {

        "score": result.get(
            "score",
            0
        ),

        "correct_count": result.get(
            "correct_count",
            0
        ),

        "total_questions": result.get(
            "total_questions",
            len(quiz)
        ),

        "feedback": result.get(
            "feedback",
            ""
        ),

        "evaluation_results": result.get(
            "results",
            []
        )
    }


# ---------------------------------------------------------
# 7. REVIEW NODE
# ---------------------------------------------------------

def review_node(
    state: StudyTutorState
):
    """
    Retrieves the student's weak topics
    through the custom MCP server.
    """

    student_id = state.get(
        "student_id",
        "student_001"
    )

    result = call_tool(
        "weak_topics",
        {
            "student_id": student_id,
            "limit": 5
        }
    )

    if result.is_error:

        raise RuntimeError(
            "MCP weak_topics tool failed."
        )

    weak_topics = []

    for content_item in result.content:

        if hasattr(
            content_item,
            "text"
        ):

            try:

                data = json.loads(
                    content_item.text
                )

                weak_topics.append(
                    data
                )

            except json.JSONDecodeError:

                continue

    return {
        "weak_topics": weak_topics
    }


# ---------------------------------------------------------
# 8. REVISION PLANNER NODE
# ---------------------------------------------------------

def revision_planner_node(
    state: StudyTutorState
):
    """
    Revision Planner Agent creates a personalized
    study plan based on weak topics.
    """

    student_id = state.get(
        "student_id",
        "student_001"
    )

    available_time = state.get(
        "available_time",
        "7 days"
    )

    result = revision_planner_agent(
        student_id=student_id,
        available_time=available_time
    )

    return {

        "weak_topics": result.get(
            "weak_topics",
            []
        ),

        "revision_plan": result.get(
            "revision_plan",
            ""
        )
    }


# ---------------------------------------------------------
# 9. FINAL NODE
# ---------------------------------------------------------

def final_node(
    state: StudyTutorState
):
    """
    Creates a final response depending on
    the action performed by the tutor.
    """

    action = state.get(
        "action",
        ""
    )

    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    if action == "explain":

        explanation = state.get(
            "explanation",
            ""
        )

        citations = state.get(
            "citations",
            []
        )

        final_response = explanation

        if citations:

            final_response += (
                "\n\nSources:\n"
            )

            for citation in citations:

                final_response += (
                    f"- {citation}\n"
                )

        return {
            "final_response":
                final_response
        }


    # -----------------------------------------------------
    # QUIZ
    # -----------------------------------------------------

    if action == "quiz":

        score = state.get(
            "score"
        )

        feedback = state.get(
            "feedback",
            ""
        )

        # ---------------------------------------------
        # Quiz has not been answered yet.
        # ---------------------------------------------

        if score is None:

            return {
                "final_response": (
                    "Quiz generated successfully. "
                    "Please answer the questions."
                )
            }

        # ---------------------------------------------
        # Quiz has been evaluated.
        # ---------------------------------------------

        return {
            "final_response": (
                f"Quiz completed.\n\n"
                f"Score: {score}%\n\n"
                f"{feedback}"
            )
        }


    # -----------------------------------------------------
    # REVIEW
    # -----------------------------------------------------

    if action == "review":

        weak_topics = state.get(
            "weak_topics",
            []
        )

        if not weak_topics:

            return {
                "final_response": (
                    "No quiz history is available yet."
                )
            }

        response = (
            "Your current weak topics:\n\n"
        )

        for item in weak_topics:

            response += (
                f"- {item['topic']}: "
                f"{item['average_score']}% "
                f"average score "
                f"({item['attempts']} attempts)\n"
            )

        return {
            "final_response":
                response
        }


    # -----------------------------------------------------
    # REVISION PLAN
    # -----------------------------------------------------

    if action == "plan":

        revision_plan = state.get(
            "revision_plan",
            ""
        )

        return {
            "final_response":
                revision_plan
        }


    # -----------------------------------------------------
    # DEFAULT
    # -----------------------------------------------------

    return {
        "final_response": (
            "The study tutor completed the request."
        )
    }


# ---------------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# ---------------------------------------------------------

def build_workflow():

    workflow = StateGraph(
        StudyTutorState
    )


    # -----------------------------------------------------
    # ADD NODES
    # -----------------------------------------------------

    workflow.add_node(
        "planner",
        planner_node
    )

    workflow.add_node(
        "explainer",
        explainer_node
    )

    workflow.add_node(
        "adaptive_explainer",
        adaptive_explainer_node
    )

    workflow.add_node(
        "quiz_master",
        quiz_master_node
    )

    workflow.add_node(
        "quiz_ready",
        quiz_ready_node
    )

    workflow.add_node(
        "evaluator",
        evaluator_node
    )

    workflow.add_node(
        "review",
        review_node
    )

    workflow.add_node(
        "revision_planner",
        revision_planner_node
    )

    workflow.add_node(
        "final",
        final_node
    )


    # -----------------------------------------------------
    # START → PLANNER
    # -----------------------------------------------------

    workflow.add_edge(
        START,
        "planner"
    )


    # -----------------------------------------------------
    # PLANNER → CONDITIONAL ROUTING
    # -----------------------------------------------------

    workflow.add_conditional_edges(

        "planner",

        route_after_planner,

        {
            "explainer":
                "explainer",

            "quiz_master":
                "quiz_master",

            "evaluator":
                "evaluator",

            "review":
                "review",

            "revision_planner":
                "revision_planner"
        }
    )


    # -----------------------------------------------------
    # EXPLAINER → FINAL
    # -----------------------------------------------------

    workflow.add_edge(
        "explainer",
        "final"
    )


    # -----------------------------------------------------
    # QUIZ MASTER → CONDITIONAL ROUTING
    # -----------------------------------------------------

    workflow.add_conditional_edges(

        "quiz_master",

        route_after_quiz_master,

        {
            "evaluator":
                "evaluator",

            "quiz_ready":
                "quiz_ready"
        }
    )


    # -----------------------------------------------------
    # QUIZ READY → FINAL
    # -----------------------------------------------------

    workflow.add_edge(
        "quiz_ready",
        "final"
    )


    # -----------------------------------------------------
    # EVALUATOR → ADAPTIVE ROUTING
    # -----------------------------------------------------

    workflow.add_conditional_edges(

        "evaluator",

        route_after_evaluator,

        {
            "adaptive_explainer":
                "adaptive_explainer",

            "finish":
                "final"
        }
    )


    # -----------------------------------------------------
    # ADAPTIVE EXPLAINER → QUIZ MASTER
    # -----------------------------------------------------

    workflow.add_edge(
        "adaptive_explainer",
        "quiz_master"
    )


    # -----------------------------------------------------
    # REVIEW → FINAL
    # -----------------------------------------------------

    workflow.add_edge(
        "review",
        "final"
    )


    # -----------------------------------------------------
    # REVISION PLANNER → FINAL
    # -----------------------------------------------------

    workflow.add_edge(
        "revision_planner",
        "final"
    )


    # -----------------------------------------------------
    # FINAL → END
    # -----------------------------------------------------

    workflow.add_edge(
        "final",
        END
    )


    # -----------------------------------------------------
    # COMPILE
    # -----------------------------------------------------

    return workflow.compile()


# ---------------------------------------------------------
# CREATE WORKFLOW
# ---------------------------------------------------------

study_tutor_workflow = build_workflow()


# ---------------------------------------------------------
# TEST WORKFLOW CONFIGURATION
# ---------------------------------------------------------

if __name__ == "__main__":

    print(
        "\n"
        "============================================"
    )

    print(
        "\nAdaptive Study Tutor"
    )

    print(
        "LangGraph Workflow"
    )

    print(
        "\n============================================"
    )

    print(
        "\nWorkflow compiled successfully!"
    )

    print(
        "\nAvailable workflow nodes:"
    )

    print(
        "- planner"
    )

    print(
        "- explainer"
    )

    print(
        "- adaptive_explainer"
    )

    print(
        "- quiz_master"
    )

    print(
        "- quiz_ready"
    )

    print(
        "- evaluator"
    )

    print(
        "- review"
    )

    print(
        "- revision_planner"
    )

    print(
        "- final"
    )

    print(
        "\nAdaptive learning flow:"
    )

    print(
        "Planner"
        " → Quiz Master"
        " → Evaluator"
    )

    print(
        "Evaluator"
        " → Low Score"
        " → Adaptive Explainer"
        " → New Quiz"
    )

    print(
        "Evaluator"
        " → Mastery"
        " → Final"
    )

    print(
        "\nEvaluation flow:"
    )

    print(
        "Existing Quiz + Student Answers"
        " → Planner"
        " → Evaluator"
    )

    print(
        "\nMaximum adaptive iterations: 3"
    )

    print(
        "\n============================================"
    )