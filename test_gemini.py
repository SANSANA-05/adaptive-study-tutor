from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key from .env
load_dotenv()

# Create Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)

# Send a test question
response = llm.invoke(
    "Explain Newton's third law in one simple sentence."
)

print("\nGemini response:")
print(response.content)