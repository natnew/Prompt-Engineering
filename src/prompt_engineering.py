# src/prompt_engineering.py

def apply_technique(prompt, technique):
    """Applies the selected technique to the prompt and provides an explanation."""
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


