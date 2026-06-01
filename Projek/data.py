# data.py — Logika data & perhitungan SAW

import pandas as pd
import streamlit as st

KRITERIA = ["GPA", "Python", "Problem_Solving", "Communication", "Internship", "Certifications"]

@st.cache_data
def load_data():
    df = pd.read_csv("dataset_karier_mahasiswa.csv")
    df["Internship_Num"] = df["Internship_Experience"].map({"Yes": 1, "No": 0})
    df["Cert_Num"]       = df["Certifications_Training"].map({"Yes": 1, "No": 0})
    return df

@st.cache_data
def get_alternatif():
    """Rata-rata tiap kriteria per karier sebagai alternatif."""
    df = load_data()
    return df.groupby("Career_Goals").agg(
        GPA           =("GPA",                      "mean"),
        Python        =("Python",                   "mean"),
        Problem_Solving=("Problem_Solving_Abilities","mean"),
        Communication =("Communication_Skills",     "mean"),
        Internship    =("Internship_Num",            "mean"),
        Certifications=("Cert_Num",                 "mean"),
    ).reset_index()

def hitung_saw(df_alt, bobot: list):
    """
    Normalisasi benefit lalu hitung skor SAW.
    Kembalikan (df_norm, df_rank).
    """
    df = df_alt.copy()

    # Normalisasi: x_ij / max(x_j)
    for k in KRITERIA:
        mx = df[k].max()
        df[k + "_norm"] = (df[k] / mx).round(6) if mx else 0.0

    # =========================
    # VALIDASI BOBOT
    # =========================
    total = sum(bobot)

    if total == 0:
        return None, None, None

    # NORMALISASI BOBOT
    w = [b / total for b in bobot]

    # Skor SAW
    norm_cols = [k + "_norm" for k in KRITERIA]
    df["Skor_SAW"] = sum(w[i] * df[norm_cols[i]] for i in range(len(KRITERIA)))
    df["Skor_SAW"] = df["Skor_SAW"].round(6)

    df_norm = df[["Career_Goals"] + norm_cols].copy()
    df_rank = df[["Career_Goals", "Skor_SAW"]].sort_values(
        "Skor_SAW", ascending=False
    ).reset_index(drop=True)
    df_rank.index += 1
    df_rank.index.name = "Peringkat"

    return df_norm, df_rank, w