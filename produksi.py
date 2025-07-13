import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aplikasi Optimasi Produksi", layout="wide")

st.title("📊 Aplikasi Optimasi Produksi (Linear Programming)")

st.sidebar.header("Input Data")

# Input data
profit_keripik = st.sidebar.number_input("Keuntungan per Keripik (Rp)", value=5000)
profit_donat = st.sidebar.number_input("Keuntungan per Donat (Rp)", value=8000)

tepung_keripik = st.sidebar.number_input("Tepung per Keripik (kg)", value=2)
tepung_donat = st.sidebar.number_input("Tepung per Donat (kg)", value=4)
max_tepung = st.sidebar.number_input("Total Tepung Tersedia (kg)", value=100)

waktu_keripik = st.sidebar.number_input("Waktu Mesin per Keripik (jam)", value=1)
waktu_donat = st.sidebar.number_input("Waktu Mesin per Donat (jam)", value=2)
max_waktu = st.sidebar.number_input("Total Waktu Mesin (jam)", value=80)

# Fungsi tujuan: maximize 5000x + 8000y => minimize -5000x -8000y
c = [-profit_keripik, -profit_donat]

# Kendala: A_ub x <= b_ub
A = [
    [tepung_keripik, tepung_donat],
    [waktu_keripik, waktu_donat]
]
b = [max_tepung, max_waktu]

# Solve LP
res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)])

if res.success:
    x_opt, y_opt = res.x
    total_profit = -(res.fun)

    st.subheader("✅ Hasil Optimasi")
    st.write(f"Jumlah Keripik yang diproduksi: *{x_opt:.0f} unit*")
    st.write(f"Jumlah Donat yang diproduksi: *{y_opt:.0f} unit*")
    st.write(f"Total keuntungan maksimal: *Rp {total_profit:,.0f}*")

    # Visualisasi area feasible
    st.subheader("📈 Visualisasi Area Feasible")

    x = np.linspace(0, max_tepung, 200)
    y1 = (max_tepung - tepung_keripik * x) / tepung_donat
    y2 = (max_waktu - waktu_keripik * x) / waktu_donat

    plt.figure(figsize=(8, 6))
    plt.plot(x, y1, label="Kendala Tepung")
    plt.plot(x, y2, label="Kendala Waktu Mesin")
    plt.fill_between(x, np.minimum(y1, y2), color="lightgreen", alpha=0.3)

    plt.scatter(x_opt, y_opt, color="red", label="Solusi Optimal")
    plt.xlabel("Keripik")
    plt.ylabel("Donat")
    plt.legend()
    plt.xlim(left=0)
    plt.ylim(bottom=0)

    st.pyplot(plt)
else:
    st.error("Optimasi gagal menemukan solusi. Periksa input data.")
