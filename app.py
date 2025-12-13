import streamlit as st

from db import get_user, create_user, add_interaction, get_user_history, get_user_likes, db_ok
from recommender import (
    get_all_items,
    get_personalized_recommendations,
    get_trending_items,
    get_similar_items,
    get_items_by_ids,
)
from ui.components import load_css, render_card, render_section_title


st.set_page_config(page_title="TrendMatrix – Personalized Recommendations", layout="wide")


def init_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "selected_item_id" not in st.session_state:
        st.session_state.selected_item_id = None


def login_sidebar():
    st.sidebar.markdown("## 👤 Login")
    st.sidebar.caption("Use any name. This just helps remember your picks.")

    # Theme toggle
    st.sidebar.toggle("Light Theme", value=False, key="light_theme")

    username = st.sidebar.text_input("Username", key="username_input")

    if st.sidebar.button("Continue", type="primary"):
        if not username.strip():
            st.sidebar.error("Please enter a username.")
            return

        try:
            user = get_user(username.strip()) or create_user(username.strip())
            st.session_state.user = user
            st.sidebar.success(f"Hi {user['username']} 👋")
        except Exception as e:
            st.sidebar.error("Could not connect to the database. You can still browse demo picks.")
            st.sidebar.code(str(e))


def show_item_grid(items, section_key, user_id):
    if not items:
        st.write("Nothing to show here yet.")
        return

    cols = st.columns(4, gap="large")

    for i, item in enumerate(items):
        col = cols[i % 4]
        with col:
            render_card(item)
            if user_id is not None and db_ok():
                like_key = f"{section_key}_like_{item['id']}"
                if st.button("❤️ Like", key=like_key):
                    add_interaction(user_id, item["id"], "liked")
                    st.toast("Saved to your vibe ✨")


def main():
    init_state()
    theme = 'light' if st.session_state.get('light_theme', False) else 'dark'
    load_css(theme)

    items_df = get_all_items()

    col1, col2 = st.columns([0.12, 0.88])
    with col1:
        st.image("assets/logo.png", width=60)
    with col2:
        st.markdown("### TrendMatrix")
        st.markdown('<div class="app-caption">A small personalized recommendation space.</div>', unsafe_allow_html=True)

    login_sidebar()

    user = st.session_state.user
    if user and db_ok():
        history_ids = get_user_history(user["id"])
        user_id = user["id"]
        st.write(f"Logged in as **{user['username']}**")
        
        # Navigation
        nav = st.sidebar.selectbox("View", ["Recommendations", "Saved Items"], key="nav")
    else:
        history_ids = []
        user_id = None
        nav = "Recommendations"
        if not db_ok():
            st.warning("Database secrets not configured. App will show demo recommendations only.")

    if nav == "Saved Items":
        if user and db_ok():
            liked_ids = get_user_likes(user_id)
            if liked_ids:
                liked_items = get_items_by_ids(liked_ids)
                st.markdown("### 💖 Your Saved Items")
                show_item_grid(liked_items, "likes", user_id)
            else:
                st.write("No saved items yet. Start liking products to see them here!")
        else:
            st.write("Please log in to view saved items.")
    else:
        # Normal recommendations flow
        if history_ids:
            recs = get_personalized_recommendations(history_ids, top_n=8)
            render_section_title("🎯 Recommended for you")
            show_item_grid(recs, "rec", user_id)
        else:
            render_section_title("✨ Fresh picks to get you started")
            show_item_grid(get_trending_items(8), "fresh", user_id)

        
        if history_ids:
            last_id = history_ids[0]
            similar = get_similar_items(last_id, top_n=8)
            if similar:
                render_section_title("📺 Because you viewed something like this")
                show_item_grid(similar, "similar", user_id)

    
        render_section_title("🔥 Trending now")
        show_item_grid(get_trending_items(8), "trending", user_id)


if __name__ == "__main__":
    main()
