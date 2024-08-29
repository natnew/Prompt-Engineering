# src/app.py
import streamlit as st
from prompt_engineering import apply_technique
from models import get_model_response, MODELS
from utils import load_techniques, load_prompts, load_guidelines

# Load data
techniques = load_techniques()
prompts_data = load_prompts()
guidelines = load_guidelines()

# Streamlit sidebar for user selection
st.sidebar.title("Prompt Engineering Tool")

# Model selection
selected_model = st.sidebar.selectbox("Select Model", list(MODELS.keys()))
selected_model_engine = MODELS[selected_model]

# Department selection
selected_department = st.sidebar.selectbox("Select Department", list(prompts_data.keys()))

# Prompt selection
selected_prompt = st.sidebar.selectbox("Select Prompt", prompts_data[selected_department])

# Technique selection
selected_technique = st.sidebar.selectbox("Select Technique", list(techniques.keys()))
technique_description = techniques[selected_technique]["description"]

# Ethical guideline audio
guideline_audio = guidelines[selected_prompt]

# Main content
st.title("Interactive Prompt Engineering")

st.subheader("Selected Prompt")
user_prompt = st.text_area("Edit your prompt below:", value=selected_prompt)

st.subheader("Technique Description")
st.write(technique_description)

# Display ethical guidelines audio
st.subheader("Ethical Guideline")
st.audio(guideline_audio, format='audio/mp3')

# Apply technique to the prompt
transformed_prompt = apply_technique(user_prompt, selected_technique)
st.subheader("Transformed Prompt")
st.write(transformed_prompt)

# Get model response
if st.button("Generate Response"):
    response = get_model_response(selected_model_engine, transformed_prompt)
    st.subheader("Model Response")
    st.write(response)
