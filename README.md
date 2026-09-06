# RAG Retrieval Application using Docker

A Retrieval-Augmented Generation (RAG) retrieval pipeline containerized using Docker.

## Technologies

- Python
- Docker
- LangChain
- HuggingFace Sentence Transformers
- Pinecone
- PyPDF

## RAG Pipeline

PDF
↓
PDF Loader
↓
Text Splitting
↓
Embedding
↓
Pinecone Vector Database
↓
Similarity Search
↓
Retrieved Results

## Docker

Build the Docker image:

```bash
docker build -t rag-app .