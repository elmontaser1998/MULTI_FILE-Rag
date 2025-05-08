# MultiFile-RAG

## Introduction

**MultiFile-RAG** is a powerful and modular application that enables users to ask questions about the content of documents (PDF, Word, CSV) using advanced Large Language Models (LLMs).

It supports semantic search, structured querying through intelligent agents, and automatic fallback between AWS Bedrock and Ollama based on environment availability.

---
## Key Features

-  Upload and analyze PDF, Word, and CSV files.
-  Automatic fallback: if AWS Bedrock fails or credentials are missing, the app uses Ollama locally.
-  Vector store with FAISS for efficient semantic search over unstructured data.
-  Smart CSV agent that interprets and answers structured queries.
-  Dockerized with full CI/CD pipeline and integrated unit testing.
-  Export conversation history to CSV.

---
## Technologies Used
| Category     | Tools / Libraries                               |
| ------------ | ----------------------------------------------- |
| LLMs         | AWS Bedrock (Claude, Titan), Ollama (LLaMA 3.2) |
| Embeddings   | Bedrock Embeddings, Ollama Embeddings           |
| Framework    | LangChain                                       |
| Frontend     | Streamlit                                       |
| Vector Store | FAISS                                           |
| DevOps       | Docker, GitHub Actions CI/CD                    |
| Testing      | Pytest                                          |

---

## Architecture

![image](https://github.com/user-attachments/assets/6b67ba11-01be-48c6-907e-de27e651c3ed)

The **MultiFile-RAG** App handles unstructured and structured documents differently:

### Process for PDF and Word Files
1. **Upload**: Users upload one or more PDF or Word documents.
2. **Text Chunking**: Extracted content is split into manageable chunks.
3. **Embedding**: Each chunk is embedded into vector representations.
4. **Storage**: Chunks are saved in a FAISS vector store.
5. **Semantic Search**: User queries are embedded and matched against stored chunks.
6. **Answer Generation**: Most relevant chunks are passed to the LLM for contextual response generation.

### Process for CSV Files
1. **Upload**: User selects a CSV file.
2. **Agent Activation**: A dedicated CSV agent is instantiated using LangChain.
3. **Query Execution**: The agent executes queries directly on the CSV using the LLM's reasoning capabilities.
4. **Answer Delivery**: Structured answers are generated without embedding or chunking.

---
## Dependencies and Installation
### Install Locally

```bash
git clone https://github.com/elmontaser1998/MULTI_FILE-Rag.git
cd MULTI_FILE-Rag

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file (optional, recommended for local testing):
```env
OLLAMA_BASE_URL=http://localhost:11434
```
🔑 If you're using AWS Bedrock, make sure your AWS credentials are properly configured.

By default, boto3 (used by the app) will look for credentials in this file:
```bash
~/.aws/credentials
```
To configure them, run the following command :
```bash
aws configure
```
---
## Usage 
Start the app:
```bash
streamlit run app.py
```

In the web UI:
1. Choose the file type: PDF, Word, or CSV
2. Upload your file(s)
3. Ask your question
4. View real-time, context-aware answers powered by LLMs
5. Export chat history as CSV if needed
---

## Docker Support

### Build the Docker Image
```bash
docker build -t multifile-rag-app .
```
### Run the App with AWS & Ollama Support
```bash
docker run --name rag-multifile -p 8501:8501 \
  -e AWS_ACCESS_KEY_ID=your_aws_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_aws_secret_key \
  -e AWS_DEFAULT_REGION=us-east-1 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --add-host=host.docker.internal:host-gateway \
  multifile-rag-app

```
---
## CI/CD Pipeline
A GitHub Actions workflow is triggered on every push or pull request to master.

Workflow Steps:
- Run unit tests with pytest
-  Build and push Docker image to Docker Hub
-  Output image digest (SHA256) for traceability

Required Secrets:
- DOCKER_USERNAME
- DOCKER_PASSWORD

---
## Tests
Run all unit tests using:
```bash
pytest test_function.py

```
Tests include PDF/Word/CSV processing and vector store logic.


