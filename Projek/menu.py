# menu.py — Isi setiap halaman

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data import load_data, get_alternatif, hitung_saw, KRITERIA


# ── Helper grafik ─────────────────────────────────────────────
def tampil_grafik(fig):
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# =====================================================================
#  HOME
# =====================================================================
def halaman_home():
    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1rem'>
        <h1 style='color:#e94560; font-size:2rem;'>✦ SPK Karier Mahasiswa Ilmu Komputer ✦</h1>
        <p style='color:#aaa;'>Membantu menentukan karier IT yang paling sesuai</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.info("**Menyediakan Alternatif**\n\nMenyajikan 40+ pilihan karier di bidang Ilmu Komputer sebagai alternatif keputusan.")
    c2.info("**Menyesuaikan Pengguna**\n\nBobot kriteria dapat disesuaikan sesuai prioritas dan profil mahasiswa.")
    c3.info("**Membantu Keputusan**\n\nMenggunakan metode SAW untuk menghasilkan ranking karier terbaik.")

    st.divider()
    c1, c2, c3 = st.columns(3)

    c1.image("https://img.icons8.com/?size=100&id=4lG6YyEmYmrU&format=png&color=000000", width=100)
    c2.image("https://img.icons8.com/?size=100&id=fuHwl8nIfR3a&format=png&color=000000", width=100)
    c3.image("https://img.icons8.com/?size=100&id=zMToY0P6F63q&format=png&color=000000", width=100)
    st.markdown(" <div style='text-align:center; fontsize:10px'> ✦ Tentang Kami ✦ ", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:#ccc;'>
        Sistem Pendukung Keputusan (SPK) ini dikembangkan untuk membantu mahasiswa 
        Ilmu Komputer dalam menentukan pilihan karier yang sesuai dengan minat, 
        kemampuan, dan prioritas masing-masing individu.
        Dengan memanfaatkan metode <b>Simple Additive Weighting (SAW)</b>, sistem ini 
        mampu memberikan rekomendasi karier terbaik berdasarkan kriteria yang telah 
        ditentukan dan dapat disesuaikan oleh pengguna.
        Kami berharap sistem ini dapat menjadi alat bantu yang bermanfaat dalam 
        mengambil keputusan karier secara lebih objektif, terstruktur, dan tepat sasaran.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    df = load_data()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Data",    f"{len(df):,} baris")
    col2.metric("Jumlah Karier", df["Career_Goals"].nunique())
    col3.metric("Kriteria",      "6")
    col4.metric("Metode",        "SAW")


# =====================================================================
#  INPUT DATA
# =====================================================================
def halaman_input():
    st.markdown('<p class="page-title">Input Data ✈</p>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Alternatif", "Kriteria dan Bobot", "Tabel Terpilih", "Tabel Semua Alternatif"]
    )

    # ── Tab 1: pilih alternatif ───────────────────────────────
    with tab1:
        st.markdown("**Masukkan Data Alternatif**")
        st.caption("Pilih karier IT yang akan dibandingkan (minimal 3)")

        df_alt = get_alternatif()
        semua_karier = df_alt["Career_Goals"].tolist()

        jumlah = st.number_input("Pilih berapa banyak alternatif", min_value=3, max_value=len(semua_karier), value=5)
        terpilih = st.multiselect(
            f"Pilih maksimal {jumlah} karier:",
            options=semua_karier,
            default=semua_karier[:int(jumlah)],
            max_selections=int(jumlah),
        )
        st.session_state["alternatif_terpilih"] = terpilih

        st.markdown(f"**Alternatif yang dipilih ({len(terpilih)}):**")
        for i, k in enumerate(terpilih, 1):
            st.write(f"{i}. {k}")

    # ── Tab 2: kriteria & bobot ───────────────────────────────
    with tab2:
        st.markdown("**Masukkan Data Kriteria dan Bobot**")
        st.caption("Minimum 5 kriteria (semua sudah tersedia dari dataset)")

        nama_kriteria = ["GPA (IPK)", "Python Skill", "Problem Solving", "Communication", "Internship", "Certifications"]
        bobot_list = []
        for i, nama in enumerate(nama_kriteria, 1):
            c1, c2 = st.columns([2, 1])
            c1.text_input(f"Kriteria {i}", value=nama, disabled=True, label_visibility="collapsed")
            b = c2.number_input(f"Bobot {i}", min_value=0.0, max_value=10.0, value=1.0, step=0.1,
                                label_visibility="visible")
            bobot_list.append(b)

        st.session_state["bobot"] = bobot_list

    # ── Tab 3: tabel alternatif terpilih ─────────────────────
    with tab3:
        st.markdown("**Tabel Alternatif Terpilih**")
        terpilih = st.session_state.get("alternatif_terpilih", [])
        if not terpilih:
            st.warning("Belum ada alternatif yang dipilih di tab Alternatif.")
        else:
            df_alt = get_alternatif()
            df_show = df_alt[df_alt["Career_Goals"].isin(terpilih)].reset_index(drop=True)
            df_show.columns = ["Karier","GPA","Python","Problem Solving","Communication","Internship","Certifications"]
            st.dataframe(df_show.round(3), use_container_width=True)

    # ── Tab 4: semua alternatif dari dataset ──────────────────
    with tab4:
        st.markdown("**Tabel Semua Alternatif (Dataset)**")
        df = load_data()
        kolom = ["GPA","Python","Problem_Solving_Abilities","Communication_Skills",
                 "Internship_Experience","Certifications_Training","Career_Goals"]
        st.dataframe(df[kolom].reset_index(drop=True), use_container_width=True, height=400)
        st.caption(f"Total: {len(df):,} baris data")


# =====================================================================
#  OUTPUT DATA
# =====================================================================
def halaman_output():
    st.markdown('<p class="page-title">Output Data ✈</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Normalisasi", "Keputusan", "Grafik"])

    # Ambil data dari session state
    terpilih = st.session_state.get("alternatif_terpilih", [])
    bobot    = st.session_state.get("bobot", [1.0] * 6)

    df_alt = get_alternatif()

    if terpilih:
        df_filtered = df_alt[df_alt["Career_Goals"].isin(terpilih)].reset_index(drop=True)
    else:
        df_filtered = df_alt.copy()

    cukup = len(df_filtered) >= 3

    # ── Tab 1: Normalisasi ────────────────────────────────────
    with tab1:
        with st.expander("✦ Normalisasi", expanded=True):
            st.markdown("**Normalisasi Matriks Keputusan**")
            if not cukup:
                st.error("Belum input alternatif dan kriteria atau kurang dari minimum")
            else:
                df_norm, df_rank, w_norm = hitung_saw(df_filtered, bobot)
                norm_cols = [c + "_norm" for c in KRITERIA]
                df_norm.columns = ["Karier","GPA","Python","Problem Solving",
                                   "Communication","Internship","Certifications"]
                st.dataframe(df_norm.round(4), use_container_width=True)
                st.session_state["df_rank"] = df_rank
                st.session_state["df_norm_ready"] = True

    # ── Tab 2: Keputusan ──────────────────────────────────────
    with tab2:
        if st.button("Keputusan"):
            if not cukup:
                st.error("Belum input alternatif dan kriteria atau kurang dari minimum")
            else:
                df_norm, df_rank, _ = hitung_saw(df_filtered, bobot)
                st.session_state["df_rank"] = df_rank

        if "df_rank" in st.session_state:
            df_rank = st.session_state["df_rank"]
            st.success(f"Keputusannya adalah: **{df_rank.iloc[0]['Career_Goals']}** "
                       f"(Skor: {df_rank.iloc[0]['Skor_SAW']:.6f})")
            st.markdown("**Tabel Perangkingan (diurutkan tertinggi ke terendah)**")
            df_show = df_rank.copy()
            df_show.columns = ["Karier","Skor SAW"]
            st.dataframe(df_show.style.background_gradient(cmap="Blues", subset=["Skor SAW"]),
                         use_container_width=True)
        else:
            st.info("Keputusannya adalah: 0")

    # ── Tab 3: Grafik ─────────────────────────────────────────
    with tab3:
        if not cukup:
            st.info("Pilih alternatif terlebih dahulu di menu Input Data.")
            return

        df_norm, df_rank, _ = hitung_saw(df_filtered, bobot)
        df_raw = load_data()

        # Grafik 1 — Skor SAW
        st.markdown("**Skor SAW per Karier**")
        fig, ax = plt.subplots(figsize=(9, max(3, len(df_rank) * 0.35)))
        colors = plt.cm.Blues(np.linspace(0.4, 0.85, len(df_rank)))
        ax.barh(df_rank["Career_Goals"][::-1], df_rank["Skor_SAW"][::-1], color=colors)
        ax.set_xlabel("Skor SAW")
        ax.spines[["top","right"]].set_visible(False)
        tampil_grafik(fig)

        # Grafik 2 — Distribusi GPA
        st.markdown("**Distribusi GPA Dataset**")
        fig, ax = plt.subplots(figsize=(9, 3.5))
        ax.hist(df_raw["GPA"], bins=30, color="#0f3460", edgecolor="white", alpha=0.9)
        ax.axvline(df_raw["GPA"].mean(), color="#e94560", linestyle="--",
                   label=f"Rata-rata: {df_raw['GPA'].mean():.2f}")
        ax.set_xlabel("GPA"); ax.set_ylabel("Frekuensi"); ax.legend()
        ax.spines[["top","right"]].set_visible(False)
        tampil_grafik(fig)

        # Grafik 3 — Perbandingan nilai kriteria alternatif terpilih
        st.markdown("**Perbandingan Kriteria Alternatif Terpilih**")
        df_bar = df_filtered.set_index("Career_Goals")[KRITERIA]
        fig, ax = plt.subplots(figsize=(9, 4))
        x = np.arange(len(KRITERIA))
        w = 0.8 / max(len(df_bar), 1)
        for i, (karier, row) in enumerate(df_bar.iterrows()):
            ax.bar(x + i * w, row.values, width=w, label=karier)
        ax.set_xticks(x + w * len(df_bar) / 2)
        ax.set_xticklabels(["GPA","Python","Prob.Solv","Comm","Intern","Cert"], fontsize=9)
        ax.legend(fontsize=7, loc="upper right")
        ax.spines[["top","right"]].set_visible(False)
        tampil_grafik(fig)
