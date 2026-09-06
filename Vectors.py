import os
import time

from pinecone import Pinecone, ServerlessSpec


class VectoreDatabase:

    def __init__(self, chunks, model):

        self.chunks = chunks
        self.model = model

        # --------------------------------
        # GET PINECONE API KEY
        # --------------------------------

        api_key = os.getenv("PINECONE_API_KEY")

        if not api_key:
            raise ValueError(
                "PINECONE_API_KEY is not set."
            )

        # --------------------------------
        # CONNECT TO PINECONE
        # --------------------------------

        self.pc = Pinecone(
            api_key=api_key
        )

        self.index_name = "sentence-transformer-index"

        # --------------------------------
        # GET EMBEDDING DIMENSION
        # --------------------------------

        test_embedding = self.model.encode(
            "test"
        )

        dimension = len(test_embedding)

        print(
            f"Embedding dimension: {dimension}"
        )

        # --------------------------------
        # CHECK PINECONE INDEX
        # --------------------------------

        existing_indexes = [
            index.name
            for index in self.pc.list_indexes()
        ]

        print(
            f"Existing Pinecone indexes: {existing_indexes}"
        )

        # --------------------------------
        # CREATE INDEX IF NOT EXISTS
        # --------------------------------

        if self.index_name not in existing_indexes:

            print(
                f"Index '{self.index_name}' does not exist."
            )

            print(
                f"Creating Pinecone index with dimension {dimension}..."
            )

            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )

            print(
                "Pinecone index creation started."
            )

            # --------------------------------
            # WAIT FOR INDEX
            # --------------------------------

            while True:

                index_description = (
                    self.pc.describe_index(
                        self.index_name
                    )
                )

                if index_description.status["ready"]:

                    print(
                        "Pinecone index is ready."
                    )

                    break

                print(
                    "Waiting for Pinecone index..."
                )

                time.sleep(2)

        else:

            print(
                f"Index '{self.index_name}' already exists."
            )

        # --------------------------------
        # CONNECT TO INDEX
        # --------------------------------

        self.index = self.pc.Index(
            self.index_name
        )

        print(
            f"Connected to Pinecone index: {self.index_name}"
        )


    # ================================================
    # STORE VECTORS
    # ================================================

    def build_index(self):

        vectors = []

        for i, text in enumerate(
            self.chunks
        ):

            # --------------------------------
            # TEXT → VECTOR
            # --------------------------------

            embedding = self.model.encode(
                text
            )

            vectors.append({

                "id": f"vector-{i}",

                "values": embedding.tolist(),

                "metadata": {

                    "content": text

                }

            })

        # --------------------------------
        # UPLOAD VECTORS TO PINECONE
        # --------------------------------

        response = self.index.upsert(
            vectors=vectors
        )

        print(
            f"Uploaded {len(vectors)} vectors to Pinecone."
        )

        return response


    # ================================================
    # SEARCH
    # ================================================

    def Search(
        self,
        question,
        k=2
    ):

        # --------------------------------
        # QUESTION → VECTOR
        # --------------------------------

        query_vector = self.model.encode(
            question
        )

        # --------------------------------
        # SEARCH PINECONE
        # --------------------------------

        results = self.index.query(

            vector=query_vector.tolist(),

            top_k=k,

            include_metadata=True

        )

        return results
