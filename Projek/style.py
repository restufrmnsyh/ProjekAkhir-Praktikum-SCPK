# style.py — CSS & konfigurasi tampilan

import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Projek Akhir SCPK",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def load_css():
    st.markdown("""
    <style>
        /* Sidebar */
        section[data-testid="stSidebar"] { background-color: #1a1a2e; }
        section[data-testid="stSidebar"] * { color: #ffffff !important; }

        /* Konten utama */
        .main { background-color: #16213e; }
        .block-container { padding-top: 3.5rem; padding-left: 2rem; padding-right: 2rem; }

        /* Judul halaman */
        .page-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #e94560;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }

        /* Tab aktif */
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #e94560 !important;
            border-bottom: 2px solid #e94560 !important;
        }

        /* Tombol */
        div.stButton > button {
            background-color: #e94560;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            width: 100%;
        }
        div.stButton > button:hover { background-color: #c73652; }

        /* Metric */
        div[data-testid="metric-container"] {
            background: #0f3460;
            border-radius: 8px;
            padding: 0.6rem 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

def sidebar_nav():
    st.sidebar.markdown("## Projek Akhir SCPK")
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Profile 👤**")
    st.sidebar.write("Muhammad Restu F (123240050)")
    st.sidebar.markdown("Kafka Akmal Dani (123240203)")
    st.sidebar.markdown("---")
    st.sidebar.markdown("Pilih salah satu")
    menu = st.sidebar.selectbox(
        "Menu",
        ["Home", "Input Data", "Output Data"],
        label_visibility="collapsed",
    )
    return menu
