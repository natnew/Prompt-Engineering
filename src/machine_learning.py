import openai
import streamlit as st

# Load the OpenAI API key from Streamlit secrets or environment variables
openai.api_key = st.secrets.get("OPENAI_API_KEY", None)

def apply_few_shot_prompting(user_prompt):
    """Apply Few-Shot Prompting using a machine learning model (OpenAI GPT)."""
    few_shot_examples = """
    Example 1:
    Question: What is the capital of France?
    Answer: The capital of France is Paris.

    Example 2:
    Question: What is the capital of Spain?
    Answer: The capital of Spain is Madrid.
    """
    full_prompt = f"{few_shot_examples}\n\nQuestion: {user_prompt}\nAnswer:"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # Use the GPT model available to you
        prompt=full_prompt,
        max_tokens=100,
        temperature=0.7
    )
    model_output = response.choices[0].text.strip()
    return model_output

def apply_zero_shot_prompting(user_prompt):
    """Apply Zero-Shot Prompting."""
    full_prompt = f"Answer this question directly: {user_prompt}"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=full_prompt,
        max_tokens=100,
        temperature=0.7
    )
    model_output = response.choices[0].text.strip()
    return model_output

def apply_chain_of_thought_prompting(user_prompt):
    """Apply Chain-of-Thought Prompting."""
    full_prompt = f"Let's think step by step to solve this problem: {user_prompt}"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=full_prompt,
        max_tokens=150,
        temperature=0.7
    )
    model_output = response.choices[0].text.strip()
    return model_output

def apply_meta_prompting(user_prompt):
    """Apply Meta-Prompting."""
    full_prompt = f"Generate a better prompt to address this problem: {user_prompt}"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=full_prompt,
        max_tokens=150,
        temperature=0.7
    )
    model_output = response.choices[0].text.strip()
    return model_output

def apply_self_consistency_prompting(user_prompt):
    """Apply Self-Consistency Prompting."""
    full_prompt = f"Make sure this answer is consistent and coherent across different attempts: {user_prompt}"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=full_prompt,
        max_tokens=150,
        temperature=0.7
    )
    model_output = response.choices[0].text.strip()
    return model_output

def apply_tree_of_thought_prompting(user_prompt):
    """Apply Tree-of-Thought Prompting."""
    full_prompt = f"Consider multiple approaches to solve this problem:\n1. First approach: ...\n2. Second approach: ...\n\nProblem: {user_prompt}"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=full_prompt,
        max_tokens=200,
        temperature=0.7
    )
    model_output = response.choices[0].text.strip()
    return model_output
