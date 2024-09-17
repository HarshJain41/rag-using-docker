# document_processing.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from docx import Document
import pdfkit


def convert_docx_to_pdf(docx_file, pdf_file):
    """
    Convert .docx file to a .pdf using pdfkit.
    """
    document = Document(docx_file)
    document.save(f"{docx_file}")
    
    # Convert the docx file to pdf using pdfkit
    pdfkit.from_file(docx_file, pdf_file)

def load_and_split_document(file_path, file_type):
    """
    Handles PDF and DOCX files. If DOCX, it converts to PDF first, 
    then processes the document.
    """
    # Convert DOCX to PDF if necessary
    if file_type == "docx":
        pdf_file = file_path.replace(".docx", ".pdf")
        convert_docx_to_pdf(file_path, pdf_file)
        file_path = pdf_file  # Update file path to newly created PDF

    # Load the PDF document
    loader = PyPDFLoader(file_path)
    raw_documents = loader.load()

    # Chunk the text using recursive character splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    documents = text_splitter.split_documents(raw_documents)
    
    return documents
