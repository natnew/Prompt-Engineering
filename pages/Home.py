# pages/Home.py
import streamlit as st

st.title("🏠 Home")

st.subheader("Prerequisites")
st.write("""
- Basic understanding of AI and machine learning.
- Familiarity with OpenAI's GPT models.
- Access to an OpenAI API key.
""")

st.subheader("About")
st.write("""
This tool is part of a larger course on Prompt Engineering, designed to help users understand how to interact with language models more effectively.
""")

st.subheader("Features")
st.write("""
- Experiment with different prompt engineering techniques.
- Customize model parameters like temperature, top-p, and max length.
- Get real-time feedback on the effectiveness of your prompts.
""")

st.subheader("Usage")
st.write("""
1. Select a model and adjust the parameters in the sidebar.
2. Choose a department and a prompt.
3. Apply a prompt engineering technique to see how the prompt is transformed.
4. Generate responses from the model to see the output.
""")

st.subheader("Feedback")
st.write("We value your feedback! Please provide any comments or suggestions to help us improve this tool.")

st.subheader("Star on GitHub")
st.write("If you like this project, please give it a star on [GitHub](https://github.com/your-repo-link).")

st.subheader("Disclaimer")
st.write("This project is a work in progress and was created as part of a larger course.")
