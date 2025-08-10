import streamlit as st
import auth  # Import our authentication module

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

st.title("🔑 Learn Python Basics")

if not auth.is_authenticated():
    auth.login()
else:
    user = auth.get_current_user()
    st.write(f"✅ Logged in as **{user['name']}**")

    # Sidebar navigation
    st.sidebar.title("📚 Topics")
    topic = st.sidebar.radio(
        "Select a topic:",
        ("Variables", "Data Types", "Input and Output")
    )

    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        auth.logout()
        st.stop()

    # Protected content based on topic
    if topic == "Variables":
        st.header("📌 Variables")
        st.write("""
        - Variables are used to store data values.
        - Example:
            ```python
            x = 10
            name = "Harshal"
            ```
        """)

    elif topic == "Data Types":
        st.header("📌 Data Types")
        st.write("""
        - Common Python data types:
            - int
            - float
            - str
            - bool
            - list, tuple, set, dict
        """)

    elif topic == "Input and Output":
        st.header("📌 Input and Output")
        st.write("""
        - `input()` is used to take user input (in terminal-based programs).
        - `print()` is used to display output.
        - Example:
            ```python
            name = input("Enter your name: ")
            print(f"Hello {name}")
            ```
        """)

    st.success("You are inside the secure dashboard!")
