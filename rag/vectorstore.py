from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embeddings import embeddings


# --------------------------------------------------
# Paths
# --------------------------------------------------

PDF_PATH = Path("knowledge_base/physics/Chapter-1.pdf")
CHROMA_PATH = "chroma_db"


# --------------------------------------------------
# Load and split PDF
# --------------------------------------------------

loader = PyPDFLoader(str(PDF_PATH))
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print(f"Loaded {len(documents)} pages")
print(f"Created {len(chunks)} chunks")


# --------------------------------------------------
# Create ChromaDB vector store
# --------------------------------------------------

vectorstore = Chroma(
    collection_name="study_tutor",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)


# --------------------------------------------------
# Add chunks to ChromaDB
# --------------------------------------------------

vectorstore.add_documents(chunks)

print("\nChunks successfully stored in ChromaDB!")
print(f"ChromaDB location: {CHROMA_PATH}")