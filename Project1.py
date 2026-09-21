import streamlit as st
import joblib
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Retention Pulse",
    page_icon="📊",
    layout="wide"
)

# ---------- LOAD ----------

try:
    model=joblib.load("Logistic_model.pkl")

except Exception as e:
    st.error(e)
    st.stop()

# exact trained columns
columns=model.feature_names_in_

st.title("Retention Pulse")
st.caption("Customer behavior insights dashboard")

# ---------- INPUTS ----------

age=st.sidebar.slider(
"Age",18,80,30)

tenure=st.sidebar.slider(
"Tenure",0,10,4)

monthly=st.sidebar.slider(
"Monthly Charges",
0,1000,250)

contract=st.sidebar.selectbox(
"Contract Type",
[
"Month-to-month",
"One year",
"Two year"
])

support=st.sidebar.slider(
"Support Calls",
0,5,2)

usage=st.sidebar.slider(
"Usage Score",
0,100,50)

dependents=st.sidebar.selectbox(
"Dependents",
["Yes","No"]
)

# ---------- PREDICT ----------

if st.button("Predict Result"):

    row=dict.fromkeys(columns,0)

    # numeric features
    if "Age" in row:
        row["Age"]=age

    if "tenure" in row:
        row["tenure"]=tenure

    if "MonthlyCharges" in row:
        row["MonthlyCharges"]=monthly

    if "SupportCalls" in row:
        row["SupportCalls"]=support

    if "UsageScore" in row:
        row["UsageScore"]=usage

    # encoded columns

    c=f"Contract_{contract}"

    if c in row:
        row[c]=1

    d=f"Dependents_{dependents}"

    if d in row:
        row[d]=1

    X=pd.DataFrame([row])

    bar=st.progress(0)

    for i in range(100):
        time.sleep(.005)
        bar.progress(i+1)

    pred=model.predict(X)

    prob=model.predict_proba(X)

    score=round(max(prob[0])*100,2)

    if pred[0]==1:
        st.error(
        f"⚠ High Churn Risk ({score}%)"
        )

    else:
        st.success(
        f"✅ Stable Customer ({score}%)"
        )

    st.balloons()