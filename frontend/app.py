from datetime import datetime
import streamlit as st
import requests

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Notes Service", layout="wide")
st.title("📝 Notes Service")

# ------------------ SESSION STATE ------------------
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://127.0.0.1:8000"
if "show_toast" not in st.session_state:
    st.session_state.show_toast = None  # message to show in toast

BACKEND_URL = st.session_state.backend_url

# ------------------ HELPER FUNCTIONS ------------------
def get_notes():
    try:
        resp = requests.get(f"{BACKEND_URL}/notes")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error fetching notes: {e}")
        return []

# ------------------ TOAST MESSAGES ------------------
if st.session_state.show_toast:
    st.toast(st.session_state.show_toast)
    st.session_state.show_toast = None

# ------------------ FETCH NOTES ------------------
notes = get_notes()
st.markdown("---")
st.subheader("All Notes")

# ------------------ ADD NOTE BUTTON ------------------

if st.button("➕ Add Note"):
    @st.dialog("📝 Add New Note")
    def add_note_dialog():
        title = st.text_input("Title", key="add_title",)
        content = st.text_area("Content", key="add_content")
        done = st.checkbox("Done", value=False, key="add_done")

        if st.button("Save Note", key="save_new_note"):
            if not title.strip():
              st.error("❌ Title is required.")
            elif not content.strip():
              st.error("❌ Content is required.")
            else:
                payload = {"title": title, "content": content, "done": done}
                try:
                 resp = requests.post(f"{BACKEND_URL}/notes", json=payload)
                 resp.raise_for_status()
                 st.session_state.show_toast = "✅ Note added successfully!"
                 st.rerun()
                except Exception as e:
                 st.error(f"Error adding note: {e}")

    add_note_dialog()

# ------------------ NOTES TABLE ------------------
if notes:
    # Table header
    header_cols = st.columns([1, 3, 5, 1, 2])
    headers = ["ID", "Title", "Content", "Done", "Created At"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for note in notes:
        row_cols = st.columns([1, 3, 5, 1, 2])
        note_id = note["id"]

        row_cols[0].write(note_id)
        row_cols[1].write(note["title"])
        row_cols[2].write(note["content"])
        row_cols[3].write("✅" if note["done"] else "❌")
        try:
            created = datetime.fromisoformat(note["created_at"]).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            created = note["created_at"]
        row_cols[4].write(created)
# ------------------ NO NOTES MESSAGE ------------------
if not notes:
    st.info("No notes found. Add a new note above.")

# ------------------ BACKEND CONFIG ------------------
st.markdown("---")
st.subheader("⚙️ Backend Configuration")
backend_url_input = st.text_input("Backend API URL", value=BACKEND_URL)
if st.button("Save Backend URL"):
    st.session_state.backend_url = backend_url_input
    st.toast(f"✅ Backend URL set to `{st.session_state.backend_url}`")

st.write(f"Current Backend URL: `{st.session_state.backend_url}`")
