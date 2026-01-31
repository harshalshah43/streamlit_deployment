import streamlit as st
import auth

if not auth.is_authenticated():
    st.warning("🔒 Admin access only. Please login.")
    st.stop()

user = auth.get_current_user()

if user =='admin':
    st.error("⛔ You are not authorized to view this page.")
    st.stop()

import json
from pathlib import Path

RESULTS_FILE = Path("quiz_results.json")

st.title("📊 Quiz Results (Admin View)")

if RESULTS_FILE.exists():
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    st.json(data)
else:
    st.info("No quiz results available yet.")

st.download_button(
    label="⬇️ Download quiz_results.json",
    data=json.dumps(data, indent=4),
    file_name="quiz_results.json",
    mime="application/json"
)
