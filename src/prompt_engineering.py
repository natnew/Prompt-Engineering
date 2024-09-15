# src/prompt_engineering.py

def apply_technique(prompt, technique):
    """Applies the selected technique to the prompt and provides an explanation."""
    explanation = ""
    transformed_prompt = prompt  # Start with the original prompt

    if technique == "Zero-Shot Prompting":
        # No changes are made in zero-shot prompting
        explanation = "Zero-Shot Prompting: The prompt is given to the model without any examples or further instructions. The model uses its general knowledge to respond directly."
        
    elif technique == "Few-Shot Prompting":
        examples = (
            "**[Added Examples]:**\n"
            "Q: How to make a sandwich?\n"
            "A: Start with bread, add ingredients, then close the sandwich.\n\n"
        )
        transformed_prompt = f"{examples}{prompt}"
        explanation = "Few-Shot Prompting: Examples are provided before the prompt to guide the model's understanding and improve response relevance."
        
    elif technique == "Chain-of-Thought (CoT) Prompting":
        added_instruction = "**[Added Instruction]:** Let's think step-by-step.\n\n"
        transformed_prompt = f"{added_instruction}{prompt}"
        explanation = (
            "Chain-of-Thought Prompting: The prompt instructs the model to articulate its reasoning process step-by-step. "
            "This encourages the model to think through each step of the problem, leading to a more accurate final answer."
        )
        
    elif technique == "Meta-Prompting":
        added_instruction = "**[Added Meta-Prompt]:** Create a new prompt based on the task requirements.\n\n"
        transformed_prompt = f"{added_instruction}{prompt}"
        explanation = (
            "Meta-Prompting: The prompt is designed to generate another prompt that better aligns with the task. "
            "This improves the specificity and accuracy of the model's response."
        )
        
    elif technique == "Self-Consistency Prompting":
        added_instruction = "**[Added Instruction]:** Ensure the response is consistent and coherent.\n\n"
        transformed_prompt = f"{added_instruction}{prompt}"
        explanation = (
            "Self-Consistency Prompting: The model is instructed to provide outputs that are logically coherent and stable across similar tasks, "
            "reducing variability in responses."
        )
        
    elif technique == "Tree-of-Thought (ToT) Prompting":
        added_instruction = "**[Added Instruction]:** Consider multiple approaches:\n1. Approach one...\n2. Approach two...\n\n"
        transformed_prompt = f"{added_instruction}{prompt}"
        explanation = (
            "Tree-of-Thought Prompting: The model is encouraged to explore multiple paths or solutions for a given problem, promoting creative thinking "
            "and diverse outputs."
        )
    else:
        explanation = "No specific technique applied."

    return transformed_prompt, explanation
