import logging
import os

from dotenv import load_dotenv

load_dotenv()  # Ensure environment variables are loaded
logger = logging.getLogger(__name__)


def get_llm(temperature: int = 0):
    """
    Returns an instance of the chosen language model based on the MODEL_PROVIDER
    environment variable.
    Supported providers: 'ollama', 'openai', 'gemini'
    """
    provider = os.getenv("MODEL_PROVIDER", "gemini").lower()
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        logger.info("Using ChatOllama as LLM provider")
        return ChatOllama(temperature=temperature, model="mistral")
    elif provider == "openai":
        from langchain_openai import ChatOpenAI

        logger.info("Using ChatOpenAI as LLM provider")
        return ChatOpenAI(temperature=temperature, model="gpt-4o-mini")
    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        logger.info("Using ChatGoogleGenerativeAI as LLM provider")
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=temperature)
    else:
        raise ValueError(f"Unsupported LLM choice: {provider}")
