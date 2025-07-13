import streamlit as st 
from scipy.optimize import linprog 
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optimasi Produksi Injection", layout="wide")

st.title("🛠️ Aplikasi Optimasi Produksi Injection (Linear Programming)")

st.sidebar.header("📥 Input Data Produksi")

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
    plt.xlabel("Jumlah Spion")
    plt.ylabel("Jumlah Dashboard")
    plt.legend()
    plt.xlim(left=0)
    plt.ylim(bottom=0)

    st.pyplot(plt)

    # Perbandingan dengan hanya satu jenis produksi
    st.subheader("📈 Perbandingan Produksi dan Keuntungan")

    # Hanya Spion
    max_spion_by_bahan = total_bahan / bahan_spion
    max_spion_by_waktu = total_waktu / waktu_spion
    max_spion_unit = int(min(max_spion_by_bahan, max_spion_by_waktu))
    profit_only_spion = max_spion_unit * profit_spion

    # Hanya Dashboard
    max_dash_by_bahan = total_bahan / bahan_dashboard
    max_dash_by_waktu = total_waktu / waktu_dashboard
    max_dash_unit = int(min(max_dash_by_bahan, max_dash_by_waktu))
    profit_only_dash = max_dash_unit * profit_dashboard

    st.markdown(f"""
    <table style="width:100%; border-collapse: collapse;" border="1">
        <tr style="background-color:#f0f0f0;">
            <th>Jenis Produksi</th>
            <th>Jumlah Unit</th>
            <th>Keuntungan Total</th>
        </tr>
        <tr>
            <td>Hanya Spion</td>
            <td>{max_spion_unit} unit</td>
            <td>Rp {profit_only_spion:,.0f}</td>
        </tr>
        <tr>
            <td>Hanya Dashboard</td>
            <td>{max_dash_unit} unit</td>
            <td>Rp {profit_only_dash:,.0f}</td>
        </tr>
        <tr style="font-weight:bold; background-color:#e0ffe0;">
            <td>Hasil Optimasi (Campuran)</td>
            <td>{x_opt:.0f} Spion, {y_opt:.0f} Dashboard</td>
            <td>Rp {total_profit:,.0f}</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Optimasi gagal. Periksa kembali input datanya.")
