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

# Bottom of sidebar - Blog link and clear button
st.sidebar.markdown("---")
st.sidebar.markdown("📖 **Learn how to build this app in this [blog](https://example.com/blog).**")

# Main content
st.title("Interactive Prompt Engineering")

st.subheader("Selected Prompt")
user_prompt = st.text_area("Edit your prompt below:", value=selected_prompt)

st.subheader("Technique Description")
st.write(technique_description)

# Apply technique to the prompt
transformed_prompt, transformation_explanation = apply_technique(user_prompt, selected_technique)

st.subheader("Transformed Prompt")
st.write(transformed_prompt)

st.subheader("Transformation Explanation")
st.write(transformation_explanation)

# Get model response without streaming
if st.button("Generate Response"):
    with st.spinner("Generating response..."):
        response = get_model_response(selected_model_engine, transformed_prompt)
    st.subheader("Model Response")
    st.write(response)
