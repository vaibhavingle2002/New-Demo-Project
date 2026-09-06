import os
import time

from pinecone import Pinecone, ServerlessSpec


class VectoreDatabase:

    def __init__(self, chunks, model):

        self.chunks = chunks
        self.model = model

        # --------------------------------
        # PINECONE API KEY
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

        # --------------------------------
        # CHECK INDEX
        # --------------------------------

        existing_indexes = [
            index.name
            for index in self.pc.list_indexes()
        ]

        if self.index_name not in existing_indexes:

            print(
                f"Index '{self.index_name}' not found."
            )

            print(
                f"Creating index with dimension {dimension}..."
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

            # Wait until index is ready
            while not self.pc.describe_index(
                self.index_name
            ).status["ready"]:

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


    # --------------------------------
    # STORE VECTORS
    # --------------------------------

    def build_index(self):

        vectors = []

        for i, text in enumerate(
            self.chunks
        ):

            # TEXT → VECTOR

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
        # STORE IN PINECONE
        # --------------------------------

        response = self.index.upsert(
            vectors=vectors
        )

        return response


    # --------------------------------
    # SEARCH
    # --------------------------------

    def Search(
        self,
        question,
        k=2
    ):

        # QUESTION → VECTOR

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
