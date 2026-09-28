from typing import Any, Dict, List, TypedDict


class StudyTutorState(TypedDict, total=False):

    # -----------------------------
    # Student information
    # -----------------------------
    student_id: str
    user_query: str

    # -----------------------------
    # Planner information
    # -----------------------------
    action: str
    topic: str

    # -----------------------------
    # Explainer / RAG information
    # -----------------------------
    explanation: str
    citations: List[str]
    used_web_search: bool

    # -----------------------------
    # Quiz information
    # -----------------------------
    quiz: List[Dict[str, Any]]
    student_answers: List[str]

    # -----------------------------
    # Evaluation information
    # -----------------------------
    score: float
    correct_count: int
    total_questions: int

    feedback: str
    evaluation_results: List[Dict[str, Any]]

    # -----------------------------
    # Progress information
    # -----------------------------
    weak_topics: List[Dict[str, Any]]

    # -----------------------------
    # Revision planning
    # -----------------------------
    available_time: str
    revision_plan: str

    # -----------------------------
    # Adaptive loop control
    # -----------------------------
    iteration: int
    max_iterations: int
    mastery_threshold: float

    # -----------------------------
    # Final response
    # -----------------------------
    final_response: str