from PyPDF2 import PdfReader
from docx import Document
import os
import logging
from langchain_experimental.agents import create_csv_agent

logging.basicConfig(level=logging.INFO)

def extract_text_from_pdfs(pdf_files):
    """Extract text from a list of uploaded PDF files."""
    text = ""
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text()
    logging.info(f"Extracted text from {len(pdf_files)} PDF(s).")
    return text

def extract_text_from_word(word_files):
    """Extract text from a list of uploaded Word documents."""
    text = ""
    for word in word_files:
        doc = Document(word)
        for paragraph in doc.paragraphs:
            text += paragraph.text
    logging.info(f"Extracted text from {len(word_files)} Word document(s).")
    return text

def process_csv_file(csv_file, llm):
    """Process a single uploaded CSV file with a specified LLM."""
    if csv_file:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, csv_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(csv_file.getbuffer())
        logging.info(f"Saved CSV file to {temp_file_path}")
        agent = create_csv_agent(llm, temp_file_path, verbose=True, allow_dangerous_code=True)
        return agent
    return None
