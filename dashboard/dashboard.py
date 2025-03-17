import os
from pathlib import Path
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    try:
        return pd.read_csv("dashboard/main_data.csv")
    except FileNotFoundError:
        return pd.read_csv("main_data.csv")


main_data = load_data()

with st.sidebar:
    # Logo dan Judul
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2418/2418779.png", width=60)
    with col2:
        st.title("🛍️ Olist Analytics")

    st.markdown("---")

    # Date Picker
    min_date = pd.to_datetime(main_data["order_purchase_timestamp"]).dt.date.min()
    max_date = pd.to_datetime(main_data["order_purchase_timestamp"]).dt.date.max()
    start_date, end_date = st.date_input(
        label="📅 Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

    st.markdown("---")

    with st.expander("📍 FILTER LOKASI", expanded=False):
        selected_states = st.multiselect(
            label="Negara Bagian",
            options=main_data["customer_state"].unique(),
            default=main_data["customer_state"].unique(),
            help="Pilih negara bagian pelanggan",
        )

    st.markdown("---")

    # Informasi Dataset
    st.markdown("**ℹ️ Informasi Dataset**")
    st.caption(
        f"Periode Data: {min_date.strftime('%d %b %Y')} - {max_date.strftime('%d %b %Y')}"
    )
    st.caption(f"Total Data: {len(main_data):,} transaksi")
    st.caption("Sumber Data: Olist E-commerce Brazil")

    # Convert date column to datetime (assuming your data has 'date' column)
    main_data["order_purchase_timestamp"] = pd.to_datetime(
        main_data["order_purchase_timestamp"]
    )

    # Create sidebar inputs
    min_date = main_data["order_purchase_timestamp"].min().date()
    max_date = main_data["order_purchase_timestamp"].max().date()

    main_data_filtered = main_data[
        (main_data["order_purchase_timestamp"] >= pd.to_datetime(start_date))
        & (main_data["order_purchase_timestamp"] <= pd.to_datetime(end_date))
        & main_data["customer_state"].isin(selected_states)
    ]

    # Download Button
    st.markdown("---")
    st.download_button(
        label="📥 Download Data Filter",
        data=main_data_filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_data.csv",
        mime="text/csv",
        help="Download data dalam format CSV",
    )


total_filtered_customers = len(main_data_filtered["customer_unique_id"])
total_income = main_data_filtered["price"].sum()

# Tambahkan metrics dengan emoji
st.header("📊 Sales Performance Overview")
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="👥 Total Customers",
        value=f"{total_filtered_customers:,}",
        help="Jumlah unik customer dalam periode terpilih",
    )

with col2:
    st.metric(
        label="💵 Total Income",
        value=f"${total_income:,.0f}",
        help="Total pendapatan kotor dalam periode terpilih",
    )

st.divider()

# Tambahkan section analisis pembayaran
st.divider()
st.header("💳 Analisis Tipe Pembayaran")

# Hitung data
payment_data = (
    main_data_filtered.groupby("payment_type")
    .agg(mean_price=("price", "mean"), total_payments=("payment_type", "count"))
    .reset_index()
)

# Buat layout 2 kolom
col1, col2 = st.columns(2)

with col1:
    # Horizontal bar chart rata-rata harga
    st.markdown("**📊 Rata-rata Harga per Tipe Pembayaran**")

    # Urutkan data dari terbesar ke terkecil
    sorted_data = payment_data.sort_values("mean_price", ascending=True)

    # Buat chart menggunakan matplotlib
    fig, ax = plt.subplots()
    ax.barh(
        sorted_data["payment_type"],
        sorted_data["mean_price"],
        edgecolor="black",
    )

    # Tambahkan label nilai
    for i, v in enumerate(sorted_data["mean_price"]):
        ax.text(v + 3, i, f"${v:,.2f}", color="black", va="center", fontsize=9)

    # Styling chart
    ax.set_xlabel("Rata-rata Harga (USD)")
    ax.set_xlim(0, sorted_data["mean_price"].max() * 1.2)
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    st.pyplot(fig, use_container_width=True)

with col2:
    # Pie chart distribusi pembayaran
    st.markdown("**🔄 Distribusi Tipe Pembayaran**")
    fig, ax = plt.subplots()
    ax.pie(
        payment_data["total_payments"],
        labels=payment_data["payment_type"],
        autopct="%1.1f%%",
        startangle=90,
        colors=["#4CAF50", "#2196F3", "#FF9800", "#E91E63"],
    )
    ax.axis("equal")  # Pie chart lingkaran sempurna
    st.pyplot(fig, use_container_width=True)

st.divider()

st.header("📈 Top Performers")

# Top 5 Kategori berdasarkan Revenue
st.markdown("**💰 Top 5 Kategori Berdasarkan Revenue**")

top5_revenue = (
    main_data_filtered.groupby("product_category_name_english")["price"]
    .sum()
    .nlargest(5)
    .reset_index()
    .rename(
        columns={
            "price": "total_revenue",
            "product_category_name_english": "product_category",
        }
    )
)

# Urutkan untuk chart
top5_sorted = top5_revenue.sort_values("total_revenue", ascending=True)

# Buat horizontal bar chart
fig, ax = plt.subplots()
ax.barh(
    top5_sorted["product_category"],
    top5_sorted["total_revenue"],
    edgecolor="black",
)

# Tambahkan label nilai
for i, v in enumerate(top5_sorted["total_revenue"]):
    ax.text(v + 100, i, f"${v:,.0f}", color="black", va="center", fontsize=9)

# Styling chart
ax.set_xlabel("Total Revenue (USD)")
ax.set_xlim(0, top5_sorted["total_revenue"].max() * 1.1)
ax.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()

st.pyplot(fig, use_container_width=True)
st.divider()
