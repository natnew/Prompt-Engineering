import openai
import streamlit as st
import pandas as pd

# Function to call GPT API to generate a bio
def chat_gpt(prompt, api_key, model="gpt-3.5-turbo"):
    openai.api_key = api_key  # Set the OpenAI API key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate a bio prompt
def generate_bio_prompt(full_name, interests, publications):
    return f"""
    Generate a professional bio for the following academic profile:

    Name: {full_name}
    Research/Teaching Interests: {interests}
    Recent Publications: {publications}

    The bio should be concise, professional, and focused on the individual.
    """

# Function to process inputs and generate a bio using GPT
def process_bio_generation(api_key, model_name, full_name, interests, publications):
    prompt = generate_bio_prompt(full_name, interests, publications)
    bio = chat_gpt(prompt, api_key, model_name)
    return bio

# Streamlit App
def main():
    # Page Title
    st.title("Professional Bio Generator with GPT")
    st.markdown("Generate professional academic bios using GPT models.")

    # API Configuration
    st.markdown("### API Configuration")
    api_key = st.text_input("API Key", type="password", help="Enter your OpenAI API key.")
    model_name = st.selectbox("Choose a Model", ["gpt-4", "gpt-3.5-turbo"], help="Select the GPT model to use.")

    # User Inputs for Bio Generation
    st.markdown("### Academic Profile Details")
    full_name = st.text_input("Full Name (First and Last Name)", help="Enter the full name of the academic.")
    interests = st.text_area("Research/Teaching Interests", help="Enter the individual's research or teaching interests.")
    publications = st.text_area(
        "Recent Publications", 
        help="Enter the titles of recent publications and, if possible, their sources (e.g., ScienceDirect, SpringerLink)."
    )

    # Generate Bio Button
    if st.button("Generate Bio"):
        # Validate Inputs
        if not api_key:
            st.error("Please provide an API key.")
        elif not full_name:
            st.error("Please provide the full name.")
        elif not interests:
            st.error("Please provide the research/teaching interests.")
        elif not publications:
            st.error("Please provide recent publications.")
        else:
            with st.spinner("Generating bio..."):
                # Generate Bio
                bio = process_bio_generation(api_key, model_name, full_name, interests, publications)
                st.success("Bio Generated Successfully!")
                st.markdown("### Generated Bio")
                st.write(bio)

    # About Section
    with st.sidebar.expander("Capabilities", expanded=False):
        st.write("""
        This app leverages cutting-edge technologies, including GPT-4 and GPT-3.5-turbo, to automate the generation 
        of professional academic bios. It is ideal for researchers, academics, and professionals looking to 
        create high-quality biographical content efficiently.
        """)

# Run the App
if __name__ == "__main__":
    main()
