# src/models.py
import openai
import os
import time
import streamlit as st

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Available models
MODELS = {
    "GPT-4o": "gpt-4o",
    "GPT-4o mini": "gpt-4o-mini",
    "GPT-4 Turbo": "gpt-4-turbo",
    "GPT-4": "gpt-4",
    "GPT-3.5": "gpt-3.5-turbo",
    "Claude 3 Sonnet": "claude-3-sonnet",
    "Claude 3 Haiku": "claude-3-haiku",
    "Command": "command",
    "Llama 3 70b instruct": "llama-3-70b-instruct",
    "Phi 3": "phi-3",
    "ChatGLM Turbo": "chatglm-turbo",
    "Baidu ERNIE 4": "ernie-4",
    "Mistral 7b": "mistral-7b",
    "o1-preview": "o1-preview",
    "o1-mini": "o1-mini"
    
}

def is_complete_sentence(text):
    """Check if the text ends with a complete sentence."""
    return text.strip().endswith(('.', '!', '?'))

def ensure_complete_ending(text):
    """Ensure the text has a complete ending, add a conclusion if missing."""
    if not text.strip().endswith(('.', '!', '?')):
        text = text.rstrip() + ' Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team.'
    return text

def get_model_response(selected_model_key, prompt, **kwargs):
    # Retrieve model metadata
    model_metadata = MODELS[selected_model_key]
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
            return f"Error: {e}"

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
            return f"Error: {e}"

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
            return f"Error: {e}"

    else:
        return "Unsupported provider."

