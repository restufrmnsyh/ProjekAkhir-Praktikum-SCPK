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
    c1.info("""
        **Menyediakan Alternatif**

        Menyajikan lebih dari 40 pilihan karier di bidang Ilmu Komputer yang dapat digunakan sebagai alternatif dalam proses pengambilan keputusan karier.
        """
        )
    c2.info("""
        **Menyesuaikan Pengguna**

        Memungkinkan pengguna menentukan bobot kriteria sesuai minat, kemampuan, dan prioritas yang dimiliki.
        """
            )
    c3.info("""
        **Membantu Keputusan**

        Menggunakan metode SAW untuk menghasilkan peringkat karier terbaik berdasarkan kriteria dan bobot yang telah ditentukan.
        """)
 
    st.divider()
    c1, c2, c3 = st.columns(3)
 
    with c1:
        st.markdown(
            """
            <div style="text-align:center;">
                <img src="https://img.icons8.com/?size=100&id=4lG6YyEmYmrU&format=png&color=000000" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )
 
    with c2:
        st.markdown(
            """
            <div style="text-align:center;">
                <img src="https://img.icons8.com/?size=100&id=fuHwl8nIfR3a&format=png&color=000000" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )
 
    with c3:
        st.markdown(
            """
            <div style="text-align:center;">
                <img src="https://img.icons8.com/?size=100&id=zMToY0P6F63q&format=png&color=000000" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )
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
    st.title("⌨️ Input Data")
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯Alternatif", "⚖️Kriteria dan Bobot", "📑Tabel Terpilih", "🗂️Tabel Semua Alternatif"]
    )

    # ── Tab 1: pilih alternatif ───────────────────────────────
    with tab1:
        st.markdown("**Masukkan Data Alternatif**")
        st.caption("Pilih karier IT yang akan dibandingkan (minimal 3)")

        df_alt = get_alternatif()
        semua_karier = df_alt["Career_Goals"].tolist()

        # Inisialisasi sekali saja
        if "jumlah_widget" not in st.session_state:
            st.session_state["jumlah_widget"] = 5
        if "alternatif_terpilih" not in st.session_state:
            st.session_state["alternatif_terpilih"] = []

        # Callback slider: trim KEDUA key saat max dikecilkan
        def on_jumlah_change():
            j = st.session_state["jumlah_widget"]
            if len(st.session_state.get("alternatif_widget", [])) > j:
                st.session_state["alternatif_widget"] = st.session_state["alternatif_widget"][:j]
            if len(st.session_state.get("alternatif_terpilih", [])) > j:
                st.session_state["alternatif_terpilih"] = st.session_state["alternatif_terpilih"][:j]

        # Callback multiselect: simpan ke key permanen & reset flag keputusan
        def on_alternatif_change():
            st.session_state["alternatif_terpilih"] = st.session_state["alternatif_widget"]
            st.session_state["show_keputusan"] = False

        jumlah = st.slider(
            "Pilih berapa banyak alternatif",
            min_value=3,
            max_value=10,
            key="jumlah_widget",
            on_change=on_jumlah_change,
        )

        # Pastikan default tidak melebihi max_selections sebelum render widget
        safe_default = st.session_state["alternatif_terpilih"][:jumlah]
        if st.session_state.get("alternatif_widget", safe_default) != safe_default:
            if len(st.session_state.get("alternatif_widget", [])) > jumlah:
                st.session_state["alternatif_widget"] = st.session_state["alternatif_widget"][:jumlah]

        st.multiselect(
            f"Pilih maksimal {jumlah} karier:",
            options=semua_karier,
            default=safe_default,
            max_selections=jumlah,
            key="alternatif_widget",
            on_change=on_alternatif_change,
        )

        terpilih = st.session_state["alternatif_terpilih"]

        st.markdown(f"**Alternatif yang dipilih ({len(terpilih)}):**")
        for i, k in enumerate(terpilih, 1):
            st.write(f"{i}. {k}")

    # ── Tab 2: kriteria & bobot ───────────────────────────────
    with tab2:
        st.markdown("**Masukkan Data Kriteria dan Bobot**")

        nama_kriteria = ["GPA (IPK)", "Python Skill", "Problem Solving", "Communication", "Internship", "Certifications"]

        # Inisialisasi key widget sekali saja dari nilai yang tersimpan,
        # sehingga bobot tidak reset saat user kembali ke halaman ini
        saved_bobot = st.session_state.get("bobot", [1.0] * 6)
        for i in range(1, 7):
            wk = f"bobot_widget_{i}"
            if wk not in st.session_state:
                st.session_state[wk] = float(saved_bobot[i - 1])

        bobot_list = []
        for i, nama in enumerate(nama_kriteria, 1):
            c1, c2 = st.columns([2, 1])
            c1.text_input(f"Kriteria {i}", value=nama, disabled=True, label_visibility="visible")
            b = c2.number_input(
                f"Bobot {i}",
                min_value=0.0,
                max_value=10.0,
                step=0.1,
                key=f"bobot_widget_{i}",
                label_visibility="visible"
            )
            bobot_list.append(b)

        st.session_state["bobot"] = bobot_list

        if sum(bobot_list) == 0:
            st.error("⚠️ Semua bobot bernilai 0. Minimal satu kriteria harus memiliki bobot lebih dari 0.")

    # ── Tab 3: tabel alternatif terpilih ─────────────────────
    with tab3:
        st.markdown("**Tabel Alternatif Terpilih**")
        # FIX 4: Selalu baca dari session state, bukan variabel lokal Tab 1
        terpilih_tab3 = st.session_state.get("alternatif_terpilih", [])
        if not terpilih_tab3:
            st.warning("Belum ada alternatif yang dipilih di tab Alternatif.")
        else:
            df_alt = get_alternatif()
            df_show = df_alt[df_alt["Career_Goals"].isin(terpilih_tab3)].reset_index(drop=True)
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
    st.title("📑Output Data")

    tab1, tab2, tab3 = st.tabs(["📲 Normalisasi", "📌 Keputusan", "📊 Grafik"])

    # Ambil data dari session state
    terpilih = st.session_state.get("alternatif_terpilih", [])
    bobot    = st.session_state.get("bobot", [1.0] * 6)

    df_alt = get_alternatif()

    if len(terpilih) < 3:
        st.warning("Silakan pilih minimal 3 alternatif terlebih dahulu.")
        return

    df_filtered = df_alt[
        df_alt["Career_Goals"].isin(terpilih)
    ].reset_index(drop=True)

    cukup = len(df_filtered) >= 3

    # Hitung SAW sekali saja, pakai ulang di semua tab
    df_norm, df_rank, w_norm = (None, None, None)
    if cukup:
        df_norm, df_rank, w_norm = hitung_saw(df_filtered, bobot)
    bobot_nol = cukup and df_norm is None  # semua bobot 0

    # ── Tab 1: Normalisasi ────────────────────────────────────
    with tab1:
        with st.expander("Normalisasi", expanded=True):
            st.markdown("**Normalisasi Matriks Keputusan**")
            if not cukup:
                st.error("Belum input alternatif dan kriteria atau kurang dari minimum")
            elif bobot_nol:
                st.error("⚠️ Semua bobot bernilai 0. Kembali ke Input Data dan isi minimal satu bobot.")
            else:
                df_norm_display = df_norm.copy()
                df_norm_display.columns = ["Karier","GPA","Python","Problem Solving",
                                           "Communication","Internship","Certifications"]
                st.dataframe(df_norm_display.round(4), use_container_width=True)

    # ── Tab 2: Keputusan ──────────────────────────────────────
    with tab2:
        if not cukup:
            st.error("Belum input alternatif dan kriteria atau kurang dari minimum")
        elif bobot_nol:
            st.error("⚠️ Semua bobot bernilai 0. Kembali ke Input Data dan isi minimal satu bobot.")
        else:
            st.markdown("**Tabel Perangkingan (diurutkan tertinggi ke terendah)**")

            df_show = df_rank.copy()
            df_show.columns = ["Karier", "Skor SAW"]

            st.dataframe(
                df_show.style.background_gradient(
                    cmap="Blues",
                    subset=["Skor SAW"]
                ),
                use_container_width=True
            )

            if "show_keputusan" not in st.session_state:
                st.session_state["show_keputusan"] = False

            if st.button("Keputusan"):
                st.session_state["show_keputusan"] = True

            if st.session_state["show_keputusan"]:
                st.success(
                    f"Keputusannya adalah: **{df_rank.iloc[0]['Career_Goals']}** "
                    f"(Skor: {df_rank.iloc[0]['Skor_SAW']:.6f})"
                )

    # ── Tab 3: Grafik ─────────────────────────────────────────
    with tab3:
        if not cukup:
            st.info("Pilih alternatif terlebih dahulu di menu Input Data.")
            return
        if bobot_nol:
            st.error("⚠️ Semua bobot bernilai 0. Kembali ke Input Data dan isi minimal satu bobot.")
            return

        df_raw = load_data()

        # Grafik 1 — Skor SAW (Pie)
        st.markdown("**Skor SAW per Karier**")
        fig, ax = plt.subplots(figsize=(8, max(5, len(df_rank) * 0.5)))
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(df_rank)))
        wedges, texts, autotexts = ax.pie(
            df_rank["Skor_SAW"],
            labels=df_rank["Career_Goals"],
            autopct="%1.1f%%",
            colors=colors,
            startangle=140,
            pctdistance=0.8,
        )
        for t in texts:
            t.set_fontsize(8)
        for at in autotexts:
            at.set_fontsize(7)
            at.set_color("white")
        ax.set_title("Proporsi Skor SAW", fontsize=11)
        tampil_grafik(fig)

        # Grafik 2 — Bobot Kriteria (Line)
        st.markdown("**Bobot Kriteria Pengguna**")
        nama_kriteria = [
            "GPA",
            "Python",
            "Problem Solving",
            "Communication",
            "Internship",
            "Certification"
        ]

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            nama_kriteria,
            bobot,
            marker="o",
            linewidth=2.5
        )

        # Menampilkan nilai pada setiap titik
        for i, nilai in enumerate(bobot):
            ax.text(i, nilai + 0.1, f"{nilai:.1f}", ha="center")

        ax.set_title("Bobot Kriteria Pengguna")
        ax.set_xlabel("Kriteria")
        ax.set_ylabel("Bobot")

        ax.grid(alpha=0.3)

        ax.spines[["top", "right"]].set_visible(False)

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
