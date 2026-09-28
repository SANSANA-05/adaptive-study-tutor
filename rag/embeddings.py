from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings


class LocalEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def embed_documents(self, texts):
        return self.model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    def embed_query(self, text):
        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()


embeddings = LocalEmbeddings()


# Test the embedding model
if __name__ == "__main__":
    text = "Newton's third law states that every action has an equal and opposite reaction."

    vector = embeddings.embed_query(text)

    print("Local embedding created successfully!")
    print("Vector length:", len(vector))
    print("First 5 values:", vector[:5])