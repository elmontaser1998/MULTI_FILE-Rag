from pathlib import Path

from utils import save_chat_to_csv
from file_processing import extract_text_from_pdfs, extract_text_from_word
from vector_store import create_vector_store

def test_save_chat_to_csv():
    history = [{"question": "Quelle heure est-il ?", "answer": "Il est midi."}]
    csv = save_chat_to_csv(history)
    assert "question,answer" in csv
    assert "Quelle heure est-il ?" in csv
    
    
def test_extract_text_from_pdfs(tmp_path):
    # Crée un faux fichier PDF avec PyPDF2
    pdf_path = "file_exemple\chatUnitTest.pdf"
    result = extract_text_from_pdfs([open(pdf_path, "rb")])
    assert isinstance(result, str)
    
def test_extract_text_from_word(tmp_path):
    word_path = "file_exemple\\resume REN.docx"
    result = extract_text_from_word([open(word_path, "rb")])
    assert isinstance(result, str)

class DummyEmbeddings:
    def embed_documents(self, texts):
        return [[0.1] * 384 for _ in texts]

def test_create_vector_store(tmp_path, monkeypatch):
    monkeypatch.chdir("file_exemple")
    text = "Ceci est un test de vectorisation. " * 20
    embeddings =  DummyEmbeddings() 
    create_vector_store(text, embeddings)
    assert Path("faiss_index").exists()