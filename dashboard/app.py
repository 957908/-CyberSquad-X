import streamlit as st
import json
import pandas as pd
import os
from database.database import CyberSquadDB


db = CyberSquadDB()
# Page Config
st.set_page_config(
    page_title="CyberSquad X",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CyberSquad X Dashboard")
st.write("AI-Powered Cybersecurity Assessment Platform")

# Check JSON File
json_file = "reports/latest_scan.json"

if not os.path.exists(json_file):
    st.error("No scan data found. Run main.py first.")
    st.stop()

# Load Data
with open(json_file, "r") as file:
    data = json.load(file)

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Risk Score",
        f"{data['risk_score']}/100"
    )

with col2:
    st.metric(
        "Vulnerabilities",
        len(data.get("vulnerabilities", []))
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

# Risk Status
risk = data["risk_score"]

if risk >= 70:
    st.error(f"🔴 High Risk : {risk}/100")

elif risk >= 40:
    st.warning(f"🟠 Medium Risk : {risk}/100")

else:
    st.success(f"🟢 Low Risk : {risk}/100")

st.divider()

# Target Information
st.subheader("🎯 Target Information")

st.write(
    f"**Target:** {data['target']}"
)

st.write(
    f"**Scan Time:** {data['timestamp']}"
)

st.divider()

# Website Information
st.subheader("🌐 Website Information")

st.json(data["website"])

st.divider()

# Vulnerability Table
st.subheader("🚨 Vulnerability Table")

vulns = data.get(
    "vulnerabilities",
    []
)

if vulns:

    df = pd.DataFrame(vulns)

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info(
        "No vulnerabilities found."
    )

st.divider()

# Recon Results
st.subheader("🔎 Recon Results")

recon_df = pd.DataFrame(
    list(data["recon"].items()),
    columns=[
        "Path",
        "Status"
    ]
)

st.dataframe(
    recon_df,
    use_container_width=True
)

st.divider()

# Recon Chart
st.subheader("📊 Recon Results Chart")

chart_df = recon_df.copy()

chart_df["Status"] = pd.to_numeric(
    chart_df["Status"],
    errors="coerce"
)

st.bar_chart(
    chart_df.set_index(
        "Path"
    )
)

st.divider()

# Raw JSON
st.subheader("📄 Raw Scan Data")

st.json(data)
st.divider()

st.subheader("📜 Scan History")

history = db.get_all_scans()

if history:

    history_df = pd.DataFrame(
        history,
        columns=[
            "ID",
            "Target",
            "Risk Score",
            "Scan Time"
        ]
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

else:

    st.info(
        "No scan history found."
    )
st.subheader("📈 Risk Trend")

if len(history_df) > 0:

    trend_df = history_df[
        ["ID", "Risk Score"]
    ]

    trend_df = trend_df.set_index(
        "ID"
    )

    st.line_chart(
        trend_df
    )

else:

    st.info(
        "Not enough data for trend chart."
    )