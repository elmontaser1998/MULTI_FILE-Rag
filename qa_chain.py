from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
import logging

logging.basicConfig(level=logging.INFO)

def setup_conversational_chain(llm):
    """Set up QA chain with a custom prompt."""
    template = """
    Based on the context, answer the question with as much detail as possible.
    If the answer is not available in the context, say "Answer not found in the provided context." 
    Do not generate an incorrect answer.

    Context: {context}
    Question: {question}

    Answer:
    """
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    return chain

def handle_user_question(question, embeddings, llm):
    """Retrieve relevant documents and answer the user's question."""
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    documents = vector_store.similarity_search(question)
    context = [doc.page_content for doc in documents]

    chain = setup_conversational_chain(llm)
    response = chain({"input_documents": documents, "question": question}, return_only_outputs=True)
    generated_answer = response["output_text"]

    logging.info("Answer generated using vector store and LLM.")
    return context, generated_answer
