import os
from pathlib import Path
import streamlit as st

# Cek path
st.write("\n" + "=" * 50)
st.write("DEBUG PATH INFORMATION")
st.write("Current Working Directory (CWD):", os.getcwd())
st.write("Script Path:", Path(__file__).absolute())
st.write("Parent Directory:", Path(__file__).parent.absolute())
st.write("List files in CWD:", os.listdir())
st.write("=" * 50 + "\n")


import pandas as pd
import altair as alt


@st.cache_data
def load_data():
    return pd.read_csv("submission/dashboard/main_data.csv")


main_data = load_data()

# with st.sidebar:
#     # Logo dan Judul
#     col1, col2 = st.columns([1, 4])
#     with col1:
#         st.image("https://cdn-icons-png.flaticon.com/512/2418/2418779.png", width=60)
#     with col2:
#         st.title("🛍️ Olist Analytics")

#     st.markdown("---")

#     # Date Picker
#     min_date = pd.to_datetime(main_data["order_purchase_timestamp"]).dt.date.min()
#     max_date = pd.to_datetime(main_data["order_purchase_timestamp"]).dt.date.max()
#     start_date, end_date = st.date_input(
#         label="📅 Rentang Waktu",
#         value=[min_date, max_date],
#         min_value=min_date,
#         max_value=max_date,
#     )

#     st.markdown("---")

#     # Filter dengan grouping
#     with st.expander("🔍 FILTER PRODUK", expanded=True):
#         selected_product_category = st.multiselect(
#             label="Kategori Produk",
#             options=main_data["product_category_name_english"].unique(),
#             default=main_data["product_category_name_english"].unique(),
#             help="Pilih kategori produk yang ingin ditampilkan",
#         )

#     with st.expander("📍 FILTER LOKASI", expanded=False):
#         selected_states = st.multiselect(
#             label="Negara Bagian",
#             options=main_data["customer_state"].unique(),
#             default=main_data["customer_state"].unique(),
#             help="Pilih negara bagian pelanggan",
#         )

#     st.markdown("---")

#     # Informasi Dataset
#     st.markdown("**ℹ️ Informasi Dataset**")
#     st.caption(
#         f"Periode Data: {min_date.strftime('%d %b %Y')} - {max_date.strftime('%d %b %Y')}"
#     )
#     st.caption(f"Total Data: {len(main_data):,} transaksi")
#     st.caption("Sumber Data: Olist E-commerce Brazil")

#     # Convert date column to datetime (assuming your data has 'date' column)
#     main_data["order_purchase_timestamp"] = pd.to_datetime(
#         main_data["order_purchase_timestamp"]
#     )

#     # Create sidebar inputs
#     min_date = main_data["order_purchase_timestamp"].min().date()
#     max_date = main_data["order_purchase_timestamp"].max().date()

#     main_data_filtered = main_data[
#         (main_data["order_purchase_timestamp"] >= pd.to_datetime(start_date))
#         & (main_data["order_purchase_timestamp"] <= pd.to_datetime(end_date))
#     ]

#     # Download Button
#     st.markdown("---")
#     st.download_button(
#         label="📥 Download Data Filter",
#         data=main_data_filtered.to_csv(index=False).encode("utf-8"),
#         file_name="filtered_data.csv",
#         mime="text/csv",
#         help="Download data dalam format CSV",
#     )


# total_filtered_customers = len(main_data_filtered["customer_unique_id"])
# total_income = main_data_filtered["price"].sum()

# # Tambahkan metrics dengan emoji
# st.header("📊 Sales Performance Overview")
# st.divider()

# col1, col2 = st.columns(2)
# with col1:
#     st.metric(
#         label="👥 Total Customers",
#         value=f"{total_filtered_customers:,}",
#         help="Jumlah unik customer dalam periode terpilih",
#     )

# with col2:
#     st.metric(
#         label="💵 Total Income",
#         value=f"${total_income:,.0f}",
#         help="Total pendapatan kotor dalam periode terpilih",
#     )

# st.divider()

# st.header("📈📉 Top & Bottom Performers")

# # Tambahkan bar chart kategori produk
# product_chart_data = (
#     main_data_filtered["product_category_name_english"]
#     .value_counts()
#     .head(10)
#     .reset_index()
#     .rename(
#         columns={
#             "count": "total_orders",
#             "product_category_name_english": "product_category",
#         }
#     )
# )

# product_chart = (
#     alt.Chart(product_chart_data)
#     .mark_bar()
#     .encode(
#         x=alt.X("total_orders:Q", title="Jumlah Pesanan"),
#         y=alt.Y(
#             "product_category:N",
#             title="Kategori Produk",
#             sort=alt.EncodingSortField(field="total_orders", order="descending"),
#         ),
#         tooltip=["product_category", "total_orders"],
#     )
#     .properties(title="📦 Top 10 Kategori Produk Paling Laris")
#     .interactive()
# )

# st.altair_chart(product_chart, use_container_width=True)

# # Tambahkan chart untuk produk paling tidak laris
# product_chart_data_worst = (
#     main_data_filtered["product_category_name_english"]
#     .value_counts()
#     .nsmallest(10)
#     .reset_index()
#     .rename(
#         columns={
#             "count": "total_orders",
#             "product_category_name_english": "product_category",
#         }
#     )
# )

# product_chart_worst = (
#     alt.Chart(product_chart_data_worst)
#     .mark_bar(color="#ff6666")
#     .encode(
#         x=alt.X("total_orders:Q", title="Jumlah Pesanan"),
#         y=alt.Y(
#             "product_category:N",
#             title="Kategori Produk",
#             sort=alt.EncodingSortField(field="total_orders", order="ascending"),
#         ),
#         tooltip=["product_category", "total_orders"],
#     )
#     .properties(title="🔻 10 Kategori Produk Paling Tidak Laris")
#     .interactive()
# )

# st.altair_chart(product_chart_worst, use_container_width=True)

# # Tambahkan boxplot harga
# st.divider()
# st.header("💰 Distribusi Harga per Kategori Produk")

# # Ambil kategori dari data sebelumnya
# top_categories = product_chart_data["product_category"].tolist()
# worst_categories = product_chart_data_worst["product_category"].tolist()

# # Filter data untuk boxplot
# top_prices = main_data_filtered[
#     main_data_filtered["product_category_name_english"].isin(top_categories)
# ]
# worst_prices = main_data_filtered[
#     main_data_filtered["product_category_name_english"].isin(worst_categories)
# ]

# # Boxplot untuk kategori teratas
# box_top = (
#     alt.Chart(top_prices)
#     .mark_boxplot(color="#4CAF50")
#     .encode(
#         x=alt.X("price:Q", title="Harga (USD)", scale=alt.Scale(domain=[0, 500])),
#         y=alt.Y(
#             "product_category_name_english:N",
#             title="Kategori",
#             sort=alt.EncodingSortField(field="price", op="median", order="descending"),
#         ),
#     )
#     .properties(title="📈 Distribusi Harga - 10 Kategori Terlaris")
# )

# # Boxplot untuk kategori terbawah
# box_worst = (
#     alt.Chart(worst_prices)
#     .mark_boxplot(color="#ff6666")
#     .encode(
#         x=alt.X("price:Q", title="Harga (USD)", scale=alt.Scale(domain=[0, 500])),
#         y=alt.Y(
#             "product_category_name_english:N",
#             title="Kategori",
#             sort=alt.EncodingSortField(field="price", op="median", order="descending"),
#         ),
#     )
#     .properties(title="📉 Distribusi Harga - 10 Kategori Tidak Laris")
# )

# # Tampilkan boxplot
# st.altair_chart(box_top, use_container_width=True)
# st.altair_chart(box_worst, use_container_width=True)

# st.divider()
