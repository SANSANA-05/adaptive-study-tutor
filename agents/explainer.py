import os
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import retrieve_documents
from agents.react_agent import run_react_agent
from agents.guardrails import check_educational_request


load_dotenv()


LOCAL_MODE = os.getenv(
    "LOCAL_MODE",
    "true"
).lower() == "true"


# ============================================================
# GEMINI
# ============================================================

def create_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        temperature=0
    )


# ============================================================
# TOPIC WORDS
# ============================================================

def get_topic_words(topic: str):
    """
    Convert the topic into useful search words.
    """

    stop_words = {
        "the",
        "a",
        "an",
        "of",
        "and",
        "or",
        "with",
        "about",
        "explain",
        "explanation",
        "example",
        "law",
        "laws",
        "what",
        "is",
        "are",
        "me",
        "please",
    }

    words = re.findall(
        r"[a-zA-Z]+",
        topic.lower()
    )

    return {
        word
        for word in words
        if word not in stop_words and len(word) > 2
    }


# ============================================================
# FILTER RELEVANT DOCUMENTS
# ============================================================

def filter_relevant_documents(
    documents,
    topic: str
):
    """
    Keep only documents that contain enough
    words related to the requested topic.
    """

    topic_words = get_topic_words(topic)

    if not topic_words:
        return documents

    relevant_documents = []

    for document in documents:

        text = document.page_content.lower()

        matches = sum(
            1
            for word in topic_words
            if word in text
        )

        relevance_ratio = (
            matches / len(topic_words)
        )

        if relevance_ratio >= 0.50:
            relevant_documents.append(
                document
            )

    return relevant_documents


# ============================================================
# TEXTBOOK SUFFICIENCY
# ============================================================

def is_textbook_sufficient(
    documents,
    topic: str
):
    """
    Decide whether the textbook contains enough
    relevant information to answer the question.
    """

    if len(documents) < 2:
        return False

    relevant_documents = filter_relevant_documents(
        documents,
        topic
    )

    if len(relevant_documents) < 2:
        return False

    combined_text = "\n".join(
        document.page_content
        for document in relevant_documents[:3]
    )

    if len(combined_text) < 1800:
        return False

    return True


# ============================================================
# CITATIONS
# ============================================================

def build_textbook_citations(
    documents
):
    """
    Build unique textbook citations.
    """

    citations = []

    for document in documents:

        source = document.metadata.get(
            "source",
            "Unknown source"
        )

        page = document.metadata.get(
            "page"
        )

        if page is not None:
            citation = (
                f"{source}, page {page + 1}"
            )
        else:
            citation = source

        if citation not in citations:
            citations.append(
                citation
            )

    return citations


# ============================================================
# CLEAN TEXTBOOK CONTENT
# ============================================================

def clean_text(text: str):
    """
    Clean PDF extraction artifacts and excessive whitespace.
    """

    if not text:
        return ""

    # Fix common PDF hyphenation
    text = re.sub(
        r"(\w)-\s+(\w)",
        r"\1\2",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Normalize excessive newlines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# REMOVE PDF ARTIFACTS
# ============================================================

def remove_pdf_artifacts(text: str):
    """
    Remove common PDF extraction artifacts such as
    section headings, page numbers and broken fragments.
    """

    if not text:
        return ""

    # Remove common section headings such as:
    # 4.6 NEWTON'S THIRD LAW OF MOTION
    text = re.sub(
        r"\b\d+\.\d+\s+[A-Z][A-Z\s'\u00e2\u20ac\u2122\-]+",
        "",
        text
    )

    # Remove page markers
    text = re.sub(
        r"\bPage\s+\d+\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove isolated page numbers
    text = re.sub(
        r"(?m)^\s*\d+\s*$",
        "",
        text
    )

    # Remove repeated whitespace
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# LOCAL EXPLANATION
# ============================================================

def build_local_explanation(
    topic: str,
    documents
):
    """
    Create a clean student-friendly explanation
    from retrieved textbook material.

    This local implementation does not use Gemini.
    """

    relevant_documents = filter_relevant_documents(
        documents,
        topic
    )

    if not relevant_documents:

        return (
            f"### Explanation: {topic}\n\n"
            "The available textbook material does not "
            "contain enough relevant information to "
            "provide a grounded explanation."
        )

    sections = []

    for document in relevant_documents[:3]:

        text = clean_text(
            document.page_content
        )

        text = remove_pdf_artifacts(
            text
        )

        if text:
            sections.append(
                text
            )

    combined_text = "\n\n".join(
        sections
    )

    if not combined_text:

        return (
            f"### Explanation: {topic}\n\n"
            "Relevant textbook content was found, "
            "but readable text could not be extracted."
        )

    # --------------------------------------------------------
    # Split into sentences
    # --------------------------------------------------------

    sentences = re.split(
        r"(?<=[.!?])\s+",
        combined_text
    )

    topic_words = get_topic_words(
        topic
    )

    useful_sentences = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_words = set(
            re.findall(
                r"[a-zA-Z]+",
                sentence.lower()
            )
        )

        overlap = len(
            sentence_words.intersection(
                topic_words
            )
        )

        if overlap > 0:

            useful_sentences.append(
                sentence
            )

    # --------------------------------------------------------
    # Select relevant sentences
    # --------------------------------------------------------

    if useful_sentences:

        selected_sentences = (
            useful_sentences[:15]
        )

        selected_text = " ".join(
            selected_sentences
        )

    else:

        selected_text = combined_text[:5000]

    # --------------------------------------------------------
    # Final student-friendly output
    # --------------------------------------------------------

    return (
        f"### Explanation: {topic}\n\n"
        f"{selected_text}\n\n"
        "### Key Point\n\n"
        "Focus on the definition, the relationship "
        "between the concepts, and the examples "
        "provided in the textbook."
    )


# ============================================================
# LOCAL EXPLANATION + WEB
# ============================================================

def local_explanation_with_web(
    topic: str,
    documents
):
    """
    Use textbook material when sufficient.

    If textbook material is insufficient,
    use Tavily through the ReAct agent.
    """

    relevant_documents = filter_relevant_documents(
        documents,
        topic
    )

    if is_textbook_sufficient(
        relevant_documents,
        topic
    ):

        explanation = build_local_explanation(
            topic,
            relevant_documents
        )

        return {
            "explanation": explanation,
            "citations": build_textbook_citations(
                relevant_documents
            ),
            "used_web_search": False
        }

    # --------------------------------------------------------
    # Textbook insufficient → Web research
    # --------------------------------------------------------

    research_result = run_react_agent(
        topic,
        max_iterations=2
    )

    messages = research_result.get(
        "messages",
        []
    )

    web_text = ""

    if messages:

        last_message = messages[-1]

        if isinstance(
            last_message,
            dict
        ):

            web_text = last_message.get(
                "content",
                ""
            )

        else:

            web_text = getattr(
                last_message,
                "content",
                ""
            )

    if not web_text:

        web_text = (
            "No supplementary web information "
            "was found."
        )

    return {
        "explanation": (
            f"### Explanation: {topic}\n\n"
            f"{web_text}"
        ),
        "citations": [],
        "used_web_search": True
    }


# ============================================================
# ADAPTIVE CONTEXT
# ============================================================

def build_adaptive_context(
    question=None,
    student_answer=None,
    correct_answer=None
):
    """
    Build adaptive feedback only when an actual
    student answer and correct answer are available.

    Therefore, normal Learn requests will not show
    adaptive feedback.
    """

    if (
        not question
        or student_answer is None
        or correct_answer is None
    ):
        return ""

    return (
        "\n\n### Adaptive Feedback\n\n"
        "The student previously answered this "
        "question incorrectly:\n\n"
        f"Question: {question}\n\n"
        f"Student answer: {student_answer}\n\n"
        f"Correct answer: {correct_answer}\n\n"
        "Focus the explanation on helping the "
        "student understand this specific mistake."
    )


# ============================================================
# EXPLAINER AGENT
# ============================================================

def explainer_agent(
    topic: str,
    question=None,
    student_answer=None,
    correct_answer=None
):
    """
    Main Explainer Agent.

    Flow:

    Student question
        ↓
    Educational guardrail
        ↓
    RAG retrieval
        ↓
    Relevant document filtering
        ↓
    Textbook explanation
        ↓
    Tavily fallback if necessary
    """

    # ========================================================
    # EDUCATIONAL REQUEST GUARDRAIL
    # ========================================================

    request_text = question or topic

    guardrail_result = check_educational_request(
        request_text
    )

    if not guardrail_result["allowed"]:

        return {
            "explanation": (
                "### Request Guardrail\n\n"
                f"{guardrail_result['reason']}"
            ),
            "citations": [],
            "used_web_search": False
        }

    # ========================================================
    # BUILD RETRIEVAL QUERY
    # ========================================================

    query = topic

    if question:

        query = (
            f"{topic} {question}"
        )

    # ========================================================
    # RAG RETRIEVAL
    # ========================================================

    documents = retrieve_documents(
        query
    )

    # ========================================================
    # LOCAL MODE
    # ========================================================

    if LOCAL_MODE:

        result = local_explanation_with_web(
            topic,
            documents
        )

        adaptive_context = build_adaptive_context(
            question=question,
            student_answer=student_answer,
            correct_answer=correct_answer
        )

        if adaptive_context:

            result["explanation"] += (
                adaptive_context
            )

        return result

    # ========================================================
    # GEMINI MODE
    # ========================================================

    relevant_documents = filter_relevant_documents(
        documents,
        topic
    )

    textbook_context = "\n\n".join(
        document.page_content
        for document in relevant_documents[:5]
    )

    citations = build_textbook_citations(
        relevant_documents
    )

    adaptive_context = build_adaptive_context(
        question=question,
        student_answer=student_answer,
        correct_answer=correct_answer
    )

    llm = create_gemini_llm()

    prompt = f"""
You are the Explainer Agent of an Adaptive Study Tutor.

Explain the requested topic in a clear,
student-friendly way.

Topic:
{topic}

Student request:
{question or topic}

Use the following textbook material as the
primary source:

{textbook_context}

Requirements:

1. Explain the concept clearly.
2. Use simple language.
3. Give an example when appropriate.
4. Stay grounded in the supplied textbook.
5. Do not invent unsupported facts.
6. Do not expose raw PDF extraction artifacts.
7. Do not mention the internal RAG implementation.
8. Organize the explanation with useful headings.
9. If adaptive feedback is provided, focus on
   the student's misunderstanding.

Adaptive context:

{adaptive_context}
"""

    response = llm.invoke(
        prompt
    )

    explanation = response.content

    return {
        "explanation": explanation,
        "citations": citations,
        "used_web_search": False
    }


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("\n============================================")
    print("Adaptive Study Tutor - Explainer Agent")
    print("============================================")

    result = explainer_agent(
        topic="Newton's third law",
        question=(
            "Explain Newton's third law "
            "with an example."
        )
    )

    print("\nExplanation:\n")

    print(
        result.get(
            "explanation",
            ""
        )
    )

    print("\nCitations:")

    for citation in result.get(
        "citations",
        []
    ):

        print(
            f"- {citation}"
        )

    print(
        "\nWeb search used:",
        result.get(
            "used_web_search",
            False
        )
    )

    print("\n============================================")