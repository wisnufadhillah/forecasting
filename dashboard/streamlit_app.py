import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Inventaris UMKM", layout="wide")

st.title("📦 Smart Inventory Forecasting UMKM")
st.markdown("Dashboard ini menampilkan insight bisnis dan pergerakan stok untuk membantu keputusan restock.")

# Load Data dengan Cache biar cepat
@st.cache_data
def load_data():
    # Mengambil path relatif: mundur 1 folder dari 'dashboard', lalu masuk ke 'dataset/processed'
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, '..', 'dataset', 'processed', 'inventory_clean.csv')
    
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()
    
    # --- METRIK UTAMA ---
    st.header("📊 Ringkasan Metrik")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Produk Unik", df['product_id'].nunique())
    col2.metric("Total Penjualan (IDR)", f"Rp {df['sales_idr'].sum():,.0f}")
    
    produk_restock = df[df['recommended_restock'] > 0]['product_name'].nunique()
    col3.metric("Produk Butuh Restock", produk_restock)
    
    st.markdown("---")
    
    # --- VISUALISASI ---
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.subheader("🏆 Top 5 Selling Products")
        top_sales = df.groupby('product_name')['quantity_sold'].sum().sort_values(ascending=False).head(5).reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x='quantity_sold', y='product_name', data=top_sales, palette='viridis', ax=ax)
        ax.set_xlabel("Total Terjual (Unit)")
        ax.set_ylabel("")
        st.pyplot(fig)

    with col_viz2:
        st.subheader("📈 Tren Penjualan Harian")
        trend = df.groupby('date')['quantity_sold'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.lineplot(x='date', y='quantity_sold', data=trend, marker='o', color='b', ax=ax2)
        ax2.set_xlabel("Tanggal")
        ax2.set_ylabel("Total Barang Terjual")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    # --- TABEL REKOMENDASI RESTOCK ---
    st.markdown("---")
    st.subheader("🚨 Peringatan Restock (Produk di bawah batas aman)")
    
    # Ambil baris transaksi terakhir untuk setiap produk
    latest_stock = df.sort_values('date').groupby('product_name').tail(1)
    need_restock = latest_stock[latest_stock['recommended_restock'] > 0][
        ['product_name', 'current_stock', 'reorder_point', 'recommended_restock']
    ].sort_values('recommended_restock', ascending=False).reset_index(drop=True)
    
    if not need_restock.empty:
        st.dataframe(need_restock, use_container_width=True)
    else:
        st.success("Mantap! Semua stok produk saat ini aman.")

except FileNotFoundError:
    # INI JUGA DIUBAH PESAN ERRORNYA YAK 👇
    st.error("❌ Data tidak ditemukan! Pastikan file 'inventory_clean.csv' sudah ada di folder 'dataset/processed/'.")

st.markdown("---")
st.markdown("*Aplikasi Dashboard - MVP Smart Inventory Forecasting*")