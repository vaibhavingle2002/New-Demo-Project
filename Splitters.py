class RecursiveSplitter:

    def __init__(
        self,
        texts,
        chunk_size=300,
        overlap=50
    ):

        self.texts = texts
        self.chunk_size = chunk_size
        self.overlap = overlap


    def split(self):

        chunks = []

        for text in self.texts:

            start = 0

            while start < len(text):

                end = start + self.chunk_size

                chunk = text[start:end]

                if chunk.strip():

                    chunks.append(chunk)

                start = end - self.overlap

        return chunks


if __name__ == "__main__":

    print(
        "PDF text splitter is ready."
    )
