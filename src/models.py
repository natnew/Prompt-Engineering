# src/models.py
import openai
import os

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Available models
MODELS = {
    "GPT-4o": "gpt-4o",
    "GPT-4o mini": "gpt-4o-mini",
    "GPT-4 Turbo": "gpt-4-turbo",
    "GPT-4": "gpt-4",
    "GPT-3.5": "gpt-3.5-turbo"
}

def get_model_response(model, prompt, temperature=0.7, top_p=1.0, max_tokens=150):
    """Fetches response from the selected model, ensuring it is correctly formatted."""
    try:
        if model in ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"]:
            # Use chat-based model completion
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=1,
                stop=None
            )
            generated_text = response['choices'][0]['message']['content'].strip()
        else:
            # Use completion-based model
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=1,
                stop=None
            )
            generated_text = response['choices'][0]['text'].strip()

        return generated_text
    
    except Exception as e:
        return f"An error occurred: {str(e)}"
