# src/prompt_engineering.py

import re

def apply_technique(prompt, technique):
    """Applies the selected technique to the prompt and provides an explanation."""
    explanation = ""
    transformed_prompt = prompt  # Start with the original prompt

    if technique == "Zero-Shot":
        # Zero-Shot Prompting: No modifications to the prompt
        transformed_prompt = prompt
        explanation = "Zero-Shot Prompting: The model is given the prompt without any additional context or examples."

    elif technique == "Few-Shot":
        # Few-Shot Prompting: Generate examples based on the prompt
        examples = generate_few_shot_examples(prompt)
        transformed_prompt = f"{examples}\n**Now, {prompt}**"
        explanation = (
            "Few-Shot Prompting: Provided dynamically generated examples to guide the model. "
            "These examples are based on your prompt to improve response relevance."
        )

    elif technique == "Chain-of-Thought":
        # Chain-of-Thought Prompting: Encourage step-by-step reasoning
        transformed_prompt = f"{prompt}\n\n**Let's think step-by-step.**"
        explanation = (
            "Chain-of-Thought Prompting: Encouraged the model to explain its reasoning process step-by-step, "
            "which can lead to more accurate and detailed responses."
        )

    elif technique == "Meta-Prompting":
        # Meta-Prompting: Ask the model to create a prompt for the task
        transformed_prompt = f"**Construct an abstract framework that outlines the key components and sequential steps required for {prompt}**"
        explanation = (
            "Meta-Prompting: Focused on the structural aspects of the task, asking the model to consider the form and pattern of information."
        )

    elif technique == "Self-Consistency":
        # Self-Consistency Prompting: Instruct the model to ensure consistency
        transformed_prompt = f"{prompt}\n\n**Please explore different possible steps and ensure that your final process is logically consistent and coherent.**"
        explanation = (
            "Self-Consistency Prompting: Encouraged the model to consider multiple reasoning paths and select the most consistent answer."
        )

    elif technique == "Tree-of-Thought":
        # Tree-of-Thought Prompting: Encourage considering multiple approaches
        transformed_prompt = (
            f"{prompt}\n\n"
            "**For each major stage, generate two alternative methods (candidates) to accomplish that step. "
            "Evaluate the effectiveness of each alternative, considering factors like efficiency and fairness. "
            "Based on your evaluation, select the best option and proceed to the next stage. "
            "Continue this process to develop a comprehensive and optimized workflow.**"
        )
        explanation = (
            "Tree-of-Thought Prompting: Prompted the model to consider multiple approaches at each step, enabling systematic exploration and strategic planning."
        )

    else:
        # No specific technique applied
        transformed_prompt = prompt
        explanation = "No specific technique applied."

    return transformed_prompt, explanation

def generate_few_shot_examples(prompt):
    """Generates few-shot examples based on the user's prompt."""
    # Analyze the prompt to determine the task type
    task_type = identify_task_type(prompt)

    # Generate examples based on the identified task
    if task_type == "process_creation":
        examples = (
            "Task: Develop a workflow for processing job applications.\n"
            "Process:\n"
            "- Applicants submit their resumes through the online portal.\n"
            "- Applications are screened for minimum qualifications.\n"
            "- Qualified candidates are scheduled for initial interviews.\n"
            "- Interview feedback is collected and reviewed.\n"
            "- Offers are extended to selected candidates.\n\n"
            "Task: Design a procedure for handling customer support tickets.\n"
            "Process:\n"
            "- Customers submit support tickets via the helpdesk system.\n"
            "- Tickets are categorized based on issue type.\n"
            "- Support agents are assigned tickets according to expertise.\n"
            "- Agents troubleshoot and resolve issues.\n"
            "- Resolutions are documented in the knowledge base.\n"
            "- Customers are notified of the resolution."
        )
    else:
        # Default examples
        examples = (
            "Example: How to make a sandwich.\n"
            "Process:\n"
            "- Gather two slices of bread.\n"
            "- Add your favorite fillings between the slices.\n"
            "- Close the sandwich and enjoy.\n\n"
            "Example: Steps to change a tire.\n"
            "Process:\n"
            "- Loosen the lug nuts.\n"
            "- Jack up the car.\n"
            "- Remove the flat tire.\n"
            "- Mount the spare tire.\n"
            "- Tighten the lug nuts.\n"
            "- Lower the car."
        )

    return examples

def identify_task_type(prompt):
    """Identifies the task type based on the prompt content."""
    prompt_lower = prompt.lower()

    if "create a process" in prompt_lower or "develop a workflow" in prompt_lower or "design a procedure" in prompt_lower:
        return "process_creation"
    else:
        return "general"
