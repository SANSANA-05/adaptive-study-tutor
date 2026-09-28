import sys
from pathlib import Path

# --------------------------------------------------
# Project Root Setup
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from rag.embeddings import embeddings


# --------------------------------------------------
# Paths
# --------------------------------------------------

KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "knowledge_base"
CHROMA_PATH = str(PROJECT_ROOT / "chroma_db")

COLLECTION_NAME = "study_tutor"


# --------------------------------------------------
# Load All PDF Files
# --------------------------------------------------

def load_all_pdfs():

    print()
    print("=" * 60)
    print("Loading Knowledge Base")
    print("=" * 60)
    print()

    pdf_files = sorted(
        KNOWLEDGE_BASE_PATH.rglob("*.pdf")
    )

    if not pdf_files:

        print("No PDF files found.")
        return []

    all_documents = []

    for pdf_path in pdf_files:

        print(f"Loading: {pdf_path.name}")

        loader = PyPDFLoader(
            str(pdf_path)
        )

        documents = loader.load()

        # Store a clean project-relative source path
        relative_source = pdf_path.relative_to(
            PROJECT_ROOT
        )

        for document in documents:

            document.metadata["source"] = str(
                relative_source
            )

            document.metadata["filename"] = (
                pdf_path.name
            )

        all_documents.extend(documents)

        print(
            f"  Pages loaded: {len(documents)}"
        )

    print()
    print(
        f"Total pages loaded: {len(all_documents)}"
    )

    return all_documents


# --------------------------------------------------
# Split Documents
# --------------------------------------------------

def split_documents(documents):

    print()
    print("=" * 60)
    print("Splitting Documents")
    print("=" * 60)
    print()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Total chunks created: {len(chunks)}"
    )

    return chunks


# --------------------------------------------------
# Rebuild Chroma Database
# --------------------------------------------------

def rebuild_vector_database(chunks):

    print()
    print("=" * 60)
    print("Rebuilding Chroma Vector Database")
    print("=" * 60)
    print()

    # Connect to existing collection
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

    # Delete old collection
    try:

        print("Removing old Chroma collection...")

        vectorstore.delete_collection()

        print("Old collection removed.")

    except Exception:

        print(
            "No existing collection found."
        )


    # Create a fresh collection
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )


    print()
    print("Creating embeddings...")
    print("This may take some time.")
    print()


    # Add all chunks
    vectorstore.add_documents(
        chunks
    )


    print()
    print(
        f"Added {len(chunks)} chunks to Chroma."
    )

    print()
    print(
        "Vector database rebuilt successfully!"
    )


# --------------------------------------------------
# Main Ingestion Pipeline
# --------------------------------------------------

def main():

    print()
    print("=" * 60)
    print("ADAPTIVE STUDY TUTOR - RAG INGESTION")
    print("=" * 60)


    # Step 1
    documents = load_all_pdfs()

    if not documents:
        return


    # Step 2
    chunks = split_documents(
        documents
    )


    # Step 3
    rebuild_vector_database(
        chunks
    )


    print()
    print("=" * 60)
    print("RAG INGESTION COMPLETED")
    print("=" * 60)
    print()


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    main()