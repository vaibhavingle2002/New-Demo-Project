import os

from pinecone import Pinecone


class VectoreDatabase:

    def __init__(self, chunks, model):

        self.chunks = chunks

        self.model = model

        api_key = os.getenv(
            "PINECONE_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "PINECONE_API_KEY is not set."
            )

        self.pc = Pinecone(
            api_key=api_key
        )

        self.index = self.pc.Index(
            "sentence-transformer-index"
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


        # STORE IN PINECONE

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


        # PINECONE SEARCH

        results = self.index.query(

            vector=query_vector.tolist(),

            top_k=k,

            include_metadata=True

        )

        return results