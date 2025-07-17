"""machine_learning.py - prompt Engineering techniques using OpenAI GPT Models.

This module provides functions to apply various prompt engineering techniques using OpenAI's GPT models.
It includes implementations for:

1. Few-Shot Prompting
2. Zero-Shot Prompting  
3. Chain-of-Thought Prompting
4. Meta-Prompting
5. Self-Consistency Prompting
6. Tree-of-Thought Prompting

Each function:
1. Constructions a tailored prompt based on the technique.
2. Send the prompt to the OpenAI API.
3. Returns the model's response.

This module serves as a backend engine for a Streamlit application, allowing users to experiment with different prompting strategies
to enhance the performance of language models."""

import os
import streamlit as st
from openai import OpenAI
import logging

# Initialize OpenAI client with API key from environment variables or Streamlit secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None))

def apply_few_shot_prompting(user_prompt):
    """Apply Few-Shot Prompting using OpenAI GPT with chat completions."""
    try:
        few_shot_examples = """
        Example 1:
        Question: What is the capital of France?
        Answer: The capital of France is Paris.

        Example 2:
        Question: What is the capital of Spain?
        Answer: The capital of Spain is Madrid.
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on the given examples."},
            {"role": "user", "content": f"{few_shot_examples}\n\nQuestion: {user_prompt}\nAnswer:"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        model_output = response.choices[0].message.content.strip()
        return model_output
    except Exception as e:
        logging.error(f"Error in apply_few_shot_prompting: {str(e)}")
        return f"Error: Unable to generate response. {str(e)}"

def apply_zero_shot_prompting(user_prompt):
    """Apply Zero-Shot Prompting using OpenAI GPT with chat completions."""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that answers questions directly and accurately."},
            {"role": "user", "content": f"Answer this question directly: {user_prompt}"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        model_output = response.choices[0].message.content.strip()
        return model_output
    except Exception as e:
        logging.error(f"Error in apply_zero_shot_prompting: {str(e)}")
        return f"Error: Unable to generate response. {str(e)}"

def apply_chain_of_thought_prompting(user_prompt):
    """Apply Chain-of-Thought Prompting using OpenAI GPT with chat completions."""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that thinks through problems step by step."},
            {"role": "user", "content": f"Let's think step by step to solve this problem: {user_prompt}"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        model_output = response.choices[0].message.content.strip()
        return model_output
    except Exception as e:
        logging.error(f"Error in apply_chain_of_thought_prompting: {str(e)}")
        return f"Error: Unable to generate response. {str(e)}"

def apply_meta_prompting(user_prompt):
    """Apply Meta-Prompting using OpenAI GPT with chat completions."""
    try:
        messages = [
            {"role": "system", "content": "You are an expert at creating better prompts. Generate an improved version of the user's prompt."},
            {"role": "user", "content": f"Generate a better prompt to address this problem: {user_prompt}"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        model_output = response.choices[0].message.content.strip()
        return model_output
    except Exception as e:
        logging.error(f"Error in apply_meta_prompting: {str(e)}")
        return f"Error: Unable to generate response. {str(e)}"

def apply_self_consistency_prompting(user_prompt):
    """Apply Self-Consistency Prompting using OpenAI GPT with chat completions."""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides consistent and coherent answers."},
            {"role": "user", "content": f"Make sure this answer is consistent and coherent across different attempts: {user_prompt}"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        model_output = response.choices[0].message.content.strip()
        return model_output
    except Exception as e:
        logging.error(f"Error in apply_self_consistency_prompting: {str(e)}")
        return f"Error: Unable to generate response. {str(e)}"

def apply_tree_of_thought_prompting(user_prompt):
    """Apply Tree-of-Thought Prompting using OpenAI GPT with chat completions."""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that explores multiple approaches to solve problems."},
            {"role": "user", "content": f"Consider multiple approaches to solve this problem:\n1. First approach: ...\n2. Second approach: ...\n\nProblem: {user_prompt}"}
        ]
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        model_output = response.choices[0].message.content.strip()
        return model_output
    except Exception as e:
        logging.error(f"Error in apply_tree_of_thought_prompting: {str(e)}")
        return f"Error: Unable to generate response. {str(e)}"
