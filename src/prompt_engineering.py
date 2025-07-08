"""prompt_engineering.py - Prompt Transformations and Explanation Logic

This module contains functions to apply various prompt engineering techniques
to enhance the performance of language models. Each technique is designed to
transform the input prompt in a specific way, and the module provides explanations
for each technique to help users understand the rationale behind the transformations.

This module defines the 'apply_technique' function, which transforms input prompts using various
prompt engineering techniques. The techniques include:
1. Zero-Shot Prompting
2. Few-Shot Prompting
3. Chain-of-Thought Prompting
4. Meta-Prompting
5. Self-Consistency Prompting  
6. Tree-of-Thought Prompting

For each technuqie, the function:
- Transforms the input prompt accordingly.
- Returns the transformed prompt along with an explanation of the technique used.

This utility helps experiement with different prompting strategies to improve the performance of language models
and provides insights into how each technique works."""

# src/prompt_engineering.py

def apply_technique(prompt, technique):
    """
    Applies a specified prompt engineering technique to transform an input prompt.
    
    This function takes a user-provided prompt and applies one of several prompt
    engineering techniques to enhance its effectiveness for language model interactions.
    Each technique modifies the prompt structure or adds contextual elements to
    improve the quality and relevance of model responses.
    
    Args:
        prompt (str): The original prompt text to be transformed. Must be a non-empty
                     string containing the user's query or instruction.
        technique (str): The prompt engineering technique to apply. Valid options are:
                        - "Zero-Shot": No modifications, uses prompt as-is
                        - "Few-Shot": Adds examples before the prompt
                        - "Chain-of-Thought": Adds step-by-step reasoning instruction
                        - "Meta-Prompting": Transforms prompt into a prompt generation task
                        - "Self-Consistency": Adds consistency validation instruction
                        - "Tree-of-Thought": Encourages multiple approach exploration
    
    Returns:
        tuple: A two-element tuple containing:
            - transformed_prompt (str): The modified prompt with the technique applied
            - explanation (str): A detailed explanation of how the technique works
                               and why it's beneficial for improving model responses
    
    Example:
        >>> prompt = "What is the capital of France?"
        >>> technique = "Chain-of-Thought"
        >>> transformed, explanation = apply_technique(prompt, technique)
        >>> print(transformed)
        "Let's think step-by-step.\nWhat is the capital of France?"
    
    Note:
        If an invalid technique is provided, the original prompt is returned
        unchanged with a default explanation message.
    """
    explanation = ""

    if technique == "Zero-Shot":
        transformed_prompt = prompt
        explanation = "Zero-Shot Prompting: The prompt is given to the model without any examples or further instructions. The model uses its general knowledge to respond directly."
    
    elif technique == "Few-Shot":
        examples = "Example: How to make a sandwich.\nResponse: Start with bread, add ingredients, then close the sandwich.\n\n"
        transformed_prompt = examples + prompt
        explanation = "Few-Shot Prompting: Examples are provided before the prompt to guide the model's understanding and improve response relevance."
    
    elif technique == "Chain-of-Thought":
        transformed_prompt = "Let's think step-by-step.\n" + prompt
        explanation = ("Chain-of-Thought Prompting: The prompt instructs the model to articulate its reasoning process step-by-step. "
                       "This encourages the model to think through each step of the problem, leading to a more accurate final answer.")
    
    elif technique == "Meta-Prompting":
        transformed_prompt = "Create a new prompt based on the task requirements: " + prompt
        explanation = ("Meta-Prompting: The prompt is designed to generate another prompt that better aligns with the task. "
                       "This improves the specificity and accuracy of the model's response.")
    
    elif technique == "Self-Consistency":
        transformed_prompt = "Ensure the response is consistent and coherent: " + prompt
        explanation = ("Self-Consistency Prompting: The model is instructed to provide outputs that are logically coherent and stable across similar tasks, "
                       "reducing variability in responses.")
    
    elif technique == "Tree-of-Thought":
        transformed_prompt = "Consider multiple approaches:\n1. ...\n2. ...\n\n" + prompt
        explanation = ("Tree-of-Thought Prompting: The model is encouraged to explore multiple paths or solutions for a given problem, promoting creative thinking "
                       "and diverse outputs.")
    
    else:
        transformed_prompt = prompt
        explanation = "No specific technique applied."

    return transformed_prompt, explanation
