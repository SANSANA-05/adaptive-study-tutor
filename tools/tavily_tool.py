import os

from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_core.tools import tool


load_dotenv()


@tool
def web_search(query: str) -> str:
    """
    Search the web for supplementary educational information,
    examples, articles, and videos using Tavily.
    """

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return "TAVILY_API_KEY is not configured."

    tavily = TavilyClient(api_key=api_key)

    response = tavily.search(
        query=query,
        max_results=5
    )

    results = response.get("results", [])

    if not results:
        return "No web search results found."

    output = []

    for index, result in enumerate(results, start=1):

        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "No content")

        output.append(
            f"""
Result {index}

Title: {title}

URL: {url}

Content:
{content}
"""
        )

    return "\n".join(output)


if __name__ == "__main__":

    print("\nTesting Tavily LangChain tool...\n")

    result = web_search.invoke(
        "Newton's third law real world examples"
    )

    print(result)