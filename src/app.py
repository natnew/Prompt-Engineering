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
    """, unsafe_allow_html=True)


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


# Apply advanced settings
if role != "No Role":
    formatted_prompt += f"\n\nRole: {role}."

# Ensure the Thinking Step is reflected with a header
if use_thinking_step == 1:
    formatted_prompt += "\n\n### Thinking Step\n<thinking>Explain step-by-step the reasoning behind the output.</thinking>"

if avoid_hallucinations == 1:
    formatted_prompt += "\n\nIf you don't know, state 'I don't know.' Use <Reference></Reference> to pull the reference you used to produce an output."

st.subheader("Transformed Prompt")
st.info(formatted_prompt)

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
- **Avoid Hallucinations**: {"Enabled" if avoid_hallucinations == 1 else "Disabled"} - Instructs the model to avoid guessing and provide references using <Reference></Reference> tags.
"""


st.subheader("Transformation Explanation")
st.info(detailed_explanation)

# Generate response and allow rating
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

        # Step 1: Add rating slider after generating the response
        st.subheader("Rate the Response")
        rating = st.slider("How helpful was this response?", min_value=1, max_value=5, value=3, step=1)

        # Step 2: Submit button for rating
        if st.button("Submit Rating"):
            st.success(f"Thank you for rating the response {rating}/5!")

            # Optional: Store rating or send to backend
            # store_rating(user_id, rating, response)  # This can be implemented if you want to save the ratings
    else:
        st.error("The response could not be generated. Please try again or choose a different model.")



