import sys
from pathlib import Path
from typing import List

# --------------------------------------------------
# Project Root Setup
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from langchain_core.documents import Document
from langchain_chroma import Chroma

from rag.embeddings import embeddings


# --------------------------------------------------
# Chroma Configuration
# --------------------------------------------------

CHROMA_PATH = str(PROJECT_ROOT / "chroma_db")

vectorstore = Chroma(
    collection_name="study_tutor",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)


# --------------------------------------------------
# Topic-Specific Keywords
# --------------------------------------------------

TOPIC_KEYWORDS = {

    "newton's third law": [
        "newton's third law",
        "third law of motion",
        "action and reaction",
        "equal and opposite",
        "action reaction"
    ],

    "newton's first law": [
        "newton's first law",
        "first law of motion",
        "law of inertia",
        "inertia"
    ],

    "newton's second law": [
        "newton's second law",
        "second law of motion",
        "force",
        "mass",
        "acceleration",
        "f = ma"
    ],

    "newton's laws of motion": [
        "newton's laws of motion",
        "first law of motion",
        "second law of motion",
        "third law of motion",
        "law of inertia",
        "action and reaction"
    ],

    "photosynthesis": [
        "photosynthesis",
        "chlorophyll",
        "carbon dioxide",
        "glucose",
        "oxygen",
        "light reaction"
    ]
}


# --------------------------------------------------
# Text Normalization
# --------------------------------------------------

def normalize_text(text: str) -> str:
    """
    Normalize text so that keyword matching
    becomes more reliable.
    """

    return (
        text
        .lower()
        .replace("–", "-")
        .replace("—", "-")
        .replace("’", "'")
    )


# --------------------------------------------------
# Get Relevant Keywords
# --------------------------------------------------

def get_topic_keywords(query: str) -> List[str]:
    """
    Return topic-specific keywords when the query
    matches a known topic.

    Otherwise, extract meaningful words from
    the user's query.
    """

    normalized_query = normalize_text(query)

    # Check predefined topics first
    for topic, keywords in TOPIC_KEYWORDS.items():

        if topic in normalized_query:
            return keywords

    # Generic keyword extraction
    words = normalized_query.split()

    stop_words = {
        "explain",
        "teach",
        "me",
        "about",
        "the",
        "a",
        "an",
        "what",
        "is",
        "are",
        "of",
        "on",
        "please",
        "can",
        "you",
        "tell"
    }

    keywords = [
        word
        for word in words
        if word not in stop_words
        and len(word) > 2
    ]

    return keywords


# --------------------------------------------------
# Calculate Keyword Score
# --------------------------------------------------

def keyword_score(
    document: Document,
    keywords: List[str]
) -> float:
    """
    Calculate how strongly a document matches
    the important keywords.
    """

    text = normalize_text(
        document.page_content
    )

    score = 0.0

    for keyword in keywords:

        keyword = normalize_text(
            keyword
        )

        if keyword in text:

            # Multi-word phrases receive
            # a stronger score.
            if " " in keyword:
                score += 3.0

            else:
                score += 1.0

    return score


# --------------------------------------------------
# Retrieve Documents
# --------------------------------------------------

def retrieve_documents(
    query: str,
    k: int = 4
) -> List[Document]:
    """
    Retrieve the most relevant textbook chunks.

    Retrieval process:

    1. Chroma semantic similarity search
    2. Retrieve additional candidate documents
    3. Apply keyword/topic relevance
    4. Boost exact topic matches
    5. Return the top k documents
    """

    # Retrieve more candidates than we finally need.
    candidate_count = max(k * 4, 12)

    candidates = vectorstore.similarity_search(
        query,
        k=candidate_count
    )

    # No results
    if not candidates:
        return []


    # --------------------------------------------------
    # Get Keywords
    # --------------------------------------------------

    keywords = get_topic_keywords(query)

    normalized_query = normalize_text(query)


    # --------------------------------------------------
    # Rank Candidates
    # --------------------------------------------------

    ranked_documents = []

    for index, document in enumerate(candidates):

        # Keyword relevance
        lexical_score = keyword_score(
            document,
            keywords
        )

        text = normalize_text(
            document.page_content
        )


        # --------------------------------------------------
        # Exact Query Bonus
        # --------------------------------------------------

        exact_match_bonus = 0.0

        if normalized_query in text:
            exact_match_bonus = 10.0


        # --------------------------------------------------
        # Semantic Ranking Bonus
        # --------------------------------------------------

        # Documents appearing earlier in Chroma's
        # similarity results receive a small bonus.
        semantic_bonus = max(
            0.0,
            (candidate_count - index) * 0.01
        )


        # --------------------------------------------------
        # Final Score
        # --------------------------------------------------

        final_score = (
            lexical_score
            + exact_match_bonus
            + semantic_bonus
        )


        ranked_documents.append(
            (
                final_score,
                index,
                document
            )
        )


    # --------------------------------------------------
    # Sort Documents
    # --------------------------------------------------

    ranked_documents.sort(
        key=lambda item: (
            item[0],
            -item[1]
        ),
        reverse=True
    )


    # --------------------------------------------------
    # Select Top K
    # --------------------------------------------------

    results = []

    for _, _, document in ranked_documents[:k]:

        results.append(document)


    return results


# --------------------------------------------------
# Test Retriever
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("RAG Retriever Test")
    print("=" * 60)
    print()

    query = "Newton's third law"

    print(f"Query: {query}")
    print()

    print("Searching textbook...")
    print()

    documents = retrieve_documents(
        query,
        k=4
    )

    print(
        f"Retrieved {len(documents)} documents."
    )

    print()


    # --------------------------------------------------
    # Display Results
    # --------------------------------------------------

    for index, document in enumerate(
        documents,
        start=1
    ):

        print("=" * 60)

        print(
            f"Document {index}"
        )

        source = document.metadata.get(
            "source",
            "Unknown"
        )

        page = document.metadata.get(
            "page"
        )

        print(
            f"Source: {source}"
        )


        if page is not None:

            print(
                f"Page: {page + 1}"
            )


        print()
        print("Content:")

        text = document.page_content.strip()

        if len(text) > 700:

            text = (
                text[:700]
                + "..."
            )

        print(text)

        print()


    print("=" * 60)
    print("RAG retrieval test completed!")
    print("=" * 60)
    print()