import streamlit as st
import auth  # Import our authentication module
import os

# Make page slightly wider
st.set_page_config(layout="wide")

# Create a slightly narrower central container
container = st.container()
with container:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 900px; /* Default is ~700px */
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

TOPICS_DIR = "topics"

def load_topic_files():
    files = [f for f in os.listdir(TOPICS_DIR) if f.endswith((".md", ".txt",".html"))]
    return {os.path.splitext(f)[0].replace("_", " ").title(): f for f in files}

def load_topic_content(filename):
    filepath = os.path.join(TOPICS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

st.title("🔑 Learn Basics Topics")


# Main Workflow starts here
if not auth.is_authenticated():
    auth.login()
else:
    user = auth.get_current_user()
    st.write(f"✅ Logged in as **{user['name']}**")
    st.success("You are inside the secure dashboard!")

    # Sidebar navigation
    st.sidebar.title("📚 Topics")
    topics = load_topic_files()
    
    # selected_topic = st.sidebar.selectbox("Select topic:", list(topics.keys()))
    selected_topic = st.sidebar.radio(
        "Select a topic:",
        sorted(tuple(topics.keys()))
    )
    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        auth.logout()
        st.stop()

    content = load_topic_content(topics[selected_topic])
    st.subheader(selected_topic)
    st.markdown(content,unsafe_allow_html=True)

    st.success("You are inside the secure dashboard!")