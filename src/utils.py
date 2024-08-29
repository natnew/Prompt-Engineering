# src/utils.py
import json

def load_techniques(filename='data/techniques.json'):
    """Loads prompt techniques and descriptions from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def load_prompts(filename='data/departments_prompts.json'):
    """Loads departments and prompts from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)
