import pandas as pd
import os

print("Sedang memproses data gajah...")
df = pd.read_csv('dataset/processed/inventory_clean.csv')

# 1. Bikin data agregasi tren penjualan (Ukurannya bakal kecil banget)
trend_df = df.groupby(['date', 'product_name']).agg({
    'quantity_sold': 'sum',
    'sales_idr': 'sum'
}).reset_index()

# 2. Bikin data status stok terakhir (Cuma 1 baris per produk = super kecil!)
stock_df = df.sort_values('date').groupby('product_name').tail(1)[
    ['product_name', 'current_stock', 'reorder_point', 'recommended_restock']
]

# Save jadi file khusus dashboard
trend_df.to_csv('dataset/processed/dashboard_trend.csv', index=False)
stock_df.to_csv('dataset/processed/dashboard_stock.csv', index=False)

print("✅ Beres! File dashboard_trend.csv & dashboard_stock.csv berhasil dibuat.")