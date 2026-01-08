from datetime import datetime
import streamlit as st
import requests

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Notes Service", layout="wide")
st.title("Notes Service")

# ------------------ SESSION STATE ------------------
if "backend_url" not in st.session_state:
    st.session_state.backend_url = "http://127.0.0.1:8000"
if "show_toast" not in st.session_state:
    st.session_state.show_toast = None  # message to show in toast
if "edit_note_id" not in st.session_state:
    st.session_state.edit_note_id = None
if "delete_note_id" not in st.session_state:
    st.session_state.delete_note_id = None

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

if st.button("Add Note"):
    @st.dialog("Add New Note")
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
    header_cols = st.columns([1, 3, 5, 1, 2,1.3])
    headers = ["ID", "Title", "Content", "Done", "Created At", "Actions"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for note in notes:
        row_cols = st.columns([1, 3, 5, 1, 2 ,1.3])
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

        # -------- ACTIONS --------
        with row_cols[5]:
            col_edit, col_delete = st.columns([1, 1])

            # EDIT BUTTON
            with col_edit:
                if st.button("Edit", key=f"edit_{note_id}"):
                    st.session_state.edit_note_id = note_id

            # DELETE BUTTON
            with col_delete:
                if st.button("Delete", key=f"delete_{note_id}" ,type="primary"):
                    st.session_state.delete_note_id = note_id


# ------------------ EDIT NOTE DIALOG ------------------
if st.session_state.edit_note_id is not None:
    note_to_edit = None
    for n in notes:
       if n["id"] == st.session_state.edit_note_id:
         note_to_edit = n
         break
    if note_to_edit:
        @st.dialog("Edit Note")
        def edit_note_dialog():
            title = st.text_input("Title", value=note_to_edit["title"], key=f"edit_title_{note_to_edit['id']}")
            content = st.text_area("Content", value=note_to_edit["content"], key=f"edit_content_{note_to_edit['id']}")
            done = st.checkbox("Done", value=note_to_edit["done"], key=f"edit_done_{note_to_edit['id']}")

            if st.button("Save Changes", key=f"save_edit_{note_to_edit['id']}"):
                payload = {}
                if title:
                    payload["title"] = title
                if content:
                    payload["content"] = content
                if done is not None:
                    payload["done"] = done
                
                try:
                    resp = requests.put(f"{BACKEND_URL}/notes/{note_to_edit['id']}", json=payload)
                    resp.raise_for_status()
                    st.session_state.edit_note_id = None
                    st.session_state.show_toast = "✅ Note updated successfully!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating note: {e}")

        edit_note_dialog()

# ------------------ DELETE DIALOG ------------------
if st.session_state.delete_note_id is not None:
    note_to_delete = None
    for n in notes:
       if n["id"] == st.session_state.delete_note_id:
         note_to_delete = n
         break
    if note_to_delete:
        @st.dialog("Confirm Delete")
        def delete_dialog():
            st.warning(f"Note ID {note_to_delete['id']}: Are you sure you want to delete note **{note_to_delete['title']}**?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Yes, Delete", key=f"confirm_delete_{note_to_delete['id']}"):
                    try:
                        resp = requests.delete(f"{BACKEND_URL}/notes/{note_to_delete['id']}",)
                        resp.raise_for_status()
                        st.session_state.delete_note_id = None
                        st.session_state.show_toast = "✅ Note deleted successfully!"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting note: {e}")
            with c2:
                if st.button("Cancel", key=f"cancel_delete_{note_to_delete['id']}", type="tertiary"):
                    st.session_state.delete_note_id = None
                    st.rerun()

        delete_dialog()


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
