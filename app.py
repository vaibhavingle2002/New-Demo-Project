import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from loader import PDFLoader
from Splitters import RecursiveSplitter
from model import HuggingEmbedding
from Vectors import VectoreDatabase


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📚 RAG Document Assistant")

st.write(
    "Upload a PDF and ask questions. "
    "The application retrieves the most relevant information "
    "using Hugging Face embeddings and Pinecone."
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Project Information")

    st.write("**Technology Stack**")

    st.write("🐍 Python")
    st.write("📄 PDF Loader")
    st.write("✂️ Text Splitter")
    st.write("🤗 Hugging Face Embeddings")
    st.write("🌲 Pinecone Vector Database")
    st.write("🐳 Docker")
    st.write("🎈 Streamlit")


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

st.subheader("1️⃣ Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)


# --------------------------------------------------
# PROCESS PDF
# --------------------------------------------------

if uploaded_file is not None:

    st.success(
        f"PDF selected: {uploaded_file.name}"
    )

    # Create temporary PDF file
    pdf_path = "/tmp/uploaded_document.pdf"

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # --------------------------------------------------
    # LOAD PDF
    # --------------------------------------------------

    with st.spinner("📄 Loading PDF..."):

        loader = PDFLoader(
            pdf_path
        )

        data = loader.load_pdf()

    st.success(
        f"PDF loaded successfully — {len(data)} pages"
    )


    # --------------------------------------------------
    # SPLIT PDF
    # --------------------------------------------------

    with st.spinner("✂️ Creating chunks..."):

        splitter = RecursiveSplitter(
            data
        )

        chunks = splitter.split()

    st.success(
        f"Chunks created: {len(chunks)}"
    )


    # --------------------------------------------------
    # EMBEDDING MODEL
    # --------------------------------------------------

    with st.spinner(
        "🤗 Loading embedding model..."
    ):

        embedding = HuggingEmbedding()

        model = embedding.embedding_model()

    st.success(
        "Embedding model loaded successfully"
    )


    # --------------------------------------------------
    # PINECONE
    # --------------------------------------------------

    with st.spinner(
        "🌲 Connecting to Pinecone..."
    ):

        database = VectoreDatabase(
            chunks,
            model
        )

        database.build_index()

    st.success(
        "Pinecone index updated successfully"
    )


    st.divider()


    # --------------------------------------------------
    # DOCUMENT INFORMATION
    # --------------------------------------------------

    st.subheader("📊 Document Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Pages",
            len(data)
        )

    with col2:
        st.metric(
            "Chunks",
            len(chunks)
        )

    with col3:
        st.metric(
            "PDF",
            uploaded_file.name
        )


    st.divider()


    # --------------------------------------------------
    # QUESTION
    # --------------------------------------------------

    st.subheader("2️⃣ Ask Your Question")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What is the new education policy?"
    )


    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    if st.button(
        "🔍 Search",
        use_container_width=True
    ):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "🔎 Searching Pinecone..."
            ):

                results = database.Search(
                    question,
                    k=2
                )


            st.subheader(
                "📌 Retrieved Results"
            )


            # --------------------------------------------------
            # DISPLAY RESULTS
            # --------------------------------------------------

            if results.matches:

                for i, match in enumerate(
                    results.matches,
                    start=1
                ):

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### Result {i}"
                        )

                        st.write(
                            f"**ID:** {match.id}"
                        )

                        st.write(
                            f"**Similarity:** {match.score:.4f}"
                        )

                        st.markdown(
                            "**Retrieved Text:**"
                        )

                        st.write(
                            match.metadata.get(
                                "content",
                                "No content available."
                            )
                        )

            else:

                st.warning(
                    "No relevant results found."
                )

else:

    st.info(
        "👆 Please upload a PDF to begin."
    )