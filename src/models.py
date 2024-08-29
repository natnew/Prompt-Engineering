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

def is_complete_sentence(text):
    """Check if the text ends with a complete sentence."""
    return text.strip().endswith(('.', '!', '?'))

def get_model_response(model, prompt):
    """Fetches response from the selected model, ensuring it finishes sentences."""
    try:
        max_tokens = 150  # Initial token limit
        generated_text = ""

        if model in ["gpt-3.5-turbo", "gpt-4"]:
            # Use chat-based model completion
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                stop=[".\n"]  # Encourage stopping after a full stop followed by a new line
            )
            generated_text = response['choices'][0]['message']['content'].strip()
        
        else:
            # Use completion-based model
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7,
                stop=[".\n"]  # Encourage stopping after a full stop followed by a new line
            )
            generated_text = response.choices[0].text.strip()

        # If the response doesn't end with a complete sentence, continue generation
        while not is_complete_sentence(generated_text):
            if model in ["gpt-3.5-turbo", "gpt-4"]:
                continuation = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": generated_text}
                    ],
                    max_tokens=50,
                    temperature=0.7,
                    stop=[".\n"]
                )
                generated_text += " " + continuation['choices'][0]['message']['content'].strip()
            else:
                continuation = openai.Completion.create(
                    model=model,
                    prompt=generated_text,
                    max_tokens=50,
                    temperature=0.7,
                    stop=[".\n"]
                )
                generated_text += " " + continuation.choices[0].text.strip()

        return generated_text

    except Exception as e:
        return f"Error fetching response: {e}"
