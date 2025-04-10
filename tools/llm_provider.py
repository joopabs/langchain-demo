import logging

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

load_dotenv()  # Ensure environment variables are loaded
logger = logging.getLogger(__name__)


def get_llm(temperature: int = 0, provider: str = "ollama"):
    """
    Create and return an LLM provider based on the specified provider name.

    Args:
        temperature: The sampling temperature to use for the model (default: 0)
        provider: The name of the LLM provider to use (default: "ollama")

    Returns:
        An initialized LLM provider instance

    Raises:
        ValueError: If the specified provider is not supported
    """
    # Provider configuration mapping
    provider_configs = {
        "mistral": {
            "class": ChatOllama,
            "model": "mistral",
            "name": "ChatOllama"
        },
        "llama3": {
            "class": ChatOllama,
            "model": "llama3",
            "name": "ChatOllama"
        },
        "openai": {
            "class": ChatOpenAI,
            "model": "gpt-4o-mini",
            "name": "ChatOpenAI"
        },
        "gemini": {
            "class": ChatGoogleGenerativeAI,
            "model": "gemini-2.0-flash",
            "name": "ChatGoogleGenerativeAI"
        }
    }

    if provider not in provider_configs:
        raise ValueError(f"Unsupported LLM choice: {provider}")

    config = provider_configs[provider]
    logger.info(f"Using {config['name']} as LLM provider")

    return config["class"](temperature=temperature, model=config["model"])
