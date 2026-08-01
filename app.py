import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file (if running locally)
load_dotenv()

# Retrieve API key safely
hf_token = os.getenv("HF_TOKEN")

# Initialize OpenAI Client pointing to Hugging Face Inference Router
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=hf_token
)

# Page Config
st.set_page_config(
    page_title="CloudOps Copilot",
    page_icon="☁️",
    layout="wide"
)

# Title
st.title("☁️ CloudOps Copilot")
st.subheader("AI Powered DevOps Infrastructure Generator")

st.write(
    "Generate Terraform, Dockerfile, Jenkinsfile and README using AI."
)

st.divider()

# User Input
st.header("📋 Project Requirements")

project_description = st.text_area(
    "Describe the infrastructure you want to generate",
    placeholder="Example: Deploy a Node.js application on AWS using Terraform, Docker, Jenkins and GitHub Actions.",
    height=200
)

generate = st.button("🚀 Generate Infrastructure")

# Generate Response
if generate:

    if not project_description.strip():
        st.warning("Please enter project requirements.")

    elif not hf_token:
        st.error("🔑 `HF_TOKEN` environment variable is missing! Please check your Jenkins credentials or .env file.")

    else:
        try:
            with st.spinner("🤖 AI is generating your DevOps project..."):

                response = client.chat.completions.create(
                    # Added provider routing suffix so HF Router resolves Qwen properly
                    model="Qwen/Qwen2.5-Coder-32B-Instruct:auto",
                    max_tokens=1500,  # Increased token limit so complete code isn't truncated
                    temperature=0.3,
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are a Senior DevOps Engineer.

Generate complete production-ready DevOps files based on the user requirements.

Return the output in the following order:

1. Terraform (main.tf)
2. Dockerfile
3. Jenkinsfile (Declarative Pipeline)
4. README.md
5. Deployment Steps

Use markdown code blocks for all files.
Do not explain unnecessary theory.
Write clean and professional code.
"""
                        },
                        {
                            "role": "user",
                            "content": project_description
                        }
                    ]
                )

            st.success("✅ Infrastructure Generated Successfully!")

            st.subheader("Generated Output")

            st.markdown(response.choices[0].message.content)

        except Exception as e:
            st.error(f"An error occurred while generating the output: {str(e)}")
