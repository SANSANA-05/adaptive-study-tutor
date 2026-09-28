from dotenv import load_dotenv
from tavily import TavilyClient
import os

# Load API keys from .env
load_dotenv()

# Get Tavily API key
api_key = os.getenv("TAVILY_API_KEY")

# Create Tavily client
tavily = TavilyClient(api_key=api_key)

# Perform a test search
response = tavily.search(
    query="Newton's third law real world examples",
    max_results=3
)

print("\nTavily search results:\n")

for result in response["results"]:
    print("Title:", result["title"])
    print("URL:", result["url"])
    print()