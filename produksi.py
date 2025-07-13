import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Optimasi Produksi Injection", layout="wide")
st.title("📦 Optimasi Produksi Injection Molding (Spion & Dashboard)")

# Sidebar Input
st.sidebar.header("📥 Input Parameter Produksi")

profit_spion = st.sidebar.number_input("Keuntungan per unit Spion (Rp)", value=15000)
profit_dashboard = st.sidebar.number_input("Keuntungan per unit Dashboard (Rp)", value=25000)

bahan_spion = st.sidebar.number_input("Bahan per Spion (kg)", value=1.5)
bahan_dashboard = st.sidebar.number_input("Bahan per Dashboard (kg)", value=3.5)
total_bahan = st.sidebar.number_input("Total Bahan Tersedia (kg)", value=500)

waktu_spion = st.sidebar.number_input("Waktu Mesin per Spion (jam)", value=0.75)
waktu_dashboard = st.sidebar.number_input("Waktu Mesin per Dashboard (jam)", value=1.5)
total_waktu = st.sidebar.number_input("Total Waktu Mesin (jam)", value=300)

# Optimasi Linear
c = [-profit_spion, -profit_dashboard]
A = [[bahan_spion, bahan_dashboard], [waktu_spion, waktu_dashboard]]
b = [total_bahan, total_waktu]

res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method='highs')

# Perhitungan hanya Spion
max_spion_bahan = total_bahan / bahan_spion
max_spion_waktu = total_waktu / waktu_spion
spion_only = int(min(max_spion_bahan, max_spion_waktu))
profit_spion_only = spion_only * profit_spion

# Perhitungan hanya Dashboard
max_dash_bahan = total_bahan / bahan_dashboard
max_dash_waktu = total_waktu / waktu_dashboard
dashboard_only = int(min(max_dash_bahan, max_dash_waktu))
profit_dashboard_only = dashboard_only * profit_dashboard

if res.success:
    x_opt, y_opt = res.x
    total_profit = -res.fun

    st.subheader("✅ Hasil Produksi Optimal (Campuran)")
    st.write(f"Jumlah Spion: **{x_opt:.0f} unit**")
    st.write(f"Jumlah Dashboard: **{y_opt:.0f} unit**")
    st.write(f"Total Keuntungan: **Rp {total_profit:,.0f}**")

    st.subheader("📊 Tabel Perbandingan Strategi Produksi")
    st.markdown(f"""
    <table style="width:100%; border-collapse: collapse;" border="1">
        <tr style="background-color:#f0f0f0;">
            <th>Strategi</th><th>Spion</th><th>Dashboard</th><th>Keuntungan</th>
        </tr>
        <tr>
            <td>Hanya Spion</td><td>{spion_only}</td><td>0</td><td>Rp {profit_spion_only:,.0f}</td>
        </tr>
        <tr>
            <td>Hanya Dashboard</td><td>0</td><td>{dashboard_only}</td><td>Rp {profit_dashboard_only:,.0f}</td>
        </tr>
        <tr style="background-color:#e0ffe0;">
            <td>Campuran (Optimasi)</td><td>{x_opt:.0f}</td><td>{y_opt:.0f}</td><td>Rp {total_profit:,.0f}</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    # ==========================
    # Grafik Garis 1: Produksi Spion
    st.subheader("📈 Grafik Garis: Produksi Spion")
    fig1, ax1 = plt.subplots()
    ax1.plot(['Hanya Spion', 'Campuran'], [spion_only, x_opt], marker='o', linestyle='-')
    ax1.set_ylabel("Jumlah Unit Spion")
    ax1.set_ylim(bottom=0)
    st.pyplot(fig1)

    # Grafik Garis 2: Produksi Dashboard
    st.subheader("📈 Grafik Garis: Produksi Dashboard")
    fig2, ax2 = plt.subplots()
    ax2.plot(['Hanya Dashboard', 'Campuran'], [dashboard_only, y_opt], marker='o', color='orange', linestyle='-')
    ax2.set_ylabel("Jumlah Unit Dashboard")
    ax2.set_ylim(bottom=0)
    st.pyplot(fig2)

    # Grafik Garis 3: Perbandingan Keuntungan
    st.subheader("📈 Grafik Garis: Perbandingan Total Keuntungan")
    strategi = ['Hanya Spion', 'Hanya Dashboard', 'Campuran']
    keuntungan = [profit_spion_only, profit_dashboard_only, total_profit]

    fig3, ax3 = plt.subplots()
    ax3.plot(strategi, keuntungan, marker='o', linestyle='-', color='green')
    ax3.set_ylabel("Keuntungan (Rp)")
    for i, val in enumerate(keuntungan):
        ax3.text(i, val + 10000, f"Rp {val:,.0f}", ha='center')
    ax3.set_ylim(bottom=0)
    st.pyplot(fig3)

else:
    st.error("❌ Optimasi gagal. Periksa kembali parameter input.")
