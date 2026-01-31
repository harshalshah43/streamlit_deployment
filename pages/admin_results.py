import streamlit as st
import auth
import json
from pathlib import Path

RESULTS_FILE = Path("quiz_results.json")

# ---------------- Auth Guard ----------------
if not auth.is_authenticated():
    st.warning("🔒 Admin access only. Please login.")
    st.stop()

user = auth.get_current_user()
if user.get("role") != "admin":
    st.error("⛔ You are not authorized to view this page.")
    st.stop()

# ---------------- Helper to load JSON safely ----------------
def load_results():
    if RESULTS_FILE.exists():
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []
    return []

# ---------------- Main Page ----------------
st.title("📊 Quiz Results (Admin View)")

data = load_results()

if data:
    st.json(data)

    st.download_button(
        label="⬇️ Download quiz_results.json",
        data=json.dumps(data, indent=4),
        file_name="quiz_results.json",
        mime="application/json"
    )
else:
    st.info("No quiz results available yet.")
