# src/utils.py
import os
import json

def load_techniques(filename='data/techniques.json'):
    """Loads prompt techniques and descriptions from a JSON file."""
    # Dynamically resolve the file path relative to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Please ensure the file exists.")
    
    with open(file_path, 'r') as f:
        return json.load(f)

def load_prompts(filename='data/departments_prompts.json'):
    """Loads departments and prompts from a JSON file."""
    # Dynamically resolve the file path relative to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, '..', filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Please ensure the file exists.")
    
    with open(file_path, 'r') as f:
        return json.load(f)
