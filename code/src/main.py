import re

import streamlit as st
import pandas as pd
import os
from io import BytesIO
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Set OpenAI API Key

# Initialize AI model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Function to generate test cases
def generate_test_cases(requirement):
    system_message = SystemMessage(content=f"""
You are a test case generator. Generate structured test cases in this exact format:

ID | Description | Expected Result
--- | ----------- | ---------------
TC1 | User enters valid credentials | Dashboard should load
TC2 | User enters invalid credentials | Error message should appear

Ensure:
1. Every row has exactly 3 columns: **ID, Description, Expected Result**.
2. **No extra text or explanation**—just the table.
3. **Use `|` as a separator**.

Now, generate test cases for: {requirement}
""")
    user_message = HumanMessage(content=requirement)
    response = llm.invoke([system_message, user_message])

    # ✅ Print response to verify correct format
    print("Generated Test Cases:\n", response.content)

    return response.content
# Function to generate test data
def generate_test_data(test_cases):
    system_message = SystemMessage(content=f"""
You are a test data generator. Based on the following test cases, generate structured test data.

Test Cases:
{test_cases}

Format the test data like this:

Test Case ID | Input | Expected Output
--- | -------- | -----------------
TC1 | "valid_user", "correct_pass" | Dashboard should load
TC2 | "valid_user", "wrong_pass" | "Invalid password" error

Ensure:
1. **Each row corresponds to a test case ID.**
2. **Exactly 3 columns: Test Case ID, Input, Expected Output.**
3. **Use `|` as a separator.**
4. **No extra text or explanation—only the table.**
""")
    user_message = HumanMessage(content="Generate test data based on the test cases.")
    response = llm.invoke([system_message, user_message])

    # ✅ Debug: Print AI response
    print("Generated Test Data:\n", response.content)

    return response.content


# Function to convert text-based output to structured DataFrame


def parse_output_to_dataframe(text_output):
    lines = text_output.strip().split("\n")
    structured_data = []

    for line in lines:
        # ✅ Ignore headers and separators
        if "ID | Description | Expected Result" in line or "---" in line:
            continue

        # ✅ Handle inconsistent spacing and separators
        columns = re.split(r"\s*\|\s*", line.strip())

        # ✅ Ensure exactly 3 columns (fill missing ones with "Unknown")
        while len(columns) < 3:
            columns.append("Unknown")

        structured_data.append(columns[:3])  # Keep only 3 columns

    return pd.DataFrame(structured_data, columns=["ID", "Description", "Expected Result"]) if structured_data else pd.DataFrame()
st.title("AI-Powered Test Case & Test Data Generator")

requirement = st.text_area("Enter System Requirement", "Login functionality should allow valid users to access the dashboard.")

# Session state to store generated data
if "test_cases_df" not in st.session_state:
    st.session_state.test_cases_df = pd.DataFrame()
if "test_data_df" not in st.session_state:
    st.session_state.test_data_df = pd.DataFrame()

if st.button("Generate Test Cases"):
    test_cases_text = generate_test_cases(requirement)
    st.session_state.test_cases_df = parse_output_to_dataframe(test_cases_text)
    st.subheader("Generated Test Cases")
    st.dataframe(st.session_state.test_cases_df)

if not st.session_state.test_cases_df.empty:
    if st.button("Generate Test Data"):
        test_data_text = generate_test_data(st.session_state.test_cases_df.to_string(index=False))
        st.session_state.test_data_df = parse_output_to_dataframe(test_data_text)
        st.subheader("Generated Test Data")
        st.dataframe(st.session_state.test_data_df)

# Function to create an Excel file
def create_excel():
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        st.session_state.test_cases_df.to_excel(writer, sheet_name="Test Cases", index=False)
        st.session_state.test_data_df.to_excel(writer, sheet_name="Test Data", index=False)
    output.seek(0)
    return output

# Download Excel button
if not st.session_state.test_cases_df.empty and not st.session_state.test_data_df.empty:
    excel_data = create_excel()
    st.download_button(label="📥 Download Test Cases & Test Data (Excel)",
                       data=excel_data,
                       file_name="test_cases_test_data.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
