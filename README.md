# RAG-Based Document Search App

This is a **RAG-based (Retrieval Augmented Generation)** document search application built with **Streamlit**, **Cohere**, and **Pinecone**. The app allows you to upload a PDF or DOCX document, ask questions related to the content of the document, and retrieve answers using a retrieval-based method with **LangChain** and **Cohere LLMs**.

## Project Structure

├── test_data/               # Folder containing test files (e.g., PDF, DOCX) to test the app working
├── Dockerfile               # Dockerfile for containerization
├── app.py                   # Main application script
├── doc_preprocessing.py      # Functions for loading and processing documents
├── indexing.py              # Functions for indexing documents in Pinecone
├── requirements.txt         # Python dependencies
├── retrieval.py             # Functions for document retrieval
└── .env                     # Environment variables (add this file manually)


## Features

- Upload PDF or DOCX documents.
- Automatically process and index documents using Pinecone.
- Query the indexed documents using **LangChain** with Cohere embeddings.
- Retrieve answers and context from documents.

## Requirements

To run this app, you need to have the following API keys:

- **Pinecone API Key** for document indexing and search.
- **Cohere API Key** for embeddings and text-based retrieval.

## Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-document-search.git
cd rag-document-search
```
### 2. Set Up Environment Variables

You need to create a .env file at the root of the project to store your API keys. Add the following:

```bash
# .env file
PINECONE_API_KEY=your_pinecone_api_key
COHERE_API_KEY=your_cohere_api_key
```
### 3. Running the App with Docker

The easiest way to run the app is by using Docker. Follow these instructions to build and run the Docker container.

1. In the root directory of the project (where the Dockerfile is located), run the following command to build the Docker image:
   ```bash
   docker build -t rag-document-search .
```

2. Run the Docker Container
```bash
docker run -p 8501:8501 -e PINECONE_API_KEY=your_valid_pinecone_api_key_here -e COHERE_API_KEY=your_cohere_api_key_here rag-document-search
```

This will start the Streamlit app inside a Docker container, and the app will be available at ```http://localhost:8501```.




