import streamlit as st
import pandas as pd
import os

EMAIL_CSV = "allmails.csv"
ROWS_PER_PAGE = 5

def load_data(uploaded_file):
    # if not os.path.exists(EMAIL_CSV):
    #     st.error(f"'{EMAIL_CSV}' not found.")
    #     st.stop()
    # df = pd.read_csv(EMAIL_CSV)
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        xls = pd.ExcelFile(uploaded_file)
        sheet_selected = st.sidebar.selectbox("Select Sheets",options = xls.sheet_names)
        if sheet_selected:
            df = pd.read_excel(uploaded_file,sheet_name = sheet_selected)
    if 'body' not in df.columns:
        st.error("CSV must contain a 'body' column.")
        st.stop()
    if 'label' not in df.columns:
        df['label'] = None
    return df

def save_data(df):
    df.to_csv(EMAIL_CSV, index=False)

def get_next_unlabeled_index(df):
    unlabeled = df[df['label'].isna()]
    return unlabeled.index[0] if not unlabeled.empty else None

st.set_page_config(page_title="Email Annotattion Tool", layout="wide")  # Wide layout

uploaded_file = st.sidebar.file_uploader("Upload your file to Start Annotation (CSV or Excel):", type=["csv", "xlsx"])

if not uploaded_file:
    st.markdown("""
    ### 👋 Welcome to the Email Annotation Tool

    Please follow these steps:

    1. Upload a `.csv` or `.xlsx` file using the uploader in the sidebar.
    2. Make sure your file has a `body` column (containing the email text).
    3. Optional columns like `label`, `id`, or `has_attachment` will be auto-detected.
    4. In the View Tab you can see your annotated data.

    Once uploaded, texts in the **body column will automatically appear** and you'll be able to:
    - Annotate email body using the **Annotate** tab.
    - View or edit labeled/unlabeled emails in the **View Data** tab.
    - Navigate Back and Forth to Edit/View Previously Marked Labels
    """)

    st.markdown("#### 📋 Sample Data Format (Order of columns is not necessary only body column must be present)")

    sample_df = pd.DataFrame({
        "id": [1, 2, 3],
        "body": [
            "Dear customer, your invoice is attached.",
            "Reminder: Please submit your timesheet by Friday.",
            "Congrats! You’ve won a gift card. Click to claim."
        ],
        "has_attachment": [True, False, False],
        "label": [None, None, None]  # This will be filled during annotation
    })

    st.dataframe(sample_df, use_container_width=True)   

if uploaded_file:
    df = load_data(uploaded_file)
    # Tabs
    tab1, tab2 = st.tabs(["📥 Annotate", "📊 View Data"])

    # ------------------ TAB 1: Annotate ------------------ #
    with tab1:
        st.title("📥 Annotate Emails")

        if 'current_index' not in st.session_state:
            next_index = get_next_unlabeled_index(df)
            if next_index is None:
                st.success("✅ All emails have been labeled!")
                st.stop()
            st.session_state.current_index = next_index

        

        if st.session_state.current_index is not None:
            email = df.loc[st.session_state.current_index]
            st.markdown(f"**Email {st.session_state.current_index + 1} of {len(df)}**")
            st.subheader("Email Preview")
            st.write(email['body'])

            current_label = email['label']
            st.markdown(f"**Current Label:** `{current_label}`" if pd.notna(current_label) else "*No label assigned yet*")

            col1, col2 = st.columns([1, 1])
            if col1.button("👍 Yes"):
                df.at[st.session_state.current_index, 'label'] = 'Yes'
                save_data(df)
                st.rerun()

            if col2.button("👎 No"):
                df.at[st.session_state.current_index, 'label'] = 'No'
                save_data(df)
                st.rerun()

        # Handle navigation buttons
        nav_col1, nav_col2 = st.columns([1, 1])
        if nav_col1.button("⬅️ Previous"):
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
            st.rerun()
        if nav_col2.button("➡️ Next"):
            st.session_state.current_index = min(len(df) - 1, st.session_state.current_index + 1)
            st.rerun()

        st.markdown("---")
        st.write(f"Labeled: {df['label'].notna().sum()} / {len(df)}")

    # ------------------ TAB 2: View Data ------------------ #
    with tab2:
        st.title("📊 View Labeled and Unlabeled Emails")

        view_option = st.radio("Select data to view:", ["Labeled", "Unlabeled"], horizontal=True)

        if view_option == "Labeled":
            view_df = df[df['label'].notna()][['id','body','label','has_attachment']].reset_index(drop=True)
        else:
            view_df = df[df['label'].isna()][['id','body','label','has_attachment']].reset_index(drop=True)

        total_rows = len(view_df)
        total_pages = (total_rows - 1) // ROWS_PER_PAGE + 1

        if total_rows == 0:
            st.info("No data to display.")
        else:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * ROWS_PER_PAGE
            end_idx = start_idx + ROWS_PER_PAGE
            st.dataframe(view_df.iloc[start_idx:end_idx], use_container_width=True)