from datetime import datetime
import pandas as pd
import streamlit as st
import requests

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Notes Service", layout="wide")
st.title("Notes Service")

# Default value is http://127.0.0.1:8000
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://127.0.0.1:8000"

def get_notes():
    try:
        resp = requests.get(f"{st.session_state.backend_url}/notes")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error fetching notes: {e}")
        return []



notes = get_notes()


if st.button("Add Note"):
        @st.dialog("Add New Note")
        def add_note_dialog():
            title = st.text_input("Title")
            content = st.text_area("Content")
            done = st.checkbox("Done", value=False)

            if st.button("Save Note"):
                payload = {"title": title, "content": content, "done": done}
                try:
                    resp = requests.post(f"{st.session_state.backend_url}/notes", json=payload)
                    resp.raise_for_status()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding note: {e}")

        add_note_dialog()


if notes:
    # Table header
    cols = st.columns([1, 3, 5, 1, 2])  # last column for Actions
    headers = ["ID", "Title", "Content", "Done", "Created At"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    # Table rows
    for note in notes:
        cols = st.columns([1, 3, 5, 1, 2])
        cols[0].write(note["id"])
        cols[1].write(note["title"])
        cols[2].write(note["content"])
        done_icon = "✅" if note["done"] else "❌"
        cols[3].write(done_icon)
        created = datetime.fromisoformat(note["created_at"]).strftime("%Y-%m-%d %H:%M")

        cols[4].write(created)

else:
    st.info("No notes found. Add a new note above.")




# ------------------ BACKEND URL (at the end of page) ------------------
st.markdown("---")
st.subheader("⚙️ Backend Configuration")


backend_url_input = st.text_input(
    "Backend API URL", value=st.session_state.backend_url
)
if st.button("Save Backend URL"):
    st.session_state.backend_url = backend_url_input
    st.success(f"✅ Backend URL set to `{st.session_state.backend_url}`")

st.write(f"Current Backend URL: `{st.session_state.backend_url}`")
