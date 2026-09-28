import json


# =========================================================
# QUESTION BANKS
# =========================================================

NEWTON_THIRD_LAW_QUESTIONS = [

    {
        "question": "Which law states that every action force has an equal and opposite reaction force?",
        "options": [
            "Newton's first law",
            "Newton's second law",
            "Newton's third law",
            "Law of gravitation"
        ],
        "correct_answer": "Newton's third law",
        "short_explanation": (
            "Newton's third law states that forces occur "
            "in equal and opposite pairs."
        )
    },

    {
        "question": "According to Newton's third law, forces occur in what kind of pairs?",
        "options": [
            "Equal and opposite pairs",
            "Unequal pairs",
            "Parallel pairs",
            "Random pairs"
        ],
        "correct_answer": "Equal and opposite pairs",
        "short_explanation": (
            "The action and reaction forces have equal "
            "magnitude and opposite direction."
        )
    },

    {
        "question": "When a person pushes a wall, what force does the wall exert on the person?",
        "options": [
            "No force",
            "A smaller force",
            "An equal and opposite force",
            "A force in the same direction"
        ],
        "correct_answer": "An equal and opposite force",
        "short_explanation": (
            "The wall exerts a force on the person equal "
            "in magnitude and opposite in direction."
        )
    },

    {
        "question": "Do the action and reaction forces act on the same object or different objects?",
        "options": [
            "The same object",
            "Different objects",
            "Only one object",
            "Neither object"
        ],
        "correct_answer": "Different objects",
        "short_explanation": (
            "The two forces in a Newton's third-law pair "
            "act on two different interacting objects."
        )
    },

    {
        "question": "Are the action and reaction forces simultaneous?",
        "options": [
            "Yes",
            "No",
            "Only sometimes",
            "Only when objects are stationary"
        ],
        "correct_answer": "Yes",
        "short_explanation": (
            "Action and reaction forces arise simultaneously "
            "during an interaction."
        )
    }
]


# =========================================================
# ADAPTIVE QUESTION BANK
# =========================================================
#
# These questions test the same topic using different
# situations and reasoning.
#
# They are used after the student performs poorly on
# the first quiz.
# =========================================================

NEWTON_THIRD_LAW_ADAPTIVE_QUESTIONS = [

    {
        "question": (
            "A swimmer pushes water backward with their hands. "
            "According to Newton's third law, what happens?"
        ),
        "options": [
            "The water pushes the swimmer forward",
            "The water does not exert a force",
            "The water pushes the swimmer backward",
            "Only the swimmer exerts a force"
        ],
        "correct_answer": "The water pushes the swimmer forward",
        "short_explanation": (
            "The swimmer pushes water backward, and the water "
            "exerts an equal and opposite force on the swimmer."
        )
    },

    {
        "question": (
            "A person jumps upward from the ground. "
            "Which force pair represents Newton's third law?"
        ),
        "options": [
            "Person's weight and gravity",
            "Person pushes ground downward and ground pushes person upward",
            "Person's weight and normal force",
            "Air resistance and weight"
        ],
        "correct_answer": (
            "Person pushes ground downward and ground pushes person upward"
        ),
        "short_explanation": (
            "The person exerts a downward force on the ground, "
            "and the ground exerts an equal and opposite upward force."
        )
    },

    {
        "question": (
            "A rocket pushes gases downward during launch. "
            "What is the reaction force?"
        ),
        "options": [
            "The gases push the rocket upward",
            "Gravity pushes the rocket upward",
            "The rocket pulls the gases upward",
            "There is no reaction force"
        ],
        "correct_answer": "The gases push the rocket upward",
        "short_explanation": (
            "The rocket pushes gases downward, while the gases "
            "exert an equal and opposite force on the rocket."
        )
    },

    {
        "question": (
            "A book rests on a table. Which pair is a Newton's "
            "third-law action-reaction pair?"
        ),
        "options": [
            "Book's weight and table's normal force",
            "Book pushes table downward and table pushes book upward",
            "Gravity and friction",
            "Book's weight and friction"
        ],
        "correct_answer": (
            "Book pushes table downward and table pushes book upward"
        ),
        "short_explanation": (
            "The book exerts a downward force on the table, and "
            "the table exerts an equal and opposite force on the book."
        )
    },

    {
        "question": (
            "Two students push against each other's hands. "
            "If Student A pushes Student B, what does Student B do?"
        ),
        "options": [
            "Student B exerts no force",
            "Student B exerts an equal and opposite force on Student A",
            "Student B always exerts a larger force",
            "Student B exerts a force in the same direction"
        ],
        "correct_answer": (
            "Student B exerts an equal and opposite force on Student A"
        ),
        "short_explanation": (
            "The interaction produces equal and opposite forces "
            "on the two different students."
        )
    }
]


# =========================================================
# OTHER NEWTON QUESTION BANKS
# =========================================================

NEWTON_FIRST_LAW_QUESTIONS = [

    {
        "question": "Which law is also called the law of inertia?",
        "options": [
            "Newton's first law",
            "Newton's second law",
            "Newton's third law",
            "Law of gravitation"
        ],
        "correct_answer": "Newton's first law",
        "short_explanation": (
            "Newton's first law is known as the law of inertia."
        )
    },

    {
        "question": "An object at rest remains at rest when the net external force is what?",
        "options": [
            "Zero",
            "Very large",
            "Constantly increasing",
            "Always negative"
        ],
        "correct_answer": "Zero",
        "short_explanation": (
            "With zero net external force, an object at rest "
            "remains at rest."
        )
    },

    {
        "question": "What property describes an object's resistance to changes in motion?",
        "options": [
            "Inertia",
            "Momentum",
            "Acceleration",
            "Velocity"
        ],
        "correct_answer": "Inertia",
        "short_explanation": (
            "Inertia is the tendency of an object to resist "
            "changes in its state of motion."
        )
    },

    {
        "question": "If the net external force on a moving object is zero, the object continues with what motion?",
        "options": [
            "Constant velocity",
            "Increasing velocity",
            "Decreasing velocity",
            "Circular acceleration"
        ],
        "correct_answer": "Constant velocity",
        "short_explanation": (
            "With zero net force, a moving object continues "
            "with constant velocity."
        )
    },

    {
        "question": "Which quantity is related to an object's inertia?",
        "options": [
            "Mass",
            "Temperature",
            "Pressure",
            "Time"
        ],
        "correct_answer": "Mass",
        "short_explanation": (
            "Greater mass means greater resistance to changes "
            "in motion."
        )
    }
]


NEWTON_SECOND_LAW_QUESTIONS = [

    {
        "question": "What equation represents Newton's second law?",
        "options": [
            "F = ma",
            "F = m/a",
            "F = a/m",
            "F = m + a"
        ],
        "correct_answer": "F = ma",
        "short_explanation": (
            "Newton's second law relates net force, mass, "
            "and acceleration as F = ma."
        )
    },

    {
        "question": "If the net force on an object increases while mass stays constant, what happens to acceleration?",
        "options": [
            "It increases",
            "It decreases",
            "It becomes zero",
            "It remains unchanged"
        ],
        "correct_answer": "It increases",
        "short_explanation": (
            "For constant mass, acceleration increases when "
            "net force increases."
        )
    },

    {
        "question": "If mass increases while net force stays constant, what happens to acceleration?",
        "options": [
            "It increases",
            "It decreases",
            "It becomes infinite",
            "It remains unchanged"
        ],
        "correct_answer": "It decreases",
        "short_explanation": (
            "For constant force, greater mass produces smaller acceleration."
        )
    },

    {
        "question": "What is the SI unit of force?",
        "options": [
            "Newton",
            "Joule",
            "Watt",
            "Pascal"
        ],
        "correct_answer": "Newton",
        "short_explanation": (
            "The SI unit of force is the newton (N)."
        )
    },

    {
        "question": "A 2 kg object experiences a net force of 10 N. What is its acceleration?",
        "options": [
            "5 m/s²",
            "20 m/s²",
            "0.2 m/s²",
            "12 m/s²"
        ],
        "correct_answer": "5 m/s²",
        "short_explanation": (
            "Using F = ma, acceleration = 10 / 2 = 5 m/s²."
        )
    }
]


# =========================================================
# GENERAL NEWTON QUESTIONS
# =========================================================

NEWTON_LAWS_QUESTIONS = (

    NEWTON_FIRST_LAW_QUESTIONS
    + NEWTON_SECOND_LAW_QUESTIONS
    + NEWTON_THIRD_LAW_QUESTIONS
)


# =========================================================
# GENERATE QUIZ
# =========================================================

def generate_quiz(
    topic: str,
    num_questions: int = 5,
    difficulty: str = "medium",
    attempt: int = 0
):
    """
    Generate a focused multiple-choice quiz.

    Parameters
    ----------
    topic:
        Topic for the quiz.

    num_questions:
        Number of questions requested.

    difficulty:
        Quiz difficulty.

    attempt:
        Adaptive attempt number.

        attempt = 0
            First quiz.

        attempt > 0
            Adaptive quiz using different questions.
    """

    topic_lower = topic.lower().strip()

    # -----------------------------------------------------
    # Select question bank
    # -----------------------------------------------------

    if (
        "newton" in topic_lower
        and "third" in topic_lower
    ):

        if attempt > 0:

            questions = (
                NEWTON_THIRD_LAW_ADAPTIVE_QUESTIONS.copy()
            )

        else:

            questions = (
                NEWTON_THIRD_LAW_QUESTIONS.copy()
            )

    elif (
        "newton" in topic_lower
        and "first" in topic_lower
    ):

        questions = (
            NEWTON_FIRST_LAW_QUESTIONS.copy()
        )

    elif (
        "newton" in topic_lower
        and "second" in topic_lower
    ):

        questions = (
            NEWTON_SECOND_LAW_QUESTIONS.copy()
        )

    elif (
        "newton" in topic_lower
        and "law" in topic_lower
    ):

        questions = (
            NEWTON_LAWS_QUESTIONS.copy()
        )

    else:

        questions = [

            {
                "question": (
                    f"What is an important concept in {topic}?"
                ),
                "options": [
                    f"Understanding {topic}",
                    "Ignoring the topic",
                    "Avoiding practice",
                    "Skipping the topic"
                ],
                "correct_answer":
                    f"Understanding {topic}",
                "short_explanation": (
                    f"Understanding the key concepts of "
                    f"{topic} is important for learning."
                )
            },

            {
                "question": (
                    f"Why is studying {topic} useful?"
                ),
                "options": [
                    "It helps understand the subject",
                    "It prevents learning",
                    "It removes the need for practice",
                    "It makes revision unnecessary"
                ],
                "correct_answer":
                    "It helps understand the subject",
                "short_explanation": (
                    f"Studying {topic} helps build understanding "
                    f"of the subject."
                )
            }
        ]

    # -----------------------------------------------------
    # Validate number of questions
    # -----------------------------------------------------

    try:

        num_questions = int(
            num_questions
        )

    except (
        TypeError,
        ValueError
    ):

        num_questions = 5

    if num_questions < 1:

        num_questions = 1

    # -----------------------------------------------------
    # Limit to available questions
    # -----------------------------------------------------

    questions = questions[
        :num_questions
    ]

    # -----------------------------------------------------
    # Add question metadata
    # -----------------------------------------------------

    for index, question in enumerate(
        questions,
        start=1
    ):

        question["id"] = index

        question["question_number"] = index

        question["difficulty"] = difficulty

        question["attempt"] = attempt

    # -----------------------------------------------------
    # Return JSON
    # -----------------------------------------------------

    return json.dumps(

        {
            "topic":
                topic,

            "difficulty":
                difficulty,

            "attempt":
                attempt,

            "num_questions":
                len(questions),

            "questions":
                questions
        },

        indent=2
    )