from datetime import date

from langchain_core.tools import tool


@tool
def get_current_date() -> str:
    """
    Return today's date for study-plan and revision scheduling.
    """

    return date.today().isoformat()


if __name__ == "__main__":

    print("\nTesting date tool...\n")

    result = get_current_date.invoke({})

    print("Current date:", result)