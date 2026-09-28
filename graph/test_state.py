from state import StudyTutorState


if __name__ == "__main__":

    state: StudyTutorState = {
        "student_id": "student_001",
        "user_query": "Explain Newton's third law.",
        "action": "explain",
        "topic": "Newton's Laws of Motion",
        "iteration": 0,
        "max_iterations": 3,
        "mastery_threshold": 70.0
    }

    print("\nShared state created successfully!\n")

    print("Student ID:", state["student_id"])
    print("User Query:", state["user_query"])
    print("Action:", state["action"])
    print("Topic:", state["topic"])
    print("Iteration:", state["iteration"])
    print("Max Iterations:", state["max_iterations"])
    print("Mastery Threshold:", state["mastery_threshold"])