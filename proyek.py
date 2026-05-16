import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SCPK Career Prediction for Computer Science Students",
    layout="wide"
)

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("StudentCareer.csv")

# RAPIIKAN NAMA KOLOM
df.columns = df.columns.str.replace("_", " ")

# AMBIL DATA CAREER
career_list = sorted(df["Career Goals"].unique())

# LIST KRITERIA
kriteria = [
    "GPA", "Python", "Problem_Solving", "Communication", "Internship", "Certifications"
]

label_kriteria = {
    "GPA":            "GPA (IPK)",
    "Python":         "Python Skill",
    "Problem_Solving":"Problem Solving",
    "Communication":  "Communication Skills",
    "Internship":     "Internship Experience",
    "Certifications": "Certifications/Training",
}

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Dashboard",
        "Dataset",
        "Input Data",
        "Hasil SAW",
        "Visualisasi",
        "Profil"
    ]
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.markdown("""
    <h1 style='text-align:center; color:#1f77ff;'>
        🎓 Sistem Pendukung Keputusan
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align:center; font-size:20px; color:gray;'>
        Prediksi Karier Mahasiswa Ilmu Komputer — Metode SAW
    </p>
    """, unsafe_allow_html=True)

    st.write("")

    # =========================
    # CARD STATISTIK
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Data",
            f"{df.shape[0]:,} baris"
        )

    with col2:
        st.metric(
            "Jumlah Kriteria",
            f"{len(kriteria)} kriteria"
        )

    with col3:
        st.metric(
            "Pilihan Karier",
            f"{len(career_list)} karier"
        )

    with col4:
        st.metric(
            "Metode SPK",
            "SAW"
        )

    st.divider()

    # =========================
    # TENTANG APLIKASI
    # =========================
    col5, col6 = st.columns(2)

    with col5:

        st.subheader("Tentang Aplikasi")

        st.info("""
        Aplikasi ini merekomendasikan karier IT paling sesuai 
        berdasarkan profil mahasiswa Ilmu Komputer menggunakan
        metode Simple Additive Weighting (SAW).
        """)

    with col6:

        st.subheader("Alur Metode SAW")

        st.success("""
        1. Tentukan alternatif (karier IT)  
        2. Tentukan kriteria penilaian  
        3. Atur bobot tiap kriteria  
        4. Normalisasi matriks keputusan  
        5. Hitung skor SAW  
        6. Ranking hasil rekomendasi
        """)

    st.write("")

    # =========================
    # TABEL KRITERIA
    # =========================
    st.subheader("Kriteria yang Digunakan")

    df_kriteria = pd.DataFrame({
        "No": range(1, len(kriteria)+1),
        "Kriteria": [
            "GPA (IPK)",
            "Python Skill",
            "Problem Solving",
            "Communication Skills",
            "Internship Experience",
            "Certifications/Training"
        ],
        "Tipe": ["Benefit"] * len(kriteria),
        "Keterangan": [
            "Indeks Prestasi Kumulatif (0–4)",
            "Kemampuan Python (1–10)",
            "Kemampuan memecahkan masalah (1–10)",
            "Kemampuan komunikasi (1–10)",
            "Pengalaman magang (Ya=1, Tidak=0)",
            "Sertifikasi/pelatihan (Ya=1, Tidak=0)"
        ]
    })

    st.dataframe(
        df_kriteria,
        hide_index=True,
        use_container_width=True
    )



# =========================
# DATASET
# =========================
elif menu == "Dataset":

    st.markdown("""
    <h1 style='text-align:center; color:#1f77ff;'>
        📋 Dataset Karier Mahasiswa
    </h1>
    """, unsafe_allow_html=True)

    st.write("")

    st.caption(
        "Sumber: Kaggle — Computer Science Student Career Dataset (2024)"
    )

    st.write("")

    # =========================
    # CARD INFO DATASET
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jumlah Baris",
            f"{df.shape[0]:,}"
        )

    with col2:
        st.metric(
            "Jumlah Kolom",
            f"{df.shape[1]}"
        )

    with col3:

        missing = df.isnull().sum().sum()

        if missing == 0:
            status = "Tidak ada ✅"
        else:
            status = f"{missing} data"

        st.metric(
            "Missing Value",
            status
        )

    st.divider()

    # =========================
    # FILTER KARIER
    # =========================
    selected_career = st.selectbox(
        "Filter Karier:",
        ["Semua"] + career_list
    )

    # FILTER DATA
    if selected_career == "Semua":
        filtered_df = df
    else:
        filtered_df = df[
            df["Career Goals"] == selected_career
        ]

    # =========================
    # INFORMASI FILTER
    # =========================
    st.caption(
        f"Menampilkan {filtered_df.shape[0]:,} dari {df.shape[0]:,} baris"
    )

    # =========================
    # KOLOM YANG DITAMPILKAN
    # =========================
    kolom_dataset = [
        "GPA",
        "Python",
        "Problem Solving Abilities",
        "Communication Skills",
        "Internship Experience",
        "Certifications Training",
        "Career Goals"
    ]

    # =========================
    # TABEL DATASET
    # =========================
    st.dataframe(
        filtered_df[kolom_dataset],
        use_container_width=True,
        height=500
    )

    st.divider()


# =========================
# INPUT DATA
# =========================
elif menu == "Input Data":

    st.title("📂 Input Data")

    # VARIABEL AWAL
    alternatif_terpilih = []
    kriteria_terpilih = []
    alternatif_values = []
    criteria_values = []
    bobot_values = {}

    # TABS
    tab1, tab2, tab3 = st.tabs([
        "Alternatif",
        "Kriteria & Bobot",
        "Data Terpilih"
    ])

    # =========================
    # TAB 1 - ALTERNATIF
    # =========================
    with tab1:

        st.subheader("Masukkan Data Alternatif")
        st.text("Minimum 3 alternatif dan maksimum 10 alternatif")

        # INPUT JUMLAH ALTERNATIF
        num_alternatif = st.number_input(
            "Pilih berapa banyak alternatif",
            min_value=3,
            max_value=10,
            value=3
        )

        # MULTISELECT CAREER
        alternatif_terpilih = st.multiselect(
            f"Pilih {num_alternatif} career:",
            options=career_list,
            max_selections=num_alternatif
        )

        st.write("### Alternatif yang Dipilih")

        for i in range(num_alternatif):

            # CEK APAKAH SUDAH DIPILIH
            if i < len(alternatif_terpilih):
                nilai = alternatif_terpilih[i]
            else:
                nilai = "-"

            col1, col2 = st.columns([1, 6])
            
            with col1:
                st.write(f"**Alternatif {i+1}:**")  # Label yang bisa diseleksi
            
            with col2:
                st.text_input(
                    f"input_alt_{i}",
                    value=nilai,
                    disabled=True,
                    label_visibility="collapsed"
                )

            alternatif_values.append(nilai)
        
        # HAPUS "-"
        alternatif_values = [
            x for x in alternatif_values if x != "-" 
        ]    

    # =========================
    # TAB 2 - KRITERIA & BOBOT
    # =========================
    with tab2:

        st.subheader("Masukkan Kriteria & Bobot")
        st.text("Minimum 5 kriteria dan maksimum 10 kriteria")

        # INPUT JUMLAH KRITERIA
        num_kriteria = st.number_input(
            "Pilih berapa banyak kriteria",
            min_value=5,
            max_value=10,
            value=5
        )

        # MULTISELECT KRITERIA
        kriteria_terpilih = st.multiselect(
            f"Pilih {num_kriteria} kriteria:",
            options=kriteria,
            max_selections=num_kriteria
        )

        st.write("### Kriteria yang Dipilih")

        for i in range(num_kriteria):

            # CEK APAKAH SUDAH DIPILIH
            if i < len(kriteria_terpilih):
                nilai = kriteria_terpilih[i]
            else:
                nilai = "-"

            st.text_input(
                f"Kriteria {i+1}",
                value=nilai,
                disabled=True
            )

            criteria_values.append(nilai)

        # HAPUS "-"
        criteria_values = [
            x for x in criteria_values if x != "-"
        ]

        # =========================
        # INPUT BOBOT
        # =========================
        if len(kriteria_terpilih) == num_kriteria:

            st.write("## Input Bobot Kriteria")

            for criterion in kriteria_terpilih:

                bobot_values[criterion] = st.slider(
                    f"Bobot {criterion}",
                    min_value=1,
                    max_value=10,
                    value=5
                )

            # TOMBOL PROSES
            proses = st.button("Proses SAW")

        else:
            proses = False

    # =========================
    # TAB 3 - DATA TERPILIH
    # =========================
    with tab3:

        st.subheader("Tabel Data Terpilih")

        # KONDISI:
        # Alternatif dan kriteria sudah dipilih
        if alternatif_terpilih and len(kriteria_terpilih) >= 5:

            # FILTER DATA
            filtered_df = (
                df[df["Career Goals"].isin(alternatif_terpilih)]
                .groupby("Career Goals")
                .first()
                .reset_index()
            )

            # KOLOM YANG DITAMPILKAN
            kolom_tampil = ["Career Goals"] + criteria_values

            # TAMPILKAN TABEL
            st.dataframe(
                filtered_df[kolom_tampil].head(50),
                hide_index=True,
                use_container_width=True
            )

            # JUMLAH DATA
            st.success(
                f"Jumlah data terfilter: {filtered_df.shape[0]}"
            )

            # PROSES SAW
            if proses:

                # SIMPAN SESSION STATE
                st.session_state.kriteria = criteria_values
                st.session_state.alternatif = alternatif_values
                st.session_state.bobot = bobot_values
                st.session_state.data = filtered_df

                st.success("Proses SAW berhasil dilakukan")

        # KONDISI:
        # Baru pilih alternatif
        elif alternatif_terpilih:

            filtered_df = df[
                df["Career Goals"].isin(alternatif_terpilih)
            ]

            st.dataframe(
                filtered_df.head(20),
                hide_index=True,
                use_container_width=True
            )
            # KONDISI:
            # Belum pilih apa-apa
        else:
            st.info("Pilih alternatif terlebih dahulu")

# =========================
# HASIL SAW
# =========================
elif menu == "Hasil SAW":

    st.header("⚖️ Hasil SAW")

    st.info("Halaman hasil SAW akan dibuat pada tahap berikutnya")

# =========================
# VISUALISASI
# =========================
elif menu == "Visualisasi":

    st.header("📊 Visualisasi")

    st.info("Halaman visualisasi akan dibuat pada tahap berikutnya")

# =========================
# PROFIL
# =========================
elif menu == "Profil":

    st.header("👥 Profil Kelompok")

    st.write("Nama Anggota:")
    st.write("1. ...")
    st.write("2. ...")