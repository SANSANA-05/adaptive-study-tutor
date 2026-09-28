import re


# ============================================================
# PROJECT GUARDRAIL PATTERNS
# ============================================================

# This is intentionally a small, deterministic filter.
# It is designed for the educational tutor project,
# not as a complete safety classifier.

INAPPROPRIATE_PATTERNS = [
    r"\bsexually explicit\b",
    r"\bsexual content\b",
    r"\bporn\b",
    r"\bpornography\b",
    r"\bnudity\b",
    r"\bgraphic violence\b",
]


QUIZ_ANSWER_PATTERNS = [
    r"\bwhat('?s| is) the answer\b",
    r"\bgive me the answer\b",
    r"\btell me the answer\b",
    r"\bshow me the answer\b",
    r"\bwhat should i choose\b",
    r"\bwhich option is correct\b",
    r"\bwhich answer is correct\b",
]


# ============================================================
# INTERNAL MATCHING
# ============================================================

def _matches_any(
    text: str,
    patterns
):
    """
    Check whether text matches any supplied pattern.
    """

    if not text:
        return False

    normalized_text = text.lower().strip()

    return any(
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE
        )
        for pattern in patterns
    )


# ============================================================
# EDUCATIONAL REQUEST GUARDRAIL
# ============================================================

def check_educational_request(
    text: str
):
    """
    Validate whether a user request is appropriate
    for the educational tutor.

    Returns:
        {
            "allowed": bool,
            "reason": str
        }
    """

    if not text or not text.strip():

        return {
            "allowed": False,
            "reason": (
                "Please enter an educational "
                "question or topic."
            )
        }

    if _matches_any(
        text,
        INAPPROPRIATE_PATTERNS
    ):

        return {
            "allowed": False,
            "reason": (
                "I can help with age-appropriate "
                "educational topics only."
            )
        }

    return {
        "allowed": True,
        "reason": ""
    }


# ============================================================
# QUIZ ANSWER REQUEST DETECTION
# ============================================================

def is_quiz_answer_request(
    text: str
):
    """
    Detect requests that attempt to obtain the
    answer to an active quiz before submission.
    """

    return _matches_any(
        text,
        QUIZ_ANSWER_PATTERNS
    )


# ============================================================
# QUIZ ANSWER GUARDRAIL MESSAGE
# ============================================================

def quiz_guardrail_message():
    """
    Message shown when a student asks for the answer
    before completing a quiz.
    """

    return (
        "I won't reveal the answer before you submit "
        "your quiz response. Try the question first. "
        "After submission, I'll explain the result "
        "and help you understand any mistake."
    )


# ============================================================
# STUDENT-FACING QUIZ SANITIZATION
# ============================================================

def sanitize_quiz_for_student(
    quiz
):
    """
    Remove answer-only fields before quiz questions
    are presented to the student.

    The original quiz remains available internally
    for the Evaluator Agent.
    """

    student_quiz = []

    for question in quiz:

        item = dict(question)

        # Never expose these fields in the
        # student-facing quiz.
        item.pop(
            "correct_answer",
            None
        )

        item.pop(
            "explanation",
            None
        )

        student_quiz.append(
            item
        )

    return student_quiz


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print(
        "Educational request:"
    )

    print(
        check_educational_request(
            "Explain Newton's third law"
        )
    )

    print(
        "\nInappropriate request:"
    )

    print(
        check_educational_request(
            "Tell me something sexually explicit"
        )
    )

    print(
        "\nQuiz answer request:"
    )

    print(
        is_quiz_answer_request(
            "What is the answer?"
        )
    )

    print(
        "\nQuiz guardrail message:"
    )

    print(
        quiz_guardrail_message()
    )