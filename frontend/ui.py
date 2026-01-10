import streamlit as st
from utils import show_toast, format_date
from api import add_note, get_notes, update_note, delete_note

# ---- Add Note Dialog ----
def add_note_dialog(backend_url):
    @st.dialog("Add New Note")
    def dialog():
        title = st.text_input("Title", key="add_title")
        content = st.text_area("Content", key="add_content")
        done = st.checkbox("Done", value=False, key="add_done")

        if st.button("Save Note", key="save_new_note"):
            if not title.strip():
                st.error("❌ Title is required.")
            elif not content.strip():
                st.error("❌ Content is required.")
            else:
                try:
                    add_note(backend_url, title, content, done)
                    st.session_state.show_toast = "✅ Note added successfully!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding note: {e}")
    dialog()


# ---- Edit Note Dialog ----
def edit_note_dialog(backend_url, note):
    @st.dialog("Edit Note")
    def dialog():
        title = st.text_input("Title", value=note["title"], key=f"edit_title_{note['id']}")
        content = st.text_area("Content", value=note["content"], key=f"edit_content_{note['id']}")
        done = st.checkbox("Done", value=note["done"], key=f"edit_done_{note['id']}")

        if st.button("Save Changes", key=f"save_edit_{note['id']}"):
            payload = {}
            if title: payload["title"] = title
            if content: payload["content"] = content
            if done is not None: payload["done"] = done
            try:
                update_note(backend_url, note["id"], payload)
                st.session_state.edit_note_id = None
                st.session_state.show_toast = "✅ Note updated successfully!"
                st.rerun()
            except Exception as e:
                st.error(f"Error updating note: {e}")
    dialog()


def delete_note_dialog(backend_url, note):
    @st.dialog("Confirm Delete")
    def dialog():
        st.warning(f"Note ID {note['id']}: Are you sure you want to delete note **{note['title']}**?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, Delete", key=f"confirm_delete_{note['id']}", type="primary"):
                try:
                    delete_note(backend_url, note["id"])
                    st.session_state.delete_note_id = None
                    st.session_state.show_toast = "✅ Note deleted successfully!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting note: {e}")
        with c2:
            if st.button("Cancel", key=f"cancel_delete_{note['id']}"):
                st.session_state.delete_note_id = None
                st.rerun()
    dialog()


# ---- Notes Table ----
def render_notes_table(notes):
    # Header
    header_cols = st.columns([1,3,5,1,2,1.3])
    headers = ["ID", "Title", "Content", "Done", "Created At", "Actions"]
    for col, header in zip(header_cols, headers):
        col.markdown(f"**{header}**")

    for note in notes:
        row_cols = st.columns([1,3,5,1,2,1.3])
        note_id = note["id"]
        row_cols[0].write(note_id)
        row_cols[1].write(note["title"])
        row_cols[2].write(note["content"])
        row_cols[3].write("✅" if note["done"] else "❌")
        row_cols[4].write(format_date(note["created_at"]))

        with row_cols[5]:
            col_edit, col_delete = st.columns([1,1])
            with col_edit:
                if st.button("Edit", key=f"edit_{note_id}"):
                    st.session_state.edit_note_id = note_id
            with col_delete:
                if st.button("Delete", key=f"delete_{note_id}" ,type="primary"):
                    st.session_state.delete_note_id = note_id


def render_backend_config(backend_url):
    st.markdown("---")
    st.subheader("⚙️ Backend Configuration")
    backend_url_input = st.text_input("Backend API URL", value=backend_url)
    if st.button("Save Backend URL"):
     st.session_state.backend_url = backend_url_input
     st.toast(f"✅ Backend URL set to `{st.session_state.backend_url}`")
    st.write(f"Current Backend URL: `{st.session_state.backend_url}`")


def render_filters_and_notes(backend_url):
    # Filters
    search_text = st.text_input("Search by title or content", value="", key="search_text")
    done_filter = st.selectbox(
        "Filter by Done Status",
        options=["All", "Done", "Not Done"],
        key="done_filter"
    )

    # Map done_filter to boolean or None
    done = None
    if done_filter == "Done":
        done = True
    elif done_filter == "Not Done":
        done = False

    # Fetch filtered notes from backend
    filtered_notes = get_notes(backend_url, q=search_text or None, done=done)

    # Render table
    render_notes_table(filtered_notes)
 
