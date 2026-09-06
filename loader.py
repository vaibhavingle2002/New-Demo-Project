from pypdf import PdfReader


class PDFLoader:

    def __init__(self, file_path):

        self.file_path = file_path

    def load_pdf(self):

        reader = PdfReader(
            self.file_path
        )

        texts = []

        for page in reader.pages:

            text = page.extract_text()

            if text:

                texts.append(text)

        return texts


if __name__ == "__main__":

    print(
        "PDF loader is ready."
    )