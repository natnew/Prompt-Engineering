# Prompt Engineering Tool - API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Core Modules](#core-modules)
3. [Models Module](#models-module)
4. [Prompt Engineering Module](#prompt-engineering-module)
5. [Utils Module](#utils-module)
6. [Machine Learning Module](#machine-learning-module)
7. [Streamlit Pages](#streamlit-pages)
8. [Configuration Files](#configuration-files)
9. [Usage Examples](#usage-examples)
10. [Integration Guide](#integration-guide)

## Overview

The Prompt Engineering Tool is a comprehensive Streamlit application designed to help users learn and experiment with different prompt engineering techniques across multiple language models. The application provides an interactive interface for applying various prompting strategies and observing their effects on model responses.

### Key Features
- Support for multiple LLMs (GPT-4o, GPT-4, GPT-3.5, o1-preview, o1-mini, etc.)
- Six different prompt engineering techniques
- Department-specific example prompts
- Real-time model parameter adjustment
- Audio-to-text prompt conversion
- Advanced role assignment and formatting options

---

## Core Modules

### Main Application (src/app.py)

The main Streamlit application that orchestrates all components and provides the user interface.

#### Key Functions

##### `audio_to_text(audio_file)`
Transcribes audio files using OpenAI's Whisper API with automatic chunking for large files.

**Parameters:**
- `audio_file` (file-like object): Audio file to transcribe

**Returns:**
- `str`: Transcribed text from the audio

**Example:**
```python
# Usage within Streamlit
audio_recording = st.audio_input("Record audio")
if audio_recording:
    transcribed_text = audio_to_text(audio_recording)
    st.write(f"Transcription: {transcribed_text}")
```

**Features:**
- Automatic file size detection and chunking
- Support for various audio formats
- Error handling for rate limits and file size issues

##### Main UI Components

**Model Selection Interface:**
```python
# Model selection with parameters
selected_model = st.sidebar.selectbox("Select Model", list(MODELS.keys()))
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.01)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 1.0, 0.01)
max_tokens = st.sidebar.slider("Max Length", 10, 500, 150, 10)
```

**Advanced Settings:**
- Role assignment (Technical Specialist, Editor, Marketing Manager, etc.)
- Thinking step inclusion
- Hallucination avoidance prompts
- Output format selection (Text, JSON, Bullet Points)
- Tone selection (Formal, Casual, Technical)

---

## Models Module

### Models Module (src/models.py)

Handles all interactions with language model APIs and response processing.

#### Constants

##### `MODELS`
Dictionary mapping user-friendly model names to API model identifiers.

```python
MODELS = {
    "GPT-4o": "gpt-4o",
    "GPT-4o mini": "gpt-4o-mini",
    "GPT-4 Turbo": "gpt-4-turbo",
    "GPT-4": "gpt-4",
    "GPT-3.5": "gpt-3.5-turbo",
    "o1": "o1",
    "o1-mini": "o1-mini",
    "o3-mini": "o3-mini",
    "GPT-4.5-preview": "gpt-4.5-preview"
}
```

#### Functions

##### `is_complete_sentence(text)`
Checks if text ends with a complete sentence.

**Parameters:**
- `text` (str): Text to check

**Returns:**
- `bool`: True if text ends with '.', '!', or '?'

**Example:**
```python
# Check if response is complete
if is_complete_sentence(response_text):
    print("Response is complete")
else:
    print("Response may be truncated")
```

##### `ensure_complete_ending(text)`
Ensures text has a complete ending, adding a professional closing if incomplete.

**Parameters:**
- `text` (str): Text to process

**Returns:**
- `str`: Text with complete ending

**Example:**
```python
incomplete_text = "Thank you for your inquiry, we will"
complete_text = ensure_complete_ending(incomplete_text)
# Result: "Thank you for your inquiry, we will Thank you for your understanding and support. Sincerely, [Your Company Name] Customer Support Team."
```

##### `get_model_response(model, prompt, temperature=None, top_p=None, max_tokens=None)`
Main function for generating responses from language models with streaming support.

**Parameters:**
- `model` (str): Model identifier (from MODELS dict)
- `prompt` (str): Input prompt for the model
- `temperature` (float, optional): Controls randomness (0.0-1.0)
- `top_p` (float, optional): Controls diversity (0.0-1.0)  
- `max_tokens` (int, optional): Maximum tokens to generate

**Returns:**
- `Generator[str]`: Streaming response chunks
- `str`: Complete response (when not streaming)

**Special Handling:**
- **o1 models**: Automatically uses `max_completion_tokens` instead of `max_tokens`
- **o1 models**: Forces `temperature=1` and `top_p=1` (o1 limitations)
- **Rate limiting**: Automatic retry with exponential backoff
- **Completeness**: Ensures responses end with complete sentences

**Example:**
```python
# Basic usage
response = get_model_response(
    model="gpt-4o",
    prompt="Explain quantum computing",
    temperature=0.7,
    max_tokens=200
)

# Streaming usage (for Streamlit)
def stream_response():
    for chunk in get_model_response("gpt-4o", prompt):
        yield chunk

st.write_stream(stream_response())
```

---

## Prompt Engineering Module

### Prompt Engineering Module (src/prompt_engineering.py)

Implements various prompt engineering techniques with detailed explanations.

#### Functions

##### `apply_technique(prompt, technique)`
Applies the selected prompt engineering technique to the input prompt.

**Parameters:**
- `prompt` (str): Original user prompt
- `technique` (str): Technique name (see available techniques below)

**Returns:**
- `tuple`: (transformed_prompt, explanation)

**Available Techniques:**

1. **Zero-Shot Prompting**
   ```python
   prompt, explanation = apply_technique("What is AI?", "Zero-Shot")
   # Returns the prompt unchanged with explanation
   ```

2. **Few-Shot Prompting**
   ```python
   prompt, explanation = apply_technique("How to make coffee?", "Few-Shot")
   # Adds examples before the prompt
   ```

3. **Chain-of-Thought Prompting**
   ```python
   prompt, explanation = apply_technique("Solve: 2+2*3", "Chain-of-Thought")
   # Prepends "Let's think step-by-step.\n"
   ```

4. **Meta-Prompting**
   ```python
   prompt, explanation = apply_technique("Write an email", "Meta-Prompting")
   # Asks model to create a better prompt first
   ```

5. **Self-Consistency Prompting**
   ```python
   prompt, explanation = apply_technique("Explain gravity", "Self-Consistency")
   # Instructs model to ensure consistency
   ```

6. **Tree-of-Thought Prompting**
   ```python
   prompt, explanation = apply_technique("Plan a project", "Tree-of-Thought")
   # Encourages exploring multiple approaches
   ```

**Complete Example:**
```python
from prompt_engineering import apply_technique

# Apply Chain-of-Thought to a math problem
original_prompt = "What is 15% of 240?"
transformed_prompt, explanation = apply_technique(original_prompt, "Chain-of-Thought")

print(f"Original: {original_prompt}")
print(f"Transformed: {transformed_prompt}")
print(f"Explanation: {explanation}")

# Output:
# Original: What is 15% of 240?
# Transformed: Let's think step-by-step.
# What is 15% of 240?
# Explanation: Chain-of-Thought Prompting: The prompt instructs the model to articulate its reasoning process step-by-step...
```

---

## Utils Module

### Utils Module (src/utils.py)

Provides utility functions for loading configuration data and managing file paths.

#### Functions

##### `load_techniques(filename='data/techniques.json')`
Loads prompt engineering techniques and their descriptions from a JSON configuration file.

**Parameters:**
- `filename` (str): Path to techniques JSON file (relative to project root)

**Returns:**
- `dict`: Dictionary containing technique definitions

**Raises:**
- `FileNotFoundError`: If the techniques file doesn't exist

**File Structure Expected:**
```json
{
    "Zero-Shot Prompting": {
        "description": "Technique description...",
        "process": ["Step 1", "Step 2", "Step 3"]
    },
    "Few-Shot Prompting": {
        "description": "Technique description...",
        "process": ["Step 1", "Step 2", "Step 3"]
    }
}
```

**Example:**
```python
from utils import load_techniques

try:
    techniques = load_techniques()
    print(f"Available techniques: {list(techniques.keys())}")
    
    # Access specific technique
    cot_info = techniques["Chain-of-Thought"]
    print(f"Description: {cot_info['description']}")
    print(f"Process steps: {cot_info['process']}")
    
except FileNotFoundError as e:
    print(f"Configuration file not found: {e}")
```

##### `load_prompts(filename='data/departments_prompts.json')`
Loads department-specific example prompts from a JSON configuration file.

**Parameters:**
- `filename` (str): Path to prompts JSON file (relative to project root)

**Returns:**
- `dict`: Dictionary mapping departments to lists of example prompts

**Raises:**
- `FileNotFoundError`: If the prompts file doesn't exist

**File Structure Expected:**
```json
{
    "Marketing": [
        "Write a product description...",
        "Create a social media campaign...",
        "Develop a brand strategy..."
    ],
    "Customer Support": [
        "Draft a response to...",
        "Create a help article...",
        "Design an FAQ section..."
    ]
}
```

**Example:**
```python
from utils import load_prompts

try:
    prompts_data = load_prompts()
    
    # List available departments
    departments = list(prompts_data.keys())
    print(f"Available departments: {departments}")
    
    # Get prompts for specific department
    marketing_prompts = prompts_data["Marketing"]
    print(f"Marketing prompts: {len(marketing_prompts)} available")
    
    for i, prompt in enumerate(marketing_prompts):
        print(f"{i+1}. {prompt[:50]}...")
        
except FileNotFoundError as e:
    print(f"Prompts file not found: {e}")
```

---

## Machine Learning Module

### Machine Learning Module (src/machine_learning.py)

Provides specialized ML-focused implementations of prompt engineering techniques.

⚠️ **Note**: This module uses the deprecated `openai.Completion.create()` API and should be updated to use `openai.ChatCompletion.create()` for production use.

#### Functions

##### `apply_few_shot_prompting(user_prompt)`
Applies Few-Shot prompting with predefined examples for question-answering tasks.

**Parameters:**
- `user_prompt` (str): User's question or prompt

**Returns:**
- `str`: Model response following few-shot pattern

**Example:**
```python
response = apply_few_shot_prompting("What is the capital of Italy?")
# Uses predefined Q&A examples to format the response
```

##### `apply_zero_shot_prompting(user_prompt)`
Applies Zero-Shot prompting with direct question format.

**Parameters:**
- `user_prompt` (str): User's question or prompt

**Returns:**
- `str`: Direct model response

##### `apply_chain_of_thought_prompting(user_prompt)`
Applies Chain-of-Thought prompting with step-by-step reasoning instruction.

**Parameters:**
- `user_prompt` (str): Problem or question requiring reasoning

**Returns:**
- `str`: Model response with explicit reasoning steps

##### `apply_meta_prompting(user_prompt)`
Applies Meta-Prompting by asking the model to generate a better prompt.

**Parameters:**
- `user_prompt` (str): Original prompt or problem statement

**Returns:**
- `str`: Improved prompt generated by the model

##### `apply_self_consistency_prompting(user_prompt)`
Applies Self-Consistency prompting to ensure coherent responses.

**Parameters:**
- `user_prompt` (str): User's prompt

**Returns:**
- `str`: Consistent and coherent response

##### `apply_tree_of_thought_prompting(user_prompt)`
Applies Tree-of-Thought prompting to explore multiple solution approaches.

**Parameters:**
- `user_prompt` (str): Problem requiring multiple approaches

**Returns:**
- `str`: Response exploring different solution paths

**Usage Example:**
```python
from machine_learning import apply_chain_of_thought_prompting

# For complex reasoning tasks
problem = "A store sells apples for $2 each and oranges for $3 each. If someone buys 5 apples and 3 oranges, how much do they spend?"
response = apply_chain_of_thought_prompting(problem)
print(response)
# Model will show step-by-step calculation
```

---

## Streamlit Pages

### Home Page (pages/Home.py)

Provides an overview of the application with setup instructions and feature descriptions.

#### Content Sections:
- **Prerequisites**: Required knowledge and tools
- **About**: Course context and purpose
- **Features**: Key application capabilities
- **Usage**: Step-by-step instructions
- **Feedback**: User feedback collection
- **Disclaimer**: Project status and educational context

#### Usage:
```python
# Access via Streamlit multipage navigation
# URL: /Home or as default page
```

### About Page (pages/About.py)

Educational content about the prompt engineering course and its objectives.

#### Content Sections:
- **Course Description**: Fundamentals and advanced techniques
- **Course Objectives**: Learning goals and outcomes
- **Target Audience**: Ideal participants and prerequisites

#### Usage:
```python
# Access via Streamlit sidebar navigation
# URL: /About
```

---

## Configuration Files

### Techniques Configuration (data/techniques.json)

Defines all available prompt engineering techniques with descriptions and process steps.

#### Structure:
```json
{
    "Technique Name": {
        "description": "Detailed explanation of the technique",
        "process": [
            "Step 1: Description",
            "Step 2: Description", 
            "Step 3: Description"
        ]
    }
}
```

#### Available Techniques:
1. **Zero-Shot Prompting**: Direct prompts without examples
2. **Few-Shot Prompting**: Prompts with example demonstrations
3. **Chain-of-Thought Prompting**: Step-by-step reasoning guidance
4. **Meta-Prompting**: Model-generated prompt refinement
5. **Self-Consistency Prompting**: Ensuring logical coherence
6. **Tree-of-Thought Prompting**: Multiple reasoning path exploration

### Departments Configuration (data/departments_prompts.json)

Contains example prompts organized by business departments.

#### Available Departments:
1. **Customer Services & Fulfillment**
2. **Editorial/Publishing**
3. **Marketing**
4. **Operations/Other**
5. **Branding & Design**
6. **Corporate Communications**
7. **Production**
8. **Publishing Process Management**

#### Usage Example:
```json
{
    "Marketing": [
        "Write a compelling description for an upcoming release of a new academic textbook on neuroscience.",
        "Develop a social media campaign strategy to promote the latest issue of our academic journal.",
        "Develop a machine learning model to predict the success of social media campaigns promoting academic publications."
    ]
}
```

---

## Usage Examples

### Basic Prompt Engineering Workflow

```python
from src.utils import load_techniques, load_prompts
from src.prompt_engineering import apply_technique
from src.models import get_model_response

# 1. Load configurations
techniques = load_techniques()
prompts_data = load_prompts()

# 2. Select components
department = "Marketing"
prompt = prompts_data[department][0]  # First marketing prompt
technique = "Chain-of-Thought"

# 3. Apply technique
transformed_prompt, explanation = apply_technique(prompt, technique)

# 4. Generate response
response = get_model_response(
    model="gpt-4o",
    prompt=transformed_prompt,
    temperature=0.7,
    max_tokens=200
)

print(f"Original: {prompt}")
print(f"Transformed: {transformed_prompt}")
print(f"Response: {response}")
```

### Advanced Configuration Example

```python
# Configure advanced prompt with all options
base_prompt = "Explain quantum computing to a beginner"
technique = "Few-Shot"

# Apply technique
transformed_prompt, _ = apply_technique(base_prompt, technique)

# Add formatting and role
role = "Technical Trainer"
output_format = "Bullet Points"
tone = "Casual"

# Construct full prompt
full_prompt = f"{transformed_prompt}\n\n"
full_prompt += f"Format the output in {output_format} format with a {tone} tone.\n"
full_prompt += f"Role: {role}.\n"
full_prompt += "\n### Thinking Step\n<thinking>Explain step-by-step the reasoning behind the output.</thinking>"
full_prompt += "\nIf you don't know, state 'I don't know.' Use <Reference></Reference> to pull the reference you used to produce an output."

# Generate response with specific parameters
response = get_model_response(
    model="gpt-4o",
    prompt=full_prompt,
    temperature=0.5,    # Lower for more consistency
    top_p=0.9,         # Slightly focused sampling
    max_tokens=300
)
```

### Audio Processing Integration

```python
import streamlit as st
from src.app import audio_to_text

# In Streamlit app context
audio_recording = st.audio_input("Record your prompt")

if audio_recording:
    # Transcribe audio to text
    transcribed_prompt = audio_to_text(audio_recording)
    
    # Apply prompt engineering
    transformed_prompt, explanation = apply_technique(
        transcribed_prompt, 
        "Meta-Prompting"
    )
    
    # Generate response
    response = get_model_response("gpt-4o", transformed_prompt)
    
    st.write(f"Transcribed: {transcribed_prompt}")
    st.write(f"Response: {response}")
```

---

## Integration Guide

### Setting Up the Application

1. **Environment Setup:**
```bash
pip install -r requirements.txt
```

2. **API Configuration:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. **Running the Application:**
```bash
streamlit run src/app.py
```

### Extending the Application

#### Adding New Models

1. Update `MODELS` dictionary in `src/models.py`:
```python
MODELS = {
    # ... existing models ...
    "New Model": "new-model-api-id"
}
```

2. Add model-specific handling in `get_model_response()` if needed:
```python
if model in ["new-model-api-id"]:
    # Special handling for new model
    request_params["custom_parameter"] = value
```

#### Adding New Techniques

1. Update `data/techniques.json`:
```json
{
    "New Technique": {
        "description": "Description of the new technique",
        "process": [
            "Step 1: First action",
            "Step 2: Second action"
        ]
    }
}
```

2. Add implementation in `src/prompt_engineering.py`:
```python
def apply_technique(prompt, technique):
    if technique == "New Technique":
        transformed_prompt = f"Special instruction: {prompt}"
        explanation = "New Technique: Applies special instructions..."
        return transformed_prompt, explanation
    # ... existing techniques ...
```

#### Adding New Departments

Update `data/departments_prompts.json`:
```json
{
    "New Department": [
        "Example prompt 1 for new department",
        "Example prompt 2 for new department",
        "Example prompt 3 for new department"
    ]
}
```

### API Integration

For external integration, you can use the core functions independently:

```python
# Import required modules
from src.prompt_engineering import apply_technique
from src.models import get_model_response
from src.utils import load_techniques

# Load configurations
techniques = load_techniques()

# Use in your application
def generate_enhanced_response(user_input, technique_name="Chain-of-Thought"):
    # Apply prompt engineering
    enhanced_prompt, explanation = apply_technique(user_input, technique_name)
    
    # Generate response
    response = get_model_response(
        model="gpt-4o",
        prompt=enhanced_prompt,
        temperature=0.7
    )
    
    return {
        "original_prompt": user_input,
        "enhanced_prompt": enhanced_prompt,
        "technique_explanation": explanation,
        "response": response
    }
```

### Error Handling Best Practices

```python
import logging
from src.models import get_model_response

def safe_model_call(model, prompt, **kwargs):
    try:
        response = get_model_response(model, prompt, **kwargs)
        return {"success": True, "response": response}
    except Exception as e:
        logging.error(f"Model call failed: {str(e)}")
        return {"success": False, "error": str(e)}

# Usage
result = safe_model_call("gpt-4o", "Your prompt here")
if result["success"]:
    print(result["response"])
else:
    print(f"Error: {result['error']}")
```

---

## Conclusion

This documentation covers all public APIs, functions, and components in the Prompt Engineering Tool. The modular design allows for easy extension and integration into other applications. For additional support or questions, refer to the project's GitHub repository or contact the maintainers.

**Key Points:**
- All functions include comprehensive error handling
- The application supports multiple LLM providers and models
- Configuration is externalized for easy customization
- Real-time streaming is supported for better user experience
- Audio input capabilities extend accessibility