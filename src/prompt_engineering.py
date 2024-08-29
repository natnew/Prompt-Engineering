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
    elif technique == "Instruction Tuning":
        return "Please follow the instructions carefully: " + prompt
    else:
        return prompt

