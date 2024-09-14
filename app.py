import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_documentation(code, context):
    if not GEMINI_API_KEY:
        return "Error: Gemini API Key not found. Please set the GEMINI_API_KEY environment variable."

    prompt = f"""
    As an expert technical writer, your task is to create clear and concise documentation for the following code snippet. 
    Consider the following context: {context}
    
    Here's the code:
    ```
    {code}
    ```
    
    Please provide:
    1. A brief overview of what the code does
    2. A description of key functions or classes
    3. Any important parameters or variables
    4. Usage examples (if applicable)
    5. Any potential pitfalls or considerations
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Technical Documentation Assistant")
    st.write("This tool helps developers write clear and concise documentation for their code or projects.")
    
    if not GEMINI_API_KEY:
        st.error("Gemini API Key not found. Please set the GEMINI_API_KEY environment variable.")
        return

    code = st.text_area("Enter your code here:", height=200)
    context = st.text_input("Enter any additional context or requirements:")
    
    if st.button("Generate Documentation"):
        if code:
            with st.spinner("Generating documentation..."):
                documentation = generate_documentation(code, context)
                if documentation.startswith("Error:"):
                    st.error(documentation)
                else:
                    st.subheader("Generated Documentation")
                    st.markdown(documentation)
        else:
            st.warning("Please enter some code to generate documentation.")

if __name__ == "__main__":
    main()