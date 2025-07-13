    st.subheader("📈 Perbandingan Produksi")

    # Perhitungan jika hanya produksi Spion
    max_spion_by_bahan = total_bahan / bahan_spion
    max_spion_by_waktu = total_waktu / waktu_spion
    max_spion_unit = int(min(max_spion_by_bahan, max_spion_by_waktu))
    profit_only_spion = max_spion_unit * profit_spion

    # Perhitungan jika hanya produksi Dashboard
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
