import os
import boto3
import logging
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

logging.basicConfig(level=logging.INFO)

def get_embedding_llm_model():
    try:
        # Vérifie si les credentials AWS sont présents
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials is None:
            raise ValueError("No AWS credentials found")

        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Tester avec un ping minimal
        embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0", client=client)
        embeddings.embed_documents(["ping test"])

        llm = ChatBedrock(model_id="anthropic.claude-3-sonnet-20240229-v1:0", client=client)
        logging.info("Connected to AWS Bedrock successfully.")
        return llm, embeddings

    except Exception as e:
        logging.warning(f" Bedrock unavailable: {e}. Falling back to Ollama.")

        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

        llm = Ollama(model="llama3.2", base_url=base_url)
        embeddings = OllamaEmbeddings(model="llama3.2", base_url=base_url)
        return llm, embeddings
