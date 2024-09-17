# app.py
import streamlit as st
from doc_preprocessing import load_and_split_document
from indexing import initialize_pinecone, delete_index
from retrieval import retrieve_documents
from langchain_cohere import CohereEmbeddings, ChatCohere
from dotenv import load_dotenv
import os
import time
from langchain_pinecone import PineconeVectorStore

load_dotenv()

# Set API keys
cohere_api = os.getenv("COHERE_API_KEY")
pinecone_api = os.getenv("PINECONE_API_KEY")
cohere_chat_model = ChatCohere(cohere_api_key=cohere_api)
cohere_embeddings = CohereEmbeddings(cohere_api_key=cohere_api, user_agent="my-app", model="embed-english-v2.0")

def pretty_print_docs(docs):
    return "\n\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)])

# Initialize session state
if "index_name" not in st.session_state:
    st.session_state.index_name = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None

st.title("RAG-Based Document Search with LangChain")

# Upload PDF or DOCX document
uploaded_file = st.file_uploader("Upload a PDF or DOCX Document", type=["pdf", "docx"])

# Input for user query
query = st.text_input("Ask a question related to the uploaded document:")

if uploaded_file is not None and st.session_state.index_name is None:
    # Detect file type
    file_type = uploaded_file.name.split(".")[-1].lower()

    # Create a unique index name for the session
    user_index = f"user-{str(time.time()).replace('.', '-')}"
    st.session_state.index_name = user_index

    # # Save the uploaded file to the "data" directory
    # file_path = os.path.join("C:/Users/ADMIN/Desktop/rag_assignment/data", uploaded_file.name)
    # with open(file_path, "wb") as f:
    #     f.write(uploaded_file.getbuffer())
    # Save the uploaded file to a container-friendly path
    file_path = os.path.join("data", uploaded_file.name)  # Use relative path
    os.makedirs("data", exist_ok=True)  # Create the 'data' directory if it doesn't exist

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and split the document, converting if necessary
    documents = load_and_split_document(file_path, file_type)
    
    # Initialize Pinecone index
    index = initialize_pinecone(pinecone_api_key=pinecone_api, index_name=user_index)
    db = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=cohere_embeddings,
        index_name=user_index,
    )
    
    # Store the retriever in session state
    st.session_state.retriever = db.as_retriever(search_kwargs={"k": 5})
    st.write("Data Indexed Successfully")

# Add a submit button for query input
if st.session_state.retriever:
    if st.button("Submit"):
        # Retrieve documents based on the query
        result = retrieve_documents(query=query, retriever=st.session_state.retriever, llm=cohere_chat_model)
        
        st.header("Response:")
        st.write(result["answer"])

        st.write("-------------------------------------------------------------------")
        
        st.header("Context:")
        if "I don't know" in result["answer"]:
            st.markdown("Can't fetch the context!!")
        else:
            st.markdown(pretty_print_docs(result["context"]))

# Clean up index when user ends the session
if st.button("End Session and Delete Index"):
    if st.session_state.index_name:
        delete_index(st.session_state.index_name, pinecone_api)
        st.success(f"Index '{st.session_state.index_name}' deleted.")
        st.session_state.index_name = None
        st.session_state.retriever = None
