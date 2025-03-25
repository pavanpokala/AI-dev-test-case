from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()


# Financial Transaction Model
class Transaction(BaseModel):
    transaction_id: str
    amount: float
    transaction_type: str
    country: str
    customer_age: int


# Simulate a fraud detection system
def detect_fraud(transaction: Transaction):
    if transaction.amount > 8000:
        return "Potential Fraud: High-value transaction!"
    if transaction.transaction_type == "Online" and transaction.country not in ["US", "UK"]:
        return "Potential Fraud: Suspicious international online transaction!"
    return "Transaction Passed"


# Simulate compliance checks
def check_compliance(transaction: Transaction):
    alerts = []
    if transaction.amount > 5000:
        alerts.append("Compliance Alert: High-value transaction requires approval!")
    if transaction.country not in ["US", "UK"]:
        alerts.append("Compliance Alert: International transaction flag!")
    return alerts if alerts else ["No compliance issues"]


# Endpoint to process transactions
@app.post("/api/transactions/process")
def process_transaction(transaction: Transaction):
    fraud_result = detect_fraud(transaction)
    compliance_result = check_compliance(transaction)

    return {
        "transaction_id": transaction.transaction_id,
        "fraud_detection": fraud_result,
        "compliance_check": compliance_result,
        "status": "Processed"
    }


# Endpoint to execute test cases
@app.post("/api/test")
def execute_test_case(test_case: dict):
    expected = test_case["expected_result"]

    # Simulated actual result (for now, assume it matches expected)
    actual_result = expected  # Change this to real logic if needed

    status = "Passed" if actual_result == expected else "Failed"

    return {
        "test_case_id": test_case["id"],
        "description": test_case["description"],
        "expected_result": expected,
        "actual_result": actual_result,
        "status": status
    }
