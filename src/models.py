# src/models.py
import openai
import os
import time
import streamlit as st

# Retrieve the OpenAI API key from environment variables
#openai.api_key = os.getenv("OPENAI_API_KEY")

# Available models
MODELS = {
    "GPT-4o": {"provider": "openai", "engine": "gpt-4o"},
    "GPT-4o mini": {"provider": "openai", "engine": "gpt-4o-mini"},
    "GPT-4 Turbo": {"provider": "openai", "engine": "gpt-4-turbo"},
    "GPT-4": {"provider": "openai", "engine": "gpt-4"},
    "GPT-3.5": {"provider": "openai", "engine": "gpt-3.5-turbo"},
    "Claude 3 Sonnet": {"provider": "anthropic", "engine": "claude-3-sonnet"},
    "Claude 3 Haiku": {"provider": "anthropic", "engine": "claude-3-haiku"},
    "Command": {"provider": "cohere", "engine": "command"},
    "Llama 3 70b instruct": {"provider": "huggingface", "engine": "llama-3-70b-instruct"},
    "Phi 3": {"provider": "huggingface", "engine": "phi-3"},
    "ChatGLM Turbo": {"provider": "huggingface", "engine": "chatglm-turbo"},
    "Baidu ERNIE 4": {"provider": "baidu", "engine": "ernie-4"},
    "Mistral 7b": {"provider": "huggingface", "engine": "mistral-7b"},
    "o1-preview": {"provider": "openai", "engine": "o1-preview"},
    "o1-mini": {"provider": "openai", "engine": "o1-mini"},
}


def set_api_key_or_client(model_metadata):
    """Set the appropriate API key or return a client based on the provider."""
    provider = model_metadata["provider"]

    if provider == "openai":
        # Use different API keys for GPT-O models
        if model_metadata["engine"].startswith("o1-"):
            openai.api_key = st.secrets["api_keys"]["OPENAI_O_KEY"]
        else:
            openai.api_key = st.secrets["api_keys"]["OPENAI_API_KEY"]
        return None  # OpenAI uses a global API key, no client needed
    elif provider == "anthropic":
        import anthropic
        return anthropic.Client(st.secrets["api_keys"]["ANTHROPIC_API_KEY"])
    elif provider == "cohere":
        import cohere
        return cohere.Client(st.secrets["api_keys"]["COHERE_API_KEY"])
    else:
        raise ValueError(f"Unsupported provider: {provider}")
        

def is_complete_sentence(text):
    """Check if the text ends with a complete sentence."""
    return text.strip().endswith(('.', '!', '?'))

def ensure_complete_ending(text):
    """Ensure the text has a complete ending, add a conclusion if missing."""
    if not text.strip().endswith(('.', '!', '?')):
        text = text.rstrip() + ' Thank you for your understanding and support.'
    return text

def get_model_response(selected_model_key, prompt, **kwargs):
    """Generate a response from the selected model."""
    # Retrieve model metadata
    model_metadata = MODELS.get(selected_model_key)
    if not model_metadata:
        return f"Model '{selected_model_key}' is not supported."

    provider = model_metadata["provider"]
    engine = model_metadata["engine"]

    # Set API key or client
    client = set_api_key_or_client(model_metadata)

    # Handle each provider
    if provider == "openai":
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 1.0),
                max_tokens=kwargs.get("max_tokens", 150),
            )
            return response["choices"][0]["text"].strip()
        except openai.error.OpenAIError as e:
            return f"OpenAI Error: {e}"

    elif provider == "anthropic":
        try:
            response = client.completion(
                model=engine,
                prompt=prompt,
                max_tokens_to_sample=kwargs.get("max_tokens", 150),
                temperature=kwargs.get("temperature", 0.7),
            )
            return response["completion"].strip()
        except anthropic.AnthropicError as e:
            return f"Anthropic Error: {e}"

    elif provider == "cohere":
        try:
            response = client.generate(
                model=engine,
                prompt=prompt,
                max_tokens=kwargs.get("max_tokens", 150),
                temperature=kwargs.get("temperature", 0.7),
            )
            return response.generations[0].text.strip()
        except cohere.CohereError as e:
            return f"Cohere Error: {e}"

    else:
        return f"Provider '{provider}' is not supported."
