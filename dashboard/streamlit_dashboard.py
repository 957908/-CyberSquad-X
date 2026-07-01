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

st.set_page_config(
    page_title="CyberSquad X",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CyberSquad X Dashboard")
st.write(
    "AI-Powered Cybersecurity Assessment Platform"
)