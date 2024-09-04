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
    "GPT-3.5": "gpt-3.5-turbo"
}

def is_complete_sentence(text):
    """Check if the text ends with a complete sentence."""
    return text.strip().endswith(('.', '!', '?'))

def get_model_response(model, prompt, temperature=0.7, top_p=1.0, max_tokens=100):
    """Fetches response from the selected model, ensuring it is complete."""
    try:
        generated_text = ""
        continuation_prompt = prompt
        retries = 3  # Number of retries in case of rate limit errors

        while retries > 0:
            try:
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
                    stop=["\n\n"]  # Encourage stopping at a logical paragraph break
                )
                chunk = response['choices'][0]['message']['content'].strip()

                # Check if the new chunk is just a repetition
                if chunk in generated_text:
                    st.warning("The model seems to be repeating itself. Adjusting strategy to avoid redundancy.")
                    break

                generated_text += chunk

                # If the generated text ends with a complete sentence or reaches the max token limit, break the loop
                if is_complete_sentence(generated_text):
                    break

                # Update the continuation prompt to continue from where it left off
                continuation_prompt = generated_text

                # Break if we are not getting more tokens, to avoid infinite loop
                if len(chunk) < max_tokens:
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

        # Ensure the last part ends with a full stop
        if not generated_text.endswith(('.', '!', '?')):
            generated_text = generated_text.rstrip() + '.'

        return generated_text

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
