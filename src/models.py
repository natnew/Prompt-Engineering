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
    "o1": "o1",
    "o1-mini": "o1-mini"
    
}

def is_complete_sentence(text):
    """Check if the text ends with a complete sentence."""
    return text.strip().endswith(('.', '!', '?'))

def ensure_complete_ending(text):
    """Ensure the text has a complete ending; add a conclusion if missing."""
    # Check if the text is empty
    if not text.strip():
        return text  # Return the empty text without appending anything

    # Check if the text ends with a complete sentence
    if text.strip().endswith(('.', '!', '?')):
        return text  # Text is already complete

    # Append the closing statement if the text is incomplete
    return text.rstrip() + ' Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team.'


def get_model_response(model, prompt, temperature=None, top_p=None, max_tokens=None):
    """Fetches response from the selected model, ensuring it is complete."""
    try:
        generated_text = ""
        continuation_prompt = prompt
        retries = 3  # Number of retries in case of rate limit errors

        while retries > 0:
            try:
                # Prepare the common parameters
                request_params = {
                    "model": model,
                    "messages": [
                        {"role": "user", "content": "You are a helpful assistant. " + continuation_prompt}
                    ],
                    "n": 1,
                    "stop": None  # Remove the stop sequence to let the model generate more naturally
                }

                # Adjust parameters based on the model
                if model in ["o1-preview", "o1-mini"]:
                    request_params["max_completion_tokens"] = 10000  # Default to 10000 if not specified
                    request_params["temperature"] = 1  # o1 models only support temperature=1
                    request_params["top_p"] = 1        # o1 models only support top_p=1
                else:
                    request_params["max_tokens"] = max_tokens if max_tokens else 500  # Default to 500 if not specified
                    request_params["temperature"] = temperature if temperature is not None else 0.7
                    request_params["top_p"] = top_p if top_p is not None else 1.0

                # Make the API call
                response = openai.ChatCompletion.create(**request_params)
                chunk = response['choices'][0]['message']['content'].strip()

                # Append only non-duplicate chunks to avoid repetition
                if chunk and chunk not in generated_text:
                    generated_text += " " + chunk

                # Check for completeness or if the text length is close to the max token limit
                if is_complete_sentence(generated_text) or (max_tokens and len(generated_text.split()) >= max_tokens):
                    break

                # Update the continuation prompt to continue from where it left off
                continuation_prompt = generated_text

                # If chunk is empty or short, avoid looping indefinitely
                if len(chunk) < (max_tokens / 2 if max_tokens else 100):  # Adjust this based on expected output length
                    break

            except openai.error.RateLimitError as e:
                # Handle rate limit error
                wait_time = float(str(e).split("Please try again in ")[1].split("s")[0])
                st.warning(f"Rate limit reached for {model}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries -= 1

        if retries == 0:
            st.error(f"Rate limit reached for {model}. Please try again later or select another model.")
            return None  # No valid response, just return

        # Ensure the last part ends with a full stop or add a closing statement
        generated_text = ensure_complete_ending(generated_text)

        return generated_text.strip()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
