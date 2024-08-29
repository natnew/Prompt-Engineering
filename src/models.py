# src/models.py
import openai

# Configure your OpenAI API key
openai.api_key = "your-openai-api-key"

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

