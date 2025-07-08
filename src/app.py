"""app.py - Streamlit UI for Interactive Prompt Engineering Tool

This is the main entry point for the web application that allows users to experiment with prompt engineering techniques.
It provides a user-friendly interface for selecting models, techniques, and prompts, and generates responses from

Features include:
- Model selection from a predefined list of OpenAI models.
- Technique selection to apply various prompt engineering strategies.   
- Input fields for user prompts, model parameters, and advanced settings.
- Real-time streaming of model responses.
- Audio input for prompts with transcription capabilities.
- Detailed explanations of the transformations applied to the prompts

This app is part of a larger educational and research initiative to make prompt engineering accessible and practical for users."""

# src/app.py
import streamlit as st
from prompt_engineering import apply_technique
from models import get_model_response, MODELS, sanitize_user_input, validate_model_selection
from utils import load_techniques, load_prompts
import os
import mimetypes
#import speech_recognition as sr  # For speech-to-text
from io import BytesIO  # To handle audio data
from pydub import AudioSegment
import tempfile
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Security configuration constants
MAX_AUDIO_SIZE = 25 * 1024 * 1024  # 25MB limit for audio files
MAX_PROMPT_LENGTH = 5000  # Maximum prompt length
ALLOWED_AUDIO_TYPES = ['audio/mpeg', 'audio/wav', 'audio/mp3', 'audio/m4a']

# Audio processing constants
WHISPER_MODEL = "whisper-1"
AUDIO_RESPONSE_FORMAT = "text"

# Set the page configuration
st.set_page_config(
    page_title="Prompt Engineering",  # Title of the tab in the browser
    page_icon="📊",                 # An optional emoji or icon
    layout="wide"                   # Optional layout setting
)



# import streamlit.components.v1 as components
# #########
# def typewrite(text: str):
#     # Load external assets (CSS and JavaScript)
#     with open("../assets/style.css") as f:
#         css = f.read()

#     with open("../assets/main.js") as f:
#         js = f.read()

#     # HTML structure for the typewriting effect
#     html = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <style>
#             {css}
#         </style>
#     </head>
#     <body>
#         <p id="typewrite" data-content="" ;">{text}</p>
#         <script>
#             {js}
#         </script>
#     </body>
#     </html>
#     """
#     return html


# # Text to display
# display_text = """Welcome to this Prompt Engineering app!...Did you know?
# A clear and explicit prompt can reduce errors and improve output quality.
# Using ‘temperature’? Higher values increase creativity, while lower values improve consistency.
# Great prompts are specific, structured, and goal-oriented—clarity is key!"""

# typewrite_html = typewrite(display_text)

# # Render the streaming text in the app
# components.html(typewrite_html, height=100)

#########



#st.snow()
# Load data
techniques = load_techniques()
prompts_data = load_prompts()

# Streamlit sidebar for user selection
st.sidebar.title(":streamlit: Prompt Engineering Tool")

# Description of the app
st.sidebar.write("This tool is designed to help you explore and learn prompt engineering techniques using various models like o1, o1-mini, GPT-4o, GPT-4o-mini, GPT-4 Turbo, and more.")

# Add this note to the sidebar:
st.sidebar.write("Accuracy, correctness, or appropriateness cannot be guaranteed.")

st.sidebar.write(
       "Built by [Natasha Newbold](https://www.linkedin.com/in/natasha-newbold/) "
            )

# Check if API key is provided
if os.getenv("OPENAI_API_KEY"):
    st.sidebar.success("✅ API key already provided!")
else:
    st.sidebar.error("❌ API key not provided. Please set your OpenAI API key.")

#####
#####

#####
#####

# Model selection
selected_model = st.sidebar.selectbox("Select Model", list(MODELS.keys()))
model_engine = MODELS[selected_model]

####
# Parameters sliders for model customization with descriptions
st.sidebar.subheader("Model Parameters")

# Temperature slider with explanation
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.01,
    help=(
        "Controls the randomness of the model's output. "
        "Lower values make the output more deterministic and focused, "
        "suitable for fact-based QA. Higher values increase creativity, "
        "ideal for tasks like poem generation."
    )
)

# Top-p slider with explanation
top_p = st.sidebar.slider(
    "Top-p (Nucleus Sampling)",
    min_value=0.0,
    max_value=1.0,
    value=1.0,
    step=0.01,
    help=(
        "Controls the diversity of the model's output using nucleus sampling. "
        "Lower values focus on the most likely tokens, resulting in more factual responses. "
        "Higher values consider a wider range of possibilities, promoting diverse outputs."
    )
)

# Max Length slider with explanation
max_tokens = st.sidebar.slider(
    "Max Length",
    min_value=10,
    max_value=500,
    value=150,
    step=10,
    help=(
        "Specifies the maximum number of tokens to generate. "
        "Lower values restrict output length, making responses concise. "
        "Higher values allow for longer, more detailed responses, but may increase costs."
    )
)


####

# Department selection
selected_department = st.sidebar.selectbox("Select Department", list(prompts_data.keys()))

# Prompt selection
selected_prompt = st.sidebar.selectbox("Select Prompt", prompts_data[selected_department])

# Technique selection
selected_technique = st.sidebar.selectbox("Select Technique", list(techniques.keys()))

####
# Fetch the technique description and process steps
technique_info = techniques[selected_technique]
technique_description = technique_info["description"]
technique_process_steps = technique_info["process"]
####

# Output format selection
output_format = st.sidebar.selectbox(
    "Select Output Format",
    ["Text", "JSON", "Bullet Points"],
    help="Choose the format in which you want the output to be displayed."
)

# Tone selection
tone = st.sidebar.selectbox(
    "Select Tone",
    ["Formal", "Casual", "Technical"],
    help="Select the tone for the output text."
)

# Advanced Settings section with sliders and selection boxes
with st.sidebar.expander("Advanced Settings"):
    # Assigning Roles
    role = st.selectbox(
        "Assign Role",
        ["No Role", "Technical Specialist", "Editor", "Marketing Manager", "Technical Trainer", "Product Owner"],
        help="Select a role to simulate a specific perspective in the response."
    )

    # Thinking Step - Slider for demonstration purposes (1: Use, 0: Do not use)
    use_thinking_step = st.slider(
        "Include Thinking Step",
        min_value=0,
        max_value=1,
        value=0,
        step=1,
        format="%d",
        help="Enable (1) to include a 'Thinking Step' header to explicitly show the model's thought process."
    )

    # Avoid Hallucinations - Slider for demonstration purposes (1: Avoid, 0: Do not avoid)
    avoid_hallucinations = st.slider(
        "Avoid Hallucinations",
        min_value=0,
        max_value=1,
        value=0,
        step=1,
        format="%d",
        help="Enable (1) to prompt the model to state 'I don't know' if it lacks sufficient information."
    )


# Bottom of sidebar - Blog link and clear button
st.sidebar.markdown("---")

######
######



# Security validation functions
def validate_audio_file(audio_file):
    """
    Validate an uploaded audio file for security and processing requirements.
    
    This function performs comprehensive validation of audio files to ensure they
    meet security requirements and are suitable for transcription processing.
    It checks file size limits, detects empty files, and performs basic format validation.
    
    Args:
        audio_file: A file-like object representing the uploaded audio file.
                   Should support seek() and tell() operations for size checking.
                   Can be None for cases where no file is provided.
    
    Returns:
        tuple: A two-element tuple containing:
            - is_valid (bool): True if file passes all validation checks, False otherwise
            - message (str): Descriptive message explaining validation result or failure reason
    
    Validation Checks:
        - File existence (not None)
        - File size within MAX_AUDIO_SIZE limit (25MB)
        - File is not empty (size > 0 bytes)
        - Basic file type validation via Streamlit's built-in handlers
    
    Example:
        >>> is_valid, msg = validate_audio_file(uploaded_file)
        >>> if is_valid:
        ...     process_audio(uploaded_file)
        >>> else:
        ...     st.error(f"Validation failed: {msg}")
    
    Side Effects:
        - Modifies file pointer position (seeks to end and back to beginning)
        - Does not close or modify the file content
    
    Note:
        File size limit is configurable via MAX_AUDIO_SIZE constant.
        Streamlit handles most MIME type validation automatically.
    """
    if not audio_file:
        return False, "No audio file provided"
    
    # Check file size
    audio_file.seek(0, 2)  # Seek to end
    file_size = audio_file.tell()
    audio_file.seek(0)  # Reset to beginning
    
    if file_size > MAX_AUDIO_SIZE:
        return False, f"File too large. Maximum size: {MAX_AUDIO_SIZE // (1024*1024)}MB"
    
    if file_size == 0:
        return False, "Empty audio file"
    
    # Basic file type validation (Streamlit handles most validation)
    return True, "Valid"

def validate_model_parameters(temperature, top_p, max_tokens):
    """
    Validate model parameters are within safe and acceptable ranges.
    
    This function ensures that user-provided model parameters fall within
    the valid ranges expected by OpenAI's API to prevent errors and ensure
    predictable behavior. It validates the three main generation parameters.
    
    Args:
        temperature (float): Controls randomness in model output (0.0 to 1.0).
                           Lower values = more deterministic, higher = more creative.
        top_p (float): Controls nucleus sampling diversity (0.0 to 1.0).
                      Lower values = more focused, higher = more diverse.
        max_tokens (int): Maximum number of tokens to generate (1 to 1000).
                         Controls response length and API costs.
    
    Returns:
        tuple: A two-element tuple containing:
            - is_valid (bool): True if all parameters are within valid ranges
            - message (str): "Valid" if successful, or specific error message
    
    Validation Rules:
        - temperature: Must be between 0.0 and 1.0 (inclusive)
        - top_p: Must be between 0.0 and 1.0 (inclusive)  
        - max_tokens: Must be between 1 and 1000 (inclusive)
    
    Example:
        >>> is_valid, msg = validate_model_parameters(0.7, 1.0, 150)
        >>> if is_valid:
        ...     # Safe to use parameters
        ...     make_api_call(temperature=0.7, top_p=1.0, max_tokens=150)
        >>> else:
        ...     st.error(f"Parameter error: {msg}")
    
    Note:
        These ranges may be more restrictive than OpenAI's actual limits
        but provide safe defaults for most use cases.
    """
    if not (0.0 <= temperature <= 1.0):
        return False, "Temperature must be between 0.0 and 1.0"
    if not (0.0 <= top_p <= 1.0):
        return False, "Top-p must be between 0.0 and 1.0"
    if not (1 <= max_tokens <= 1000):
        return False, "Max tokens must be between 1 and 1000"
    return True, "Valid"

# Function to transcribe audio using OpenAI Whisper API
def audio_to_text(audio_file):
    """
    Securely transcribe audio files to text using OpenAI's Whisper API.
    
    This function handles the complete audio transcription workflow including
    validation, API calls, error handling, and automatic file chunking for
    large files. It includes comprehensive security measures and sanitization
    of transcribed content to prevent potential security issues.
    
    Args:
        audio_file: A file-like object containing audio data. Should be a valid
                   audio format supported by Whisper (mp3, wav, m4a, etc.).
                   File will be validated before processing.
    
    Returns:
        str: The transcribed text content, sanitized for security.
             Returns descriptive error message if transcription fails.
    
    Features:
        - Input validation and security checks
        - Automatic file chunking for oversized files (>25MB)
        - Comprehensive error handling with user-friendly messages
        - Output sanitization to prevent prompt injection
        - Support for multiple audio formats via Whisper API
    
    Error Handling:
        - Validation errors: Returns validation failure message
        - File too large: Automatically splits into chunks and processes
        - API errors: Returns sanitized error message
        - Processing errors: Returns generic error message (no sensitive data)
    
    Example:
        >>> transcribed = audio_to_text(uploaded_audio)
        >>> if not transcribed.startswith("Audio validation failed"):
        ...     st.write(f"Transcription: {transcribed}")
        >>> else:
        ...     st.error(transcribed)
    
    Side Effects:
        - Makes API calls to OpenAI Whisper service
        - May create temporary files for chunking large audio
        - Displays Streamlit warnings for chunking operations
        - Modifies file pointer position during processing
    
    Security Notes:
        - All transcribed content is sanitized via sanitize_user_input()
        - File validation prevents oversized or malicious uploads
        - Error messages are sanitized to prevent information disclosure
        - Temporary files are automatically cleaned up after processing
    """
    # Validate audio file first
    is_valid, validation_message = validate_audio_file(audio_file)
    if not is_valid:
        return f"Audio validation failed: {validation_message}"
    
    try:
        # Transcribe the audio file using new client syntax
        response = client.audio.transcriptions.create(
            model=WHISPER_MODEL,
            file=audio_file,
            response_format=AUDIO_RESPONSE_FORMAT
        )
        
        # Sanitize the transcribed text
        sanitized_response = sanitize_user_input(response)
        return sanitized_response
        
    except Exception as transcription_error:
        error_str = str(transcription_error)
        if "bytes" in error_str or "file size" in error_str.lower():
            st.warning("File is too large. Breaking it into smaller chunks...")
            audio_file.seek(0)
            try:
                audio = AudioSegment.from_file(audio_file, format="mp3")
                halfway_point = len(audio) // 2

                first_half = audio[:halfway_point]
                second_half = audio[halfway_point:]

                transcription_text = ""
                
                # Process first half
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as first_file:
                    first_half.export(first_file.name, format="mp3")
                    first_file.seek(0)
                    with open(first_file.name, "rb") as audio_chunk:
                        first_response = client.audio.transcriptions.create(
                            model=WHISPER_MODEL,
                            file=audio_chunk,
                            response_format=AUDIO_RESPONSE_FORMAT
                        )
                        transcription_text += sanitize_user_input(first_response)
                
                # Process second half
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as second_file:
                    second_half.export(second_file.name, format="mp3")
                    second_file.seek(0)
                    with open(second_file.name, "rb") as audio_chunk:
                        second_response = client.audio.transcriptions.create(
                            model=WHISPER_MODEL,
                            file=audio_chunk,
                            response_format=AUDIO_RESPONSE_FORMAT
                        )
                        transcription_text += sanitize_user_input(second_response)
                
                return transcription_text
            except Exception as chunk_error:
                return "An error occurred during audio processing. Please try a smaller file."
        else:
            return "An audio processing error occurred. Please try again with a different file."
    except Exception as general_error:
        # Log the actual error for debugging but don't expose it to users
        return "An unexpected error occurred during transcription. Please try again."

# Collapsible audio input section
with st.sidebar.expander("🎙️ Record an Audio Prompt", expanded=True):
    st.write("Record your audio prompt below:")
    
    # Audio recorder (placeholder for recording)
    st.caption("Record your audio.")
    audio_recording = st.audio_input("Record audio")

    audio_to_process = None
    if audio_recording:
        st.audio(audio_recording)
        audio_to_process = audio_recording
        st.success("Audio recorded successfully.")

    if audio_to_process:
        with st.spinner("Transcribing audio..."):
            try:
                # Handle transcription with security validation
                transcribed_text = audio_to_text(audio_to_process)
                
                # Check if transcription was successful
                if transcribed_text and not transcribed_text.startswith("Audio validation failed") and not transcribed_text.startswith("An error occurred"):
                    st.info(f"Copy Transcribed Text: {transcribed_text}")
                    
                    # Downloadable transcription
                    text_file = BytesIO()
                    text_file.write(transcribed_text.encode())
                    text_file.seek(0)
                    st.download_button(
                        label="Download Transcribed Text",
                        data=text_file,
                        file_name="transcribed_prompt.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(transcribed_text)  # Display the error message
            except Exception as e:
                st.error("An error occurred during audio processing. Please try again with a different file.")



######
######


# Main content
st.title("Interactive Prompt Engineering :balloon:")


# Add dropdown section using st.expander with updated wording
with st.expander("When to prompt engineer"):
    st.write("""
    Prompt engineering is highly effective for controlling performance benchmarks, but it’s not always the best solution for every issue. 
    Instead of relying on prompt engineering to fix everything, selecting the right model can sometimes offer quicker and more practical improvements.
    Explore the tips below for better prompt outputs.

    ### Best Practices
    These techniques range from broadly useful to more specific. Their impact depends on your use case:

    - **Be concise and explicit**: Use simple, direct prompts to reduce confusion.
    - **Provide examples**: Provide multiple examples to improve response accuracy.
    - **Allow the model time to reason**: Guide the model step-by-step for complex reasoning.
    - **Use XML tags**: Structure prompts with tags for better organisation.
    - **Assign a role to the model**: Assign a role to set the model's context.
    - **Pre-populate responses**: Start with part of an answer to guide the model.
    - **Link complex prompts**: Break tasks into smaller steps to handle complexity.

    ### Context Engineering & RAG Techniques (2024-2025)
    Modern prompt engineering increasingly relies on context management and external knowledge integration:

    - **Contextual Prompt Chaining**: Link multiple prompts with shared context to maintain coherence across complex tasks.
    - **Dynamic Context Windows**: Adjust context based on query complexity and available token limits.
    - **Retrieval-Augmented Generation (RAG)**: Combine external knowledge sources with prompts for accurate, up-to-date responses.
    - **Multi-Modal Context**: Integrate text, images, and other data types for comprehensive understanding.
    - **Context Compression**: Optimize token usage while preserving essential meaning and context.
    - **Adaptive Context**: Real-time context modification based on user feedback and interaction patterns.

    ### Effective Prompting for O1 Models
    O1 models differ from GPT-4o or Claude 3.5 Sonnet, excelling in chain-of-thought reasoning without explicit guidance. Follow these practices for optimal results:
    
    - Use concise, clear prompts; avoid unnecessary detail.
    - Skip chain-of-thought instructions; the model reasons internally.
    - Define input parts clearly using delimiters (e.g., triple quotes, XML tags).
    - Provide only essential context in retrieval-augmented generation (RAG).
    
    **Source:**
    Anthropic. [*Prompt engineering techniques*](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
    """)

# New dropdown with additional resources
with st.expander("Additional Resources"):
    st.markdown("""
    ### Overview
    This project is part of a larger body of work around a comprehensive Generative AI course, designed to provide in-depth knowledge and hands-on experience with AI models.
    
    **Explore the following resources to enhance your understanding:**
    
    - [Glossary](https://natnew.github.io/Awesome-Prompt-Engineering/AI_Glossary.html): Understand the key terms and concepts used in AI and prompt engineering.
    - [Best Practices](https://generative-ai-hub.gitbook.io/awesomegenerativeai): Learn the best practices for designing and using prompts effectively.
    - [Use Cases](https://generative-ai-hub.gitbook.io/awesomegenerativeai): Discover various use cases where prompt engineering can make a significant impact.
    - [Ethical Guidelines](https://ethicsinai.streamlit.app/): Understand the ethical considerations and guidelines for using AI responsibly.
    - [Conspiracy Generator](https://conspiracy-generation.streamlit.app/): Explore the ethical implications of narrative manipulation with our AI tool that turns any story into a conspiracy theory.
    - [Chat with Hugging Face Zephyr 7b](https://huggingface.co/spaces/NatashaN/chatbot_retry_undo_like): Explore a modern chatbot interface with the Hugging Face Zephyr 7b model, which allows users to interact dynamically with individual chat messages.
    - [ArXiv CS RAG](https://huggingface.co/spaces/NatashaN/Arxiv-CS-RAG): Leverage the ArXiv CS Retrieval-Augmented Generator (RAG) to explore cutting-edge research in computer science.
    """, unsafe_allow_html=True)

# Advanced Reasoning Techniques dropdown
with st.expander("🧠 Advanced Reasoning & Control Techniques"):
    st.markdown("""
    ### Advanced Reasoning Patterns
    Cutting-edge techniques for complex problem-solving and decision-making:

    - **Program-Aided Language Models (PAL)**: Combine code generation with reasoning to solve mathematical and logical problems.
    - **Reflection Prompting**: Enable self-correction and iterative improvement through explicit reflection steps.
    - **Constitutional AI**: Generate value-aligned responses through principle-based prompting and self-correction.
    - **Debate Prompting**: Use multiple perspectives and internal debate for complex decision-making processes.
    - **Analogical Reasoning**: Leverage analogies and metaphors for better problem understanding and explanation.
    - **Metacognitive Prompting**: Explicitly prompt the model to think about its own thinking process.

    ### Control & Optimization Techniques
    Advanced methods for fine-tuning model behavior and output quality:

    - **Temperature Scheduling**: Dynamic temperature adjustment during generation for optimal creativity vs. accuracy balance.
    - **Prompt Optimization via Gradient Descent**: Automated prompt improvement using optimization algorithms.
    - **Multi-Agent Prompting**: Coordinate multiple AI agents with different roles for complex task completion.
    - **Prompt Ensembles**: Combine multiple prompt variations for increased robustness and reliability.
    - **Adaptive Prompting**: Real-time prompt modification based on feedback and performance metrics.
    - **Constraint-Based Prompting**: Use explicit constraints to guide model behavior within specific boundaries.

    ### Implementation Tips
    - **Start Simple**: Begin with basic techniques before implementing advanced patterns.
    - **Measure Impact**: Track performance improvements when adding complexity.
    - **Context Awareness**: Consider computational costs and token limits when implementing these techniques.
    - **Iterative Refinement**: Continuously refine prompts based on output quality and user feedback.
    """)


st.subheader("Selected Prompt")
user_prompt = st.text_area(
    "See/Type your prompt below:", 
    value=selected_prompt,
    max_chars=MAX_PROMPT_LENGTH,
    help=f"Maximum {MAX_PROMPT_LENGTH} characters allowed for security reasons."
)

# Validate and sanitize the user prompt
if user_prompt:
    if len(user_prompt) > MAX_PROMPT_LENGTH:
        st.error(f"Prompt too long. Maximum {MAX_PROMPT_LENGTH} characters allowed.")
        st.stop()
    
    # Sanitize the user input
    sanitized_user_prompt = sanitize_user_input(user_prompt)
    if not sanitized_user_prompt:
        st.error("Invalid prompt detected. Please modify your input.")
        st.stop()
    
    if sanitized_user_prompt != user_prompt:
        st.warning("⚠️ Some content was filtered from your prompt for security reasons.")
else:
    sanitized_user_prompt = ""

# Apply technique to the prompt and consider output format and tone
transformed_prompt, transformation_explanation = apply_technique(sanitized_user_prompt, selected_technique)

# Adjust the transformed prompt based on output format and tone
formatted_prompt = f"{transformed_prompt}\n\nFormat the output in {output_format} format with a {tone} tone."

# Apply advanced settings
if role != "No Role":
    formatted_prompt += f"\n\nRole: {role}."

# Ensure the Thinking Step is reflected with a header
if use_thinking_step == 1:
    formatted_prompt += "\n\n### Thinking Step\n<thinking>Explain step-by-step the reasoning behind the output.</thinking>"

if avoid_hallucinations == 1:
    formatted_prompt += "\n\nIf you don't know, state 'I don't know.' Use <Reference></Reference> to pull the reference you used to produce an output."

st.subheader("Transformed Prompt")
#st.info(formatted_prompt)


####
# Prepare the technique process text
process_text = "\n".join(technique_process_steps)
# Replace placeholders with actual values using sanitized prompt
process_text = process_text.replace("[PROMPT]", sanitized_user_prompt).replace("[TECHNIQUE]", selected_technique)

# Combine the description and process
combined_text = f"{technique_description}\n\n{process_text}"

# Display the combined text in the "Transformed Prompt" info box
st.info(combined_text)
####


# Detailed transformation explanation
detailed_explanation = f"""
The following transformation was applied using the **{selected_technique}** technique with the specified parameters:
- **Output Format**: {output_format}
- **Tone**: {tone}
- **Temperature**: {temperature} - This controls the randomness of the output. A lower value means more deterministic responses, while a higher value introduces more creativity.
- **Top-P (Nucleus Sampling)**: {top_p} - This parameter determines the diversity of the output. Lower values limit responses to the most likely tokens, while higher values allow for more diverse outputs.
- **Max Length**: {max_tokens} tokens - This defines the maximum number of tokens generated in the response, controlling the response length and ensuring it does not exceed the specified limit.
- **Role**: {role} - Simulates the perspective of a specific role.
- **Thinking Step**: {"Enabled" if use_thinking_step == 1 else "Disabled"} - A 'Thinking Step' header is included to explicitly show the model's thought process.
- **Avoid Hallucinations**: {"Enabled" if avoid_hallucinations == 1 else "Disabled"} - Instructs the model to avoid guessing and provide references.
"""

st.subheader("Transformation Explanation")
st.info(detailed_explanation)

# Get model response with real-time streaming
if st.button("Generate Response"):
    # Validate model parameters
    param_valid, param_message = validate_model_parameters(temperature, top_p, max_tokens)
    if not param_valid:
        st.error(f"Invalid parameters: {param_message}")
        st.stop()
    
    # Validate model selection
    try:
        validated_model = validate_model_selection(model_engine)
    except ValueError as e:
        st.error(f"Invalid model selection: {e}")
        st.stop()
    
    st.subheader("Model Response")

    # Generate response with validated inputs
    response = get_model_response(
        validated_model,
        formatted_prompt,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )
    
    if response:
        st.write(response)
    else:
        st.error("Failed to generate response. Please try again.")


