# src/utils.py

def load_example_prompts():
    """Loads example prompts for different departments."""
    return {
        "Marketing": ["Write an engaging product description.", "Create a catchy slogan."],
        "Customer Support": ["Generate a polite response to a complaint.", "Draft an apology letter."],
        "Data Science": ["Explain machine learning to a beginner.", "Describe a data pipeline."],
    }

def load_techniques():
    """Loads descriptions for different prompt engineering techniques."""
    return {
        "Zero-Shot": "The model is provided with a prompt and generates a response without additional context.",
        "Few-Shot": "The model is given a few examples along with the prompt to guide its response.",
        "Chain-of-Thought": "The model is encouraged to think step-by-step to arrive at a more complex answer.",
        "Instruction Tuning": "Provide clear instructions to guide the model's response more effectively.",
    }

