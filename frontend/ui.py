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
                st.error("Title is required.")
            elif not content.strip():
                st.error("Content is required.")
            else:
                with st.spinner("Saving..."):
                    try:
                        add_note(backend_url, title, content, done)
                        st.session_state.show_toast = "Note added successfully!"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding note: {e}")
    dialog()


# ---- Edit Note Dialog ----
def edit_note_dialog(backend_url, note_id):
    # Find the note in session_state
    note = None
    for n in st.session_state.notes:
      if n["id"] == note_id:
        note = n
        break    
    if not note:
        st.error("Note not found")
        return

    @st.dialog("Edit Note")
    def dialog():
        title = st.text_input("Title", value=note["title"])
        content = st.text_area("Content", value=note["content"])
        done = st.checkbox("Done", value=note["done"])
        
        if st.button("Save Changes", key=f"save_edit_{note_id}"):
            payload = {}
            if title: payload["title"] = title
            if content: payload["content"] = content
            if done is not None: payload["done"] = done
            
            with st.spinner("Updating..."):
                try:
                    update_note(backend_url, note_id, payload)
                    st.session_state.edit_note_id = None
                    st.session_state.show_toast = "Note updated successfully!"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating note: {e}")
    dialog()


# ---- Delete Note Dialog ----
def delete_note_dialog(backend_url, note_id):
    # Find the note in session_state
    note = None
    for n in st.session_state.notes:
      if n["id"] == note_id:
        note = n
        break
    if not note:
        st.error("Note not found")
        return

    @st.dialog("Confirm Delete")
    def dialog():
        st.warning(f"Are you sure you want to delete note **{note['title']}**?")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Yes, Delete", key=f"confirm_delete_{note_id}", type="primary"):
                with st.spinner("Deleting..."):
                    try:
                        delete_note(backend_url, note_id)
                        st.session_state.delete_note_id = None
                        st.session_state.show_toast = "Note deleted successfully!"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting note: {e}")
    dialog()


# ---- Notes Table ----
def render_notes_table(notes):
    if not notes:
        st.info("📝 No notes found. Click '➕ Add Note' to create your first note!")
        return
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
        if note["done"]:
          row_cols[3].badge("", icon=":material/check:", color="green")
        else:
          row_cols[3].badge("", icon=":material/close:", color="red")

        row_cols[4].write(format_date(note["created_at"]))

        with row_cols[5]:
            col_edit, col_delete = st.columns([1,1])
            with col_edit:
                if st.button("Edit", key=f"edit_{note_id}"):
                    st.session_state.edit_note_id = note_id
                    st.rerun()
            with col_delete:
                if st.button("Delete", key=f"delete_{note_id}" ,type="primary"):
                    st.session_state.delete_note_id = note_id
                    st.rerun()


def render_backend_config(backend_url):
    st.markdown("---")
    st.subheader("Backend Configuration")
    backend_url_input = st.text_input("Backend API URL", value=backend_url)
    if st.button("Save Backend URL"):
        st.session_state.backend_url = backend_url_input
        st.toast(f"Backend URL set to `{st.session_state.backend_url}`")
    st.write(f"Current Backend URL: `{st.session_state.backend_url}`")


def render_filters_and_notes(backend_url):
    # Filters wrapped in form to prevent rerun on every keystroke
    with st.form(key="filter_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([4, 2, 1])
        
        with col1:
            search_text = st.text_input("Search by title or content", value="")
        
        with col2:
            done_filter = st.selectbox(
                "Filter by Done Status",
                options=["All", "Done", "Not Done"]
            )
        
        with col3:
            st.write("")
            st.write("")
            submit = st.form_submit_button("Search", use_container_width=True)

    # Map done_filter to boolean or None
    done = None
    if done_filter == "Done":
        done = True
    elif done_filter == "Not Done":
        done = False

    # Always fetch from backend (no cache)
    filtered_notes = get_notes(backend_url, q=search_text or None, done=done)
    
    # Save notes into session state so can be used later to pass the id for note delete and update
    if filtered_notes:
        st.session_state.notes = filtered_notes

    # Render table
    render_notes_table(filtered_notes)