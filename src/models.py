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

def is_complete_sentence(text):
    """Check if the text ends with a complete sentence."""
    return text.strip().endswith(('.', '!', '?'))

def get_model_response(model, prompt, temperature=0.7, top_p=1.0, max_tokens=150):
    """Fetches response from the selected model, ensuring it is complete."""
    try:
        generated_text = ""
        continuation_prompt = prompt

        while True:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": continuation_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=1,
                stop=None  # Optionally add stop sequences like ['\n\n'] or ['.', '!', '?']
            )
            chunk = response['choices'][0]['message']['content'].strip()
            generated_text += chunk

            # If the generated text ends with a complete sentence or reaches the max token limit, break the loop
            if is_complete_sentence(generated_text):
                break

            # Update the continuation prompt to continue from where it left off
            continuation_prompt = generated_text

            # Break if we are not getting more tokens, to avoid infinite loop
            if len(chunk) < max_tokens:
                break

        # Ensure the last part ends with a full stop
        if not generated_text.endswith(('.', '!', '?')):
            generated_text = generated_text.rstrip() + '.'

        return generated_text

    except Exception as e:
        return f"An error occurred: {str(e)}"
