import requests
import streamlit as st

def get_notes(backend_url):
    try:
        resp = requests.get(f"{backend_url}/notes")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error fetching notes: {e}")
        return []

def add_note(backend_url, title, content, done):
    payload = {"title": title, "content": content, "done": done}
    resp = requests.post(f"{backend_url}/notes", json=payload)
    resp.raise_for_status()
    return resp.json()

def update_note(backend_url, note_id, payload):
    resp = requests.put(f"{backend_url}/notes/{note_id}", json=payload)
    resp.raise_for_status()
    return resp.json()

def delete_note(backend_url, note_id):
    resp = requests.delete(f"{backend_url}/notes/{note_id}")
    resp.raise_for_status()
    return True
