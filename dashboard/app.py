import streamlit as st
import json
import os

st.set_page_config(
    page_title="CyberSquad X",
    layout="wide"
)

st.title("🛡️ CyberSquad X Dashboard")

json_file = "reports/latest_scan.json"

if not os.path.exists(json_file):
    st.error("No scan data found.")
    st.stop()

with open(json_file, "r") as file:
    data = json.load(file)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Risk Score",
        f"{data['risk_score']}/100"
    )

with col2:
    st.metric(
        "Vulnerabilities",
        len(data["vulnerabilities"])
    )

with col3:
    st.metric(
        "Missing Headers",
        len(
            data["website"].get(
                "missing_headers",
                []
            )
        )
    )

st.divider()

st.subheader("Target")

st.write(data["target"])

st.subheader("Scan Time")

st.write(data["timestamp"])

st.divider()

st.subheader("Website Information")

st.json(data["website"])

st.divider()

st.subheader("Recon Results")

st.json(data["recon"])

st.divider()

st.subheader("Vulnerabilities")

st.json(data["vulnerabilities"])