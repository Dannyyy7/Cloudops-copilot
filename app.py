import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenRouter Client

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
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

    if project_description.strip() == "":
        st.warning("Please enter project requirements.")

    else:

        with st.spinner("🤖 AI is generating your DevOps project..."):

            response = client.chat.completions.create(
                model="Qwen/Qwen2.5-Coder-32B-Instruct",
                max_tokens=800,
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a Senior DevOps Engineer.

Generate complete production-ready DevOps files.

Return the output in the following order:

1. Terraform (main.tf)
2. Dockerfile
3. Jenkinsfile (Declarative Pipeline)
4. README.md
5. Deployment Steps

Use markdown code blocks.

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
