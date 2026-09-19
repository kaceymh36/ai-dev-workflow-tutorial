"""Entry point for the ShopSmart sales dashboard."""

from decimal import Decimal
from pathlib import Path

import streamlit as st

from sales_data import SalesDataError, load_sales_data, summarize_kpis

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")

st.title("ShopSmart Sales Dashboard")
st.write("Explore sales performance across time, product categories, and regions.")

# Resolve from this file so launching from another folder still finds the CSV.
data_path = Path(__file__).resolve().parent / "data" / "sales-data.csv"
try:
    data = load_sales_data(data_path)
except SalesDataError as error:
    st.error(str(error))
    st.stop()

st.caption(
    f"Reporting period: {min(data['date']):%b %d, %Y} to {max(data['date']):%b %d, %Y}"
)

kpis = summarize_kpis(data)
# Convert exact cents to dollars only for display; formatting rounds to whole dollars.
sales_dollars = Decimal(f"{kpis['total_sales_cents']}e-2")
sales_column, orders_column = st.columns(2)
with sales_column:
    st.metric("Total Sales", f"${sales_dollars:,.0f}", border=True)
with orders_column:
    st.metric("Total Orders", f"{kpis['total_orders']:,}", border=True)

with st.container(border=True):
    st.subheader("Monthly Sales")
    st.caption("Monthly sales chart coming soon.")

category_column, region_column = st.columns(2)
with category_column:
    with st.container(border=True):
        st.subheader("Sales by Category")
        st.caption("Category breakdown coming soon.")
with region_column:
    with st.container(border=True):
        st.subheader("Sales by Region")
        st.caption("Regional breakdown coming soon.")
