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
from models import get_model_response, MODELS
from utils import load_techniques, load_prompts
import os
#import speech_recognition as sr  # For speech-to-text
from io import BytesIO  # To handle audio data
from pydub import AudioSegment
import tempfile
import openai
import time


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
selected_model_engine = MODELS[selected_model]

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
technique_description = techniques[selected_technique]["description"]

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



# Function to transcribe audio using OpenAI Whisper API
def audio_to_text(audio_file):
    try:
        # Transcribe the audio file
        response = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
        return response
    except openai.error.InvalidRequestError as e:
        if "bytes" in str(e):
            st.warning("File is too large. Breaking it into smaller chunks...")
            audio_file.seek(0)
            audio = AudioSegment.from_file(audio_file, format="mp3")
            halfway_point = len(audio) // 2

            first_half = audio[:halfway_point]
            second_half = audio[halfway_point:]

            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as first_file, \
                 tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as second_file:
                first_half.export(first_file.name, format="mp3")
                second_half.export(second_file.name, format="mp3")
                first_file.seek(0)
                second_file.seek(0)

                transcription_text = ""
                with open(first_file.name, "rb") as f:
                    transcription_text += openai.Audio.transcribe(
                        model="whisper-1",
                        file=f,
                        response_format="text"
                    )
                with open(second_file.name, "rb") as f:
                    transcription_text += openai.Audio.transcribe(
                        model="whisper-1",
                        file=f,
                        response_format="text"
                    )
            return transcription_text
        else:
            return f"An error occurred: {e}"

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
                # Handle transcription
                transcribed_text = audio_to_text(audio_to_process)
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
            except Exception as e:
                st.error(f"An error occurred: {e}")



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


st.subheader("Selected Prompt")
user_prompt = st.text_area("See/Type your prompt below:", value=selected_prompt)

# Apply technique to the prompt and consider output format and tone
transformed_prompt, transformation_explanation = apply_technique(user_prompt, selected_technique)

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
# Replace placeholders with actual values
process_text = process_text.replace("[PROMPT]", user_prompt).replace("[TECHNIQUE]", selected_technique)

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
    st.subheader("Model Response")

    def stream_response():
        try:
            for chunk in get_model_response(
                selected_model_engine,
                formatted_prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            ):
                yield chunk
                time.sleep(0.02)  # Optional: Simulate a delay for better streaming experience
        except Exception as e:
            yield f"Error generating response: {str(e)}"

    # Stream the response in real-time
    st.write_stream(stream_response())


