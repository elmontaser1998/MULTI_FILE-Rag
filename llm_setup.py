import boto3
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
import logging

logging.basicConfig(level=logging.INFO)

def get_embedding_llm_model():
    """Load embedding and LLM models, preferring AWS Bedrock, fallback to Ollama."""
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=client)
        embeddings.embed_documents(["ping test"])
        llm = ChatBedrock(model_id="anthropic.claude-v2:1", client=client)
        logging.info("Connected to AWS Bedrock successfully.")
    except Exception as e:
        logging.warning(f"Bedrock connection failed: {e}.")
        llm = Ollama(model="llama3.2")
        embeddings = OllamaEmbeddings(model="llama3.2")
    return llm, embeddings
