import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import (
    AzureChatOpenAI,
    AzureOpenAI,
    AzureOpenAIEmbeddings,
    ChatOpenAI,
    OpenAI,
    OpenAIEmbeddings,
)
from pydantic.v1.types import SecretStr

# Load environment variables
load_dotenv()

# Configuration
DEFAULT_TEMPERATURE = 0.0

# Utility function to get API keys from environment variables


def get_api_key(service):
    return os.getenv(f"API_KEY_{service.upper()}") or os.getenv(
        f"{service.upper()}_API_KEY"
    )


# Ollama models
def get_ollama_chat(
    model_name: str, temperature=DEFAULT_TEMPERATURE, base_url="http://localhost:11434"
):
    return Ollama(model=model_name, temperature=temperature, base_url=base_url)


def get_ollama_embedding(model_name: str, temperature=DEFAULT_TEMPERATURE):
    return OllamaEmbeddings(model=model_name, temperature=temperature)


# HuggingFace models


def get_huggingface_embedding(model_name: str):
    return HuggingFaceEmbeddings(model_name=model_name)


# LM Studio and other OpenAI compatible interfaces


def get_lmstudio_chat(
    model_name: str,
    base_url="http://localhost:1234/v1",
    temperature=DEFAULT_TEMPERATURE,
):
    # type: ignore
    return ChatOpenAI(
        model_name=model_name,
        base_url=base_url,
        temperature=temperature,
        api_key="none",
    )


def get_lmstudio_embedding(model_name: str, base_url="http://localhost:1234/v1"):
    # type: ignore
    return OpenAIEmbeddings(model_name=model_name, base_url=base_url)


# Anthropic models


def get_anthropic_chat(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE):
    api_key = api_key or get_api_key("anthropic")
    # type: ignore
    return ChatAnthropic(
        model_name=model_name, temperature=temperature, api_key=api_key
    )


# OpenAI models


def get_openai_chat(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE):
    api_key = api_key or get_api_key("openai")
    # type: ignore
    return ChatOpenAI(model_name=model_name, temperature=temperature, api_key=api_key)


def get_openai_instruct(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE):
    api_key = api_key or get_api_key("openai")
    # type: ignore
    return OpenAI(model=model_name, temperature=temperature, api_key=api_key)


def get_openai_embedding(model_name: str, api_key=None):
    api_key = api_key or get_api_key("openai")
    return OpenAIEmbeddings(model=model_name, api_key=api_key)  # type: ignore


def get_azure_openai_chat(
    deployment_name: str,
    api_key=None,
    temperature=DEFAULT_TEMPERATURE,
    azure_endpoint=None,
):
    api_key = api_key or get_api_key("openai_azure")
    azure_endpoint = azure_endpoint or os.getenv("OPENAI_AZURE_ENDPOINT")
    # type: ignore
    return AzureChatOpenAI(
        deployment_name=deployment_name,
        temperature=temperature,
        api_key=api_key,
        azure_endpoint=azure_endpoint,
    )


def get_azure_openai_instruct(
    deployment_name: str,
    api_key=None,
    temperature=DEFAULT_TEMPERATURE,
    azure_endpoint=None,
):
    api_key = api_key or get_api_key("openai_azure")
    azure_endpoint = azure_endpoint or os.getenv("OPENAI_AZURE_ENDPOINT")
    # type: ignore
    return AzureOpenAI(
        deployment_name=deployment_name,
        temperature=temperature,
        api_key=api_key,
        azure_endpoint=azure_endpoint,
    )


def get_azure_openai_embedding(deployment_name: str, api_key=None, azure_endpoint=None):
    api_key = api_key or get_api_key("openai_azure")
    azure_endpoint = azure_endpoint or os.getenv("OPENAI_AZURE_ENDPOINT")
    # type: ignore
    return AzureOpenAIEmbeddings(
        deployment_name=deployment_name, api_key=api_key, azure_endpoint=azure_endpoint
    )


# Google models


def get_google_chat(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE):
    api_key = api_key or get_api_key("google")
    # type: ignore
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        },
    )


# Groq models


def get_groq_chat(model_name: str, api_key=None, temperature=DEFAULT_TEMPERATURE):
    api_key = api_key or get_api_key("groq")
    # type: ignore
    return ChatGroq(model_name=model_name, temperature=temperature, api_key=api_key)


# OpenRouter models


def get_openrouter(
    model_name: str = "meta-llama/llama-3.1-8b-instruct:free",
    api_key=None,
    temperature=DEFAULT_TEMPERATURE,
):
    api_key = api_key or get_api_key("openrouter")
    # type: ignore
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        model=model_name,
        temperature=temperature,
    )


def get_embedding_hf(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    return HuggingFaceEmbeddings(model_name=model_name)


def get_embedding_openai(api_key=None):
    api_key = api_key or get_api_key("openai")
    return OpenAIEmbeddings(api_key=api_key)  # type: ignore
