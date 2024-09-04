# src/app.py
import streamlit as st
from prompt_engineering import apply_technique
from models import get_model_response, MODELS
from utils import load_techniques, load_prompts
import os


# Load data
techniques = load_techniques()
prompts_data = load_prompts()

# Streamlit sidebar for user selection
st.sidebar.title("📊 Prompt Engineering Tool")

# Description of the app
st.sidebar.write("This tool is designed to help you explore and learn prompt engineering techniques using various models like GPT-4o, GPT-4 Turbo, and more.")

# Check if API key is provided
if os.getenv("OPENAI_API_KEY"):
    st.sidebar.success("✅ API key already provided!")
else:
    st.sidebar.error("❌ API key not provided. Please set your OpenAI API key.")

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

# Bottom of sidebar - Blog link and clear button
st.sidebar.markdown("---")
st.sidebar.markdown("📖 **Learn how to build this app in this [blog](https://example.com/blog).**")

# Main content
st.title("Interactive Prompt Engineering")

# Add dropdown section using st.expander with updated wording
with st.expander("When to prompt engineer"):
    st.write("""
    This guide highlights success the criteria that can be influenced through prompt engineering. 
    However, not all success criteria or failed evaluations are best addressed by prompt engineering. 
    For example, issues such as latency and cost may sometimes be more effectively improved by selecting a different model.
    """)

st.subheader("Selected Prompt")
user_prompt = st.text_area("Edit your prompt below:", value=selected_prompt)

st.subheader("Technique Description")
st.info(technique_description)

# Apply technique to the prompt and consider output format and tone
transformed_prompt, transformation_explanation = apply_technique(user_prompt, selected_technique)

# Adjust the transformed prompt based on output format and tone
formatted_prompt = f"{transformed_prompt}\n\nFormat the output in {output_format} format with a {tone} tone."

st.subheader("Transformed Prompt")
st.info(formatted_prompt)

# Create a detailed transformation explanation
detailed_explanation = f"""
The following transformation was applied using the **{selected_technique}** technique with the specified parameters:
- **Output Format**: {output_format}
- **Tone**: {tone}
- **Temperature**: {temperature} - This controls the randomness of the output. A lower value means more deterministic responses, while a higher value introduces more creativity.
- **Top-P (Nucleus Sampling)**: {top_p} - This parameter determines the diversity of the output. Lower values limit responses to the most likely tokens, while higher values allow for more diverse outputs.
- **Max Length**: {max_tokens} tokens - This defines the maximum number of tokens generated in the response, controlling the response length and ensuring it does not exceed the specified limit.
"""

st.subheader("Transformation Explanation")
st.info(detailed_explanation)

# Get model response with complete sentence enforcement
if st.button("Generate Response"):
    with st.spinner("Generating response..."):
        response = get_model_response(
            selected_model_engine,
            formatted_prompt,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens
        )
    if response:
        st.subheader("Model Response")
        st.write(response)
    else:
        st.error("The response could not be generated due to rate limits. Please try again or choose a different model.")


