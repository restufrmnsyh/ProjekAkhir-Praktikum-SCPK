# app.py — Entry point
# Jalankan: streamlit run app.py

from style import set_page_config, load_css, sidebar_nav
from menu import halaman_home, halaman_input, halaman_output

set_page_config()
load_css()

menu = sidebar_nav()

if   menu == "Home":        halaman_home()
elif menu == "Input Data":  halaman_input()
elif menu == "Output Data": halaman_output()