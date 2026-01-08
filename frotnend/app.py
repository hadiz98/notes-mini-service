import streamlit as st

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Notes Service", layout="wide")
st.title("Notes Service")

# ------------------ SETTINGS ------------------
# Settings simulated using expander
with st.expander("Settings", expanded=False):
    # Use session_state to store backend URL
    if "backend_url" not in st.session_state:
        st.session_state.backend_url = "http://127.0.0.1:8000"

    backend_url_input = st.text_input(
        "Backend API URL", value=st.session_state.backend_url
    )
    if st.button("Save Settings"):
        st.session_state.backend_url = backend_url_input
        st.success("Settings saved!")

# Save and Access the backend URL
BACKEND_URL = st.session_state.backend_url
st.write(f"Current Backend URL: `{BACKEND_URL}`")
