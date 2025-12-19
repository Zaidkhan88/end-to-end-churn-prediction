import streamlit as st
import requests

st.title("Customer Churn Prediction")

Contract = st.selectbox("Contract Type", {
    "Month-to-month": 0,
    "One year": 1,
    "Two year": 2
}.keys())

tenure = st.number_input("Tenure (months)", 0, 100)

OnlineSecurity = st.radio("Online Security", ["No", "Yes"])
TechSupport = st.radio("Tech Support", ["No", "Yes"])
OnlineBackup = st.radio("Online Backup", ["No", "Yes"])
DeviceProtection = st.radio("Device Protection", ["No", "Yes"])
PaperlessBilling = st.radio("Paperless Billing", ["No", "Yes"])
Dependents = st.radio("Dependents", ["No", "Yes"])

MonthlyCharges = st.number_input("Monthly Charges", 0.0)
TotalCharges = st.number_input("Total Charges", 0.0)

payload = {
    "Contract": {"Month-to-month":0,"One year":1,"Two year":2}[Contract],
    "tenure": tenure,
    "OnlineSecurity": 1 if OnlineSecurity == "Yes" else 0,
    "TechSupport": 1 if TechSupport == "Yes" else 0,
    "TotalCharges": TotalCharges,
    "OnlineBackup": 1 if OnlineBackup == "Yes" else 0,
    "MonthlyCharges": MonthlyCharges,
    "PaperlessBilling": 1 if PaperlessBilling == "Yes" else 0,
    "DeviceProtection": 1 if DeviceProtection == "Yes" else 0,
    "Dependents": 1 if Dependents == "Yes" else 0
}

if st.button("Predict Churn"):
    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    result = response.json()

    if result["churn_prediction"] == 1:
        st.error(f"Likely to Churn 😟 (Prob: {result['churn_probability']})")
    else:
        st.success(f"Customer will Stay 🙂 (Prob: {result['churn_probability']})")
