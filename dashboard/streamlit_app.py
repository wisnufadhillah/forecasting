import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Dashboard Inventaris UMKM", layout="wide")
st.title("📦 Smart Inventory Forecasting UMKM")
st.markdown("Dashboard ini menampilkan insight bisnis dan pergerakan stok untuk membantu keputusan restock.")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    # Sekarang kita baca 2 file kecil hasil ekstraksi
    trend_path = os.path.join(base_dir, '..', 'dataset', 'processed', 'dashboard_trend.csv')
    stock_path = os.path.join(base_dir, '..', 'dataset', 'processed', 'dashboard_stock.csv')
    
    df_trend = pd.read_csv(trend_path)
    df_stock = pd.read_csv(stock_path)
    df_trend['date'] = pd.to_datetime(df_trend['date'])
    return df_trend, df_stock

try:
    df_trend, df_stock = load_data()
    
    # --- METRIK UTAMA ---
    st.header("📊 Ringkasan Metrik")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Produk Unik", df_stock['product_name'].nunique())
    col2.metric("Total Penjualan (IDR)", f"Rp {df_trend['sales_idr'].sum():,.0f}")
    
    produk_restock = df_stock[df_stock['recommended_restock'] > 0]['product_name'].nunique()
    col3.metric("Produk Butuh Restock", produk_restock)
    
    st.markdown("---")
    
    # --- VISUALISASI ---
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.subheader("🏆 Top 5 Selling Products")
        top_sales = df_trend.groupby('product_name')['quantity_sold'].sum().sort_values(ascending=False).head(5).reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x='quantity_sold', y='product_name', data=top_sales, palette='viridis', ax=ax)
        ax.set_xlabel("Total Terjual (Unit)")
        ax.set_ylabel("")
        st.pyplot(fig)

    with col_viz2:
        st.subheader("📈 Tren Penjualan Harian")
        trend_harian = df_trend.groupby('date')['quantity_sold'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.lineplot(x='date', y='quantity_sold', data=trend_harian, marker='o', color='b', ax=ax2)
        ax2.set_xlabel("Tanggal")
        ax2.set_ylabel("Total Barang Terjual")
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    # --- TABEL REKOMENDASI RESTOCK ---
    st.markdown("---")
    st.subheader("🚨 Peringatan Restock (Produk di bawah batas aman)")
    
    need_restock = df_stock[df_stock['recommended_restock'] > 0].sort_values('recommended_restock', ascending=False).reset_index(drop=True)
    
    if not need_restock.empty:
        st.dataframe(need_restock, use_container_width=True)
    else:
        st.success("Mantap! Semua stok produk saat ini aman.")

except FileNotFoundError:
    st.error("❌ Data tidak ditemukan! Pastikan file CSV udah digenerate.")