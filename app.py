"""Entry point for the ShopSmart sales dashboard."""

from pathlib import Path

import streamlit as st

from sales_data import SalesDataError, load_sales_data

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

# These spaces will receive KPI values and charts in the next milestones.
sales_column, orders_column = st.columns(2)
with sales_column:
    st.subheader("Total Sales")
    st.caption("Sales total coming soon.")
with orders_column:
    st.subheader("Total Orders")
    st.caption("Order count coming soon.")

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
