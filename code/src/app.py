import streamlit as st
import hashlib
import openai

openai.api_key = OpenAI_API_KEY

def generate_test_cases(context):
    prompt = f"Generate structured test cases for a finance system based on this context:\n\n{context}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messaages=[{"role":"user", "content":prompt}]
    )
    return response["choices"][0]["message"]["content"]

def has_context_changed(new_context, context_hash):
    new_hash = hashlib.sha256(new_context.encode('utf-8')).hexdigest()
    return new_hash != context_hash, new_hash
st.title("GenAI-Based Test Case Generator for Financial Systems")
st.write("Enter a financial system context to generate structured test cases dynamically")

new_context = st.text_area("Enter a financial system context", "")
if "context_hash" not in st.session_state:
    st.session_state.context_hash = ""
if "test_cases" not in st.session_state:
    st.session_state.test_cases = ""

if st.button("Generate Test Cases"):
    changed, new_hash = has_context_changed(new_context, st.session_state.context_hash)
    if changed:
        st.session_state.context_hash = new_hash
        st.session_state.test_cases = generate_test_cases(st.session_state.context_hash)
        st.success("Test Cases Generated")
    else:
        st.session_state.test_cases = generate_test_cases(st.session_state.context_hash)

        st.info("Test Cases Not Generated")

if st.session_state.test_cases:
    st.subheader("Generated Test Cases")
    st.text_area("Test Cases", st.session_state.test_cases, height=300)