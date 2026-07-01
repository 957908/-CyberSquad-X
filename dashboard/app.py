import streamlit as st
import json
import pandas as pd
import os
import sys


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

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

# JSON File
json_file = "reports/latest_scan.json"

if not os.path.exists(json_file):
    st.error(
        "No scan data found. Run main.py first."
    )
    st.stop()

# Load JSON
with open(
    json_file,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Risk Score",
        f"{data.get('risk_score',0)}/100"
    )

with col2:
    st.metric(
        "Vulnerabilities",
        len(
            data.get(
                "vulnerabilities",
                []
            )
        )
    )

with col3:
    st.metric(
        "Missing Headers",
        len(
            data.get(
                "website",
                {}
            ).get(
                "missing_headers",
                []
            )
        )
    )

# Risk Level
risk = data.get(
    "risk_score",
    0
)

if risk >= 70:

    st.error(
        f"🔴 High Risk : {risk}/100"
    )

elif risk >= 40:

    st.warning(
        f"🟠 Medium Risk : {risk}/100"
    )

else:

    st.success(
        f"🟢 Low Risk : {risk}/100"
    )

st.divider()

# Target Information
st.subheader("🎯 Target Information")

st.write(
    f"**Target:** {data.get('target','N/A')}"
)

st.write(
    f"**Scan Time:** {data.get('timestamp','N/A')}"
)
st.subheader("🛰️ Nmap Scan Results")

st.text_area(
    "Nmap Output",
    data.get(
        "nmap",
        "No Nmap data found."
    ),
    height=300
)

st.divider()

# Website Information
st.subheader("🌐 Website Information")

st.json(
    data.get(
        "website",
        {}
    )
)

st.divider()

# Ollama Analysis
st.subheader("🤖 Ollama AI Analysis")

st.text_area(
    "Ollama Report",
    data.get(
        "ai_analysis",
        "No AI analysis available."
    ),
    height=300
)

# CrewAI Analysis
st.subheader("👥 CrewAI Security Analysis")

st.text_area(
    "CrewAI Report",
    data.get(
        "crew_analysis",
        "No CrewAI analysis available."
    ),
    height=400
)

st.divider()
# Vulnerabilities
st.subheader("🚨 Vulnerability Table")

vulns = data.get(
    "vulnerabilities",
    []
)

if vulns:

    vuln_df = pd.DataFrame(
        {
            "Vulnerability": vulns
        }
    )

    st.dataframe(
        vuln_df,
        use_container_width=True
    )

else:

    st.info(
        "No vulnerabilities found."
    )

st.divider()

# Recon Results
st.subheader("🔎 Recon Results")

recon_data = data.get(
    "recon",
    {}
)

if recon_data:

    recon_df = pd.DataFrame(
        list(
            recon_data.items()
        ),
        columns=[
            "Path",
            "Status"
        ]
    )

    st.dataframe(
        recon_df,
        use_container_width=True
    )

    st.subheader(
        "📊 Recon Results Chart"
    )

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

else:

    st.info(
        "No recon data available."
    )

st.divider()

# Scan History
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

    st.subheader(
        "📈 Risk Trend"
    )

    trend_df = history_df[
        [
            "ID",
            "Risk Score"
        ]
    ]

    trend_df = trend_df.set_index(
        "ID"
    )

    st.line_chart(
        trend_df
    )

else:

    st.info(
        "No scan history found."
    )

st.divider()

# Raw JSON
st.subheader("📄 Raw Scan Data")

st.json(data)