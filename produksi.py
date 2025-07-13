import streamlit as st 
from scipy.optimize import linprog 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optimasi Produksi Injection", layout="wide")

st.title("🛠️ Aplikasi Optimasi Produksi Injection (Linear Programming)")

st.sidebar.header("Input Data Produksi")

# Input data untuk produk
profit_spion = st.sidebar.number_input("Keuntungan per unit Spion (Rp)", value=15000)
profit_dashboard = st.sidebar.number_input("Keuntungan per unit Dashboard (Rp)", value=25000)

bahan_spion = st.sidebar.number_input("Bahan Plastik per Spion (kg)", value=1.5)
bahan_dashboard = st.sidebar.number_input("Bahan Plastik per Dashboard (kg)", value=3.5)
total_bahan = st.sidebar.number_input("Total Bahan Plastik Tersedia (kg)", value=500)

waktu_spion = st.sidebar.number_input("Waktu Mesin per Spion (jam)", value=0.75)
waktu_dashboard = st.sidebar.number_input("Waktu Mesin per Dashboard (jam)", value=1.5)
total_waktu = st.sidebar.number_input("Total Waktu Mesin Tersedia (jam)", value=300)

# Fungsi tujuan (maksimalkan keuntungan)
c = [-profit_spion, -profit_dashboard]

# Kendala (bahan dan waktu)
A = [
    [bahan_spion, bahan_dashboard],
    [waktu_spion, waktu_dashboard]
]
b = [total_bahan, total_waktu]

# Optimasi Linear
res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)])

if res.success:
    x_opt, y_opt = res.x
    total_profit = -res.fun

    st.subheader("✅ Hasil Optimasi Produksi")
    st.write(f"Jumlah **Spion** yang diproduksi: *{x_opt:.0f} unit*")
    st.write(f"Jumlah **Dashboard** yang diproduksi: *{y_opt:.0f} unit*")
    st.write(f"Total keuntungan maksimal: *Rp {total_profit:,.0f}*")

    # Visualisasi grafik area feasible
    st.subheader("📊 Visualisasi Area Feasible")

    x = np.linspace(0, total_bahan, 200)
    y1 = (total_bahan - bahan_spion * x) / bahan_dashboard
    y2 = (total_waktu - waktu_spion * x) / waktu_dashboard

    plt.figure(figsize=(8, 6))
    plt.plot(x, y1, label="Kendala Bahan Plastik")
    plt.plot(x, y2, label="Kendala Waktu Mesin")
    plt.fill_between(x, np.minimum(y1, y2), color="lightblue", alpha=0.3)

    plt.scatter(x_opt, y_opt, color="red", label="Solusi Optimal")
    plt.xlabel("Spion")
    plt.ylabel("Dashboard")
    plt.legend()
    plt.xlim(left=0)
    plt.ylim(bottom=0)

    st.pyplot(plt)
else:
    st.error("❌ Optimasi gagal. Periksa kembali input datanya.")
