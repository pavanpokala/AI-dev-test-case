import streamlit as st
import pandas as pd
from io import BytesIO


# Mock Financial System
class MockFinancialApp:
    def __init__(self):
        self.users = {"valid_user": "correct_pass"}  # Mock user database
        self.balance = 1000  # Mock account balance

    def login(self, username, password):
        if username in self.users and self.users[username] == password:
            return "Dashboard should load"
        elif username in self.users:
            return "Invalid password error"
        elif username == "":
            return "Username required message"
        else:
            return "User does not exist"

    def check_balance(self, username):
        if username in self.users:
            return f"Balance: ${self.balance}"
        return "User not found"


# Initialize Mock Financial App
mock_app = MockFinancialApp()

# Streamlit UI
st.title("Mock Financial App - Automated Test Execution")

# Upload Test Data
uploaded_file = st.file_uploader("Upload Test Data (Excel)", type=["xlsx"])

if uploaded_file:
    test_cases_df = pd.read_excel(uploaded_file, sheet_name="Test Cases")
    test_data_df = pd.read_excel(uploaded_file, sheet_name="Test Data")

    st.subheader("Test Cases")
    st.dataframe(test_cases_df)

    st.subheader("Test Data")
    st.dataframe(test_data_df)

    # Run Tests
    results = []
    for _, row in test_data_df.iterrows():
        test_case_id = row["Test Case ID"]
        inputs = eval(row["Input"]) if isinstance(row["Input"], str) else row["Input"]
        expected_output = row["Expected Output"]

        # Execute test cases on the mock financial app
        if test_case_id == "TC1":
            actual_output = mock_app.login(*inputs)
        elif test_case_id == "TC2":
            actual_output = mock_app.login(*inputs)
        elif test_case_id == "TC3":
            actual_output = mock_app.login(*inputs)
        else:
            actual_output = "Unknown Test Case"

        result = "Pass" if actual_output == expected_output else "Fail"
        results.append([test_case_id, inputs, expected_output, actual_output, result])

    # Create results DataFrame
    results_df = pd.DataFrame(results, columns=["Test Case ID", "Input", "Expected Output", "Actual Output", "Result"])

    st.subheader("Test Results")
    st.dataframe(results_df)


    # Function to create an Excel file for results
    def create_results_excel():
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            results_df.to_excel(writer, sheet_name="Test Results", index=False)
        output.seek(0)
        return output


    # Download results
    excel_data = create_results_excel()
    st.download_button(label="📥 Download Test Results (Excel)",
                       data=excel_data,
                       file_name="mock_test_results.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
