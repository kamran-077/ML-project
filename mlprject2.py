import streamlit as st
import joblib
import pandas as pd
import time

st.set_page_config(
    page_title="Retention Pulse",
    page_icon="📊",
    layout="wide"
)

# ---------- LOAD MODEL ----------

try:
    model = joblib.load("Logistic_model.pkl")
except Exception as e:
    st.error(f"Could not load model: {e}")
    st.stop()

# Exact columns used during training
columns = model.feature_names_in_

st.title("Retention Pulse")
st.caption("Customer behavior insights dashboard")

# ---------- INPUTS ----------

age = st.sidebar.slider(
    "Age",
    min_value=18,
    max_value=80,
    value=30
)

tenure = st.sidebar.slider(
    "Tenure",
    min_value=0,
    max_value=10,
    value=4
)

monthly = st.sidebar.slider(
    "Monthly Charges",
    min_value=0,
    max_value=1000,
    value=250
)

contract = st.sidebar.selectbox(
    "Contract Type",
    [
        "Month-to-month",
        "One year",
        "Two year"
    ]
)

support = st.sidebar.slider(
    "Support Calls",
    min_value=0,
    max_value=5,
    value=2
)

usage = st.sidebar.slider(
    "Usage Score",
    min_value=0,
    max_value=100,
    value=50
)

dependents = st.sidebar.selectbox(
    "Dependents",
    ["Yes", "No"]
)

# ---------- PREDICT ----------

if st.button("Predict Result"):

    # Create a row containing exactly the model's training columns
    row = dict.fromkeys(columns, 0)

    # Numeric features
    if "Age" in row:
        row["Age"] = age

    if "tenure" in row:
        row["tenure"] = tenure

    if "MonthlyCharges" in row:
        row["MonthlyCharges"] = monthly

    if "SupportCalls" in row:
        row["SupportCalls"] = support

    if "UsageScore" in row:
        row["UsageScore"] = usage

    # One-hot encoded Contract feature
    contract_column = f"Contract_{contract}"

    if contract_column in row:
        row[contract_column] = 1

    # One-hot encoded Dependents feature
    dependents_column = f"Dependents_{dependents}"

    if dependents_column in row:
        row[dependents_column] = 1

    # Create DataFrame in the exact column order expected by the model
    X = pd.DataFrame([row], columns=columns)

    # ---------- PROGRESS ----------

    bar = st.progress(0)

    for i in range(100):
        time.sleep(0.005)
        bar.progress(i + 1)

    # ---------- PREDICTION ----------

    pred = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]

    # Get probability corresponding specifically to class 1
    class_probabilities = dict(
        zip(model.classes_, probabilities)
    )

    churn_probability = class_probabilities.get(1, 0)

    churn_score = round(churn_probability * 100, 2)

    # ---------- RESULT ----------

    if pred == 1:
        st.error(
            f"⚠ High Churn Risk ({churn_score}%)"
        )

    else:
        st.success(
            f"✅ Stable Customer ({round((1 - churn_probability) * 100, 2)}% retention probability)"
        )

    # ---------- ADDITIONAL DETAILS ----------

    st.subheader("Prediction Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Churn Probability",
            f"{churn_score}%"
        )

    with col2:
        st.metric(
            "Retention Probability",
            f"{round((1 - churn_probability) * 100, 2)}%"
        )

    with col3:
        st.metric(
            "Prediction",
            "Churn" if pred == 1 else "Stable"
        )

    st.progress(churn_probability)