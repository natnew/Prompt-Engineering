# src/models.py
import openai
import os

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Available models
MODELS = {
    "GPT-4": "gpt-4",
    "GPT-3.5": "gpt-3.5-turbo",
}

def get_model_response(model, prompt):
    """Fetches response from the selected model."""
    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error fetching response: {e}"


