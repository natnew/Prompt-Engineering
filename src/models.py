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
        if model in ["gpt-3.5-turbo", "gpt-4"]:
            # For chat models, use the v1/chat/completions endpoint
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            return response['choices'][0]['message']['content'].strip()
        else:
            # For text completion models, use the v1/completions endpoint
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=150
            )
            return response.choices[0].text.strip()
    except Exception as e:
        return f"Error fetching response: {e}"



