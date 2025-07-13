import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optimasi Produksi Campuran", layout="wide")
st.title("🛠️ Optimasi Produksi Campuran (Spion & Dashboard)")

# Sidebar untuk input data
st.sidebar.header("📥 Input Parameter Produksi")

profit_spion = st.sidebar.number_input("Keuntungan per unit Spion (Rp)", value=15000)
profit_dashboard = st.sidebar.number_input("Keuntungan per unit Dashboard (Rp)", value=25000)

bahan_spion = st.sidebar.number_input("Kebutuhan bahan Spion (kg)", value=1.5)
bahan_dashboard = st.sidebar.number_input("Kebutuhan bahan Dashboard (kg)", value=3.5)
total_bahan = st.sidebar.number_input("Total Bahan Plastik (kg)", value=500)

waktu_spion = st.sidebar.number_input("Waktu mesin Spion (jam)", value=0.75)
waktu_dashboard = st.sidebar.number_input("Waktu mesin Dashboard (jam)", value=1.5)
total_waktu = st.sidebar.number_input("Total Waktu Mesin (jam)", value=300)

# Fungsi Tujuan: Maksimalkan keuntungan (negatif karena linprog = minimisasi)
c = [-profit_spion, -profit_dashboard]

# Matriks kendala: A_ub * x <= b_ub
A = [
    [bahan_spion, bahan_dashboard],    # Bahan
    [waktu_spion, waktu_dashboard]     # Waktu
]
b = [total_bahan, total_waktu]

# Batasan variabel (jumlah unit >= 0)
x_bounds = (0, None)
y_bounds = (0, None)

res = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

if res.success:
    spion_opt, dashboard_opt = res.x
    total_profit = -res.fun
    total_bahan_terpakai = spion_opt * bahan_spion + dashboard_opt * bahan_dashboard
    total_waktu_terpakai = spion_opt * waktu_spion + dashboard_opt * waktu_dashboard

    st.subheader("✅ Hasil Optimasi Produksi Campuran")
    st.write(f"Jumlah **Spion** yang diproduksi: *{spion_opt:.0f} unit*")
    st.write(f"Jumlah **Dashboard** yang diproduksi: *{dashboard_opt:.0f} unit*")
    st.write(f"🎯 Total Keuntungan: *Rp {total_profit:,.0f}*")
    st.write(f"🧱 Total Bahan Terpakai: *{total_bahan_terpakai:.2f} kg* dari {total_bahan} kg")
    st.write(f"⏱️ Total Waktu Mesin Terpakai: *{total_waktu_terpakai:.2f} jam* dari {total_waktu} jam")

    st.subheader("📊 Visualisasi Area Feasible")

    x = np.linspace(0, total_bahan, 200)
    y1 = (total_bahan - bahan_spion * x) / bahan_dashboard
    y2 = (total_waktu - waktu_spion * x) / waktu_dashboard
    y = np.minimum(y1, y2)

    plt.figure(figsize=(8, 6))
    plt.plot(x, y1, label="Batas Bahan Plastik")
    plt.plot(x, y2, label="Batas Waktu Mesin")
    plt.fill_between(x, 0, y, color='lightblue', alpha=0.5)
    plt.scatter(spion_opt, dashboard_opt, color='red', label='Solusi Optimal')
    plt.xlabel("Spion")
    plt.ylabel("Dashboard")
    plt.title("Area Feasible Produksi")
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)
else:
    st.error("❌ Optimasi gagal. Periksa kembali parameter produksi.")
