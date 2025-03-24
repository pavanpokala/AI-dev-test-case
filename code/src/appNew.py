import streamlit as st
import openai

# Streamlit UI
st.title("AI-Generated Test Cases for Financial Institutions")

# Context Input
context = st.text_area("Enter Context for Financial Institution:", "Banking transaction system for fraud detection")

openai.api_key = OpenAI_API_KEY

# Generate Test Cases Button
if st.button("Generate Test Cases"):
    with st.spinner("Generating test cases..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert in software testing for financial institutions."},
                {"role": "user", "content": f"Generate test cases based on the following context: {context}"}
            ]
        )
        test_cases = response['choices'][0]['message']['content']

        # Display generated test cases
        st.subheader("Generated Test Cases:")
        st.text_area("Test Cases", test_cases, height=300)

# Auto-update test cases when context changes (experimental feature)
if st.button("Modify Context and Regenerate"):
    with st.spinner("Updating test cases..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in software testing for financial institutions."},
                {"role": "user", "content": f"Modify test cases according to this new context: {context}"}
            ]
        )
        updated_test_cases = response['choices'][0]['message']['content']

        # Display updated test cases
        st.subheader("Updated Test Cases:")
        st.text_area("Test Cases", updated_test_cases, height=300)
