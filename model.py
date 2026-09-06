from sentence_transformers import SentenceTransformer


class HuggingEmbedding:

    def __init__(self):

        self.model = None


    def embedding_model(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        return self.model


    def encode(self, text):

        return self.model.encode(
            text,
            normalize_embeddings=True
        )


if __name__ == "__main__":

    model = HuggingEmbedding()

    print(
        "Embedding model loaded successfully."
    )