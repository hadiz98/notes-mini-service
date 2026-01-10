# app.py
import streamlit as st
from ui import add_note_dialog, delete_note_dialog, edit_note_dialog, render_backend_config, render_filters_and_notes

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Notes Service", layout="wide")
st.title("Notes Service")

# ------------------ SESSION STATE ------------------
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://127.0.0.1:8000"
if "show_toast" not in st.session_state:
    st.session_state.show_toast = None
if "edit_note_id" not in st.session_state:
    st.session_state.edit_note_id = None
if "delete_note_id" not in st.session_state:
    st.session_state.delete_note_id = None
if "notes" not in st.session_state:
    st.session_state.notes = []


BACKEND_URL = st.session_state.backend_url

# ------------------ SHOW TOAST ------------------
if st.session_state.show_toast:
    st.toast(st.session_state.show_toast)
    st.session_state.show_toast = None

# ------------------ SEPARATOR ------------------
st.markdown("---")
st.subheader("All Notes")

# ------------------ ADD NOTE ------------------
if st.button("➕ Add Note"):
    add_note_dialog(BACKEND_URL)

# fetch happens here with filters applied
render_filters_and_notes(BACKEND_URL)

# ------------------ EDIT NOTE DIALOG ------------------
if st.session_state.edit_note_id is not None:
    edit_note_dialog(BACKEND_URL, st.session_state.edit_note_id)
    st.session_state.edit_note_id = None


# ------------------ DELETE NOTE DIALOG ------------------
if st.session_state.delete_note_id is not None:
    delete_note_dialog(BACKEND_URL, st.session_state.delete_note_id)
    st.session_state.delete_note_id = None


# ------------------ BACKEND CONFIG ------------------
render_backend_config(BACKEND_URL)
