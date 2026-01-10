import requests
import streamlit as st

def get_notes(backend_url, q: str | None = None, done: bool | None = None):
    #Fetch notes from backend, optionally filtered by query text and done status.
    try:
        params = {}
        if q:
            params["q"] = q
        if done is not None:
            params["done"] = done
        resp = requests.get(f"{backend_url}/notes", params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error fetching notes: {e}")
        return []
    

def add_note(backend_url, title, content, done):
    #Add Note to backend 
    payload = {"title": title, "content": content, "done": done}
    resp = requests.post(f"{backend_url}/notes", json=payload)
    resp.raise_for_status()
    return resp.json()

def update_note(backend_url, note_id, payload):
    #Update Note to backend based on id and data
    resp = requests.put(f"{backend_url}/notes/{note_id}", json=payload)
    resp.raise_for_status()
    return resp.json()

def delete_note(backend_url, note_id):
    #Delete Note by ID
    resp = requests.delete(f"{backend_url}/notes/{note_id}")
    resp.raise_for_status()
    return True
