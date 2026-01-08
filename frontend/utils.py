import streamlit as st
from datetime import datetime

def show_toast(message: str):
    st.toast(message)

def format_date(iso_date: str) -> str:
    try:
        return datetime.fromisoformat(iso_date).strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return iso_date
