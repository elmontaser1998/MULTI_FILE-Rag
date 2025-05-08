import streamlit as st
import os
import time
import logging
from models import ChatTurn,UserQuestion,UploadedFileInfo
from dotenv import load_dotenv
from llm_setup import get_embedding_llm_model
from file_processing import extract_text_from_pdfs, extract_text_from_word, process_csv_file
from vector_store import create_vector_store
from qa_chain import handle_user_question
from langchain_community.llms import Ollama
from utils import save_chat_to_csv

# Configure logger (reset each time the script runs)
log_file = "chat_assistant.log"
open(log_file, 'w').close()  # Clear previous logs
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    st.set_page_config(page_title="Multi-File Chat 💡", layout="wide")
    st.title("💬 Multi-File Chat Assistant with History & Export")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Load LLM and embedding model
    llm, embeddings = get_embedding_llm_model()
    logging.info("LLM and embedding models loaded successfully.")

    # UI menu for file type
    menu = ["Chat with PDF", "Chat with Word", "Chat with CSV"]
    choice = st.selectbox("Select file type to chat with:", menu)

    csv_file = None

    if choice == "Chat with PDF":
        with st.sidebar:
            pdf_files = st.file_uploader("Select PDF files", accept_multiple_files=True, type="pdf")
            if st.button("Process PDFs"):
                if pdf_files:
                    for f in pdf_files:
                        try:
                            UploadedFileInfo(filename=f.name, expected_type="pdf")
                        except Exception as e:
                            st.error(f"Invalid file: {e}")
                            return
                    st.info("Processing your PDFs...")
                    text = extract_text_from_pdfs(pdf_files)
                    create_vector_store(text, embeddings)
                    logging.info(f"Processed {len(pdf_files)} PDF file(s). Vector store created.")
                    st.success("PDFs processed successfully!")

    elif choice == "Chat with Word":
        with st.sidebar:
            word_files = st.file_uploader("Select Word files", accept_multiple_files=True, type="docx")
            if st.button("Process Word Docs"):
                if word_files:
                    for f in word_files:
                        try:
                            UploadedFileInfo(filename=f.name, expected_type="docx")
                        except Exception as e:
                            st.error(f"Invalid file: {e}")
                            return
                    st.info("Processing your Word documents...")
                    text = extract_text_from_word(word_files)
                    create_vector_store(text, embeddings)
                    logging.info(f"Processed {len(word_files)} Word file(s). Vector store created.")
                    st.success("Word documents processed successfully!")

    elif choice == "Chat with CSV":
        with st.sidebar:
            csv_file = st.file_uploader("Select CSV file", type="csv")
            if st.button("Process CSV"):
                if csv_file:
                    try:
                        UploadedFileInfo(filename=csv_file.name, expected_type="csv")
                    except Exception as e:
                        st.error(f"Invalid file: {e}")
                        return
                    st.info("Processing your CSV file...")
                    agent = process_csv_file(csv_file, llm)
                    if agent:
                        st.success("CSV processed successfully!")
                        logging.info("CSV processed and agent created.")
                    else:
                        st.error("Failed to process the CSV file.")
                        logging.warning("CSV file processing failed.")

    # User input question
    user_question = st.text_input("Enter your question:")

    if user_question:
        logging.info(f"User question: {user_question}")
        try:
            question_obj = UserQuestion(text=user_question)
        except Exception as e:
            st.error(f"Invalid question: {e}")
            return

        if choice == "Chat with CSV" and csv_file:
            # CSV chat uses a CSV agent
            agent = process_csv_file(csv_file, Ollama(model="llama3.2"))
            if agent:
                start_time = time.time()
                response = agent.run(question_obj.text)
                end_time = time.time()
                logging.info(f"CSV response generated in {end_time - start_time:.2f} seconds.")
                st.write("Response:", response)
                st.session_state.chat_history.append({"question": question_obj.text, "answer": response})
            else:
                logging.error("CSV agent creation failed on question.")
        else:
            # Non-CSV file uses vectorstore QA chain
            context, generated_answer = handle_user_question(question_obj.text, embeddings, llm)
            logging.info("Answer generated from vector store.")
            st.write("Response:", generated_answer)
            chat = ChatTurn(question=question_obj.text, answer=generated_answer)
            st.session_state.chat_history.append(chat.model_dump())
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("🕓 Chat History")
        for item in reversed(st.session_state.chat_history):
            st.markdown(f"**Q:** {item['question']}")
            st.markdown(f"**A:** {item['answer']}")

        # Download history as CSV
        st.download_button("⬇️ Download Q&A CSV", save_chat_to_csv(st.session_state.chat_history), "chat_history.csv")

if __name__ == "__main__":
    main()
