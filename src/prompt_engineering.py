# src/prompt_engineering.py

def apply_technique(prompt, technique):
    """Applies the selected technique to the prompt."""
    if technique == "Zero-Shot":
        return prompt
    elif technique == "Few-Shot":
        examples = "Example: How to make a sandwich.\nResponse: Start with bread, add ingredients, then close the sandwich.\n\n"
        return examples + prompt
    elif technique == "Chain-of-Thought":
        return "Let's think step-by-step.\n" + prompt
    elif technique == "Meta-Prompting":
        return "Create a new prompt based on the task requirements: " + prompt
    elif technique == "Self-Consistency":
        return "Ensure the response is consistent and coherent: " + prompt
    elif technique == "Tree-of-Thought":
        return "Consider multiple approaches:\n1. ...\n2. ...\n\n" + prompt
    else:
        return prompt


