import streamlit as st
from pathlib import Path

CSS_FILE = Path("ui/styles.css")
CARD_HTML_FILE = Path("ui/card.html")


def load_css():
    if CSS_FILE.exists():
        css = CSS_FILE.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_card(item):
    if not CARD_HTML_FILE.exists():
        st.write(item.get("title", ""))
        return

    html = CARD_HTML_FILE.read_text(encoding="utf-8")
    for key, value in item.items():
        html = html.replace(f"{{{{{key}}}}}", str(value))
    st.markdown(html, unsafe_allow_html=True)


def render_section_title(text):
    st.markdown(f"<div class='pp-section-title'>{text}</div>", unsafe_allow_html=True)
