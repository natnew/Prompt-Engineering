"""Utils.py - JSON Data Loader for Prompt Engineering App

This module provides utility functions to load JSON data files containing prompt techniques and department prompts.
It includes functions to:

- 'load_techniques': Load prompt techniques and their descriptions from a JSON file.
- 'load_prompts': Load department-specific prompts from a JSON file.    

both functions:
1. Resolve the file paths dynamically relative to the script's location.
2. Raise a clear error if expected file is missing
3. Return the loaded data as a Python dictionary parsed from the JSON content.

These utilities support modular and reusable data access across the app."""

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
