# app.py
import streamlit as st
from api import get_notes
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

BACKEND_URL = st.session_state.backend_url


# ------------------ SHOW TOAST ------------------
if st.session_state.show_toast:
    st.toast(st.session_state.show_toast)
    st.session_state.show_toast = None

# ------------------ FETCH NOTES ------------------
notes = get_notes(BACKEND_URL)


# ------------------ SEPERATOR FOR NOTES ------------------

st.markdown("---")
st.subheader("All Notes")



# ------------------ ADD NOTE ------------------
if st.button("➕ Add Note"):
    add_note_dialog(BACKEND_URL)

# ------------------ NOTES Table ------------------
render_filters_and_notes(BACKEND_URL , notes)


# ------------------ EDIT NOTE DIALOG ------------------
if st.session_state.edit_note_id is not None:
    edit_note_id = None
    for n in notes:
       if n["id"] == st.session_state.edit_note_id:
         edit_note_id = n
         break
    if edit_note_id:
        edit_note_dialog(BACKEND_URL, edit_note_id)

# ------------------ DELETE NOTE DIALOG ------------------
if st.session_state.delete_note_id is not None:
    delete_note_id = None
    for n in notes:
       if n["id"] == st.session_state.delete_note_id:
         delete_note_id = n
         break
    if delete_note_id:
        delete_note_dialog(BACKEND_URL, delete_note_id)

# ------------------ NO NOTES MESSAGE ------------------
if not notes:
    st.info("No notes found. Add a new note above.")

# ------------------ BACKEND CONFIG ------------------
render_backend_config(BACKEND_URL)