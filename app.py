"""Entry point for the ShopSmart sales dashboard."""

from decimal import Decimal
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go

from sales_data import SalesDataError, load_sales_data, monthly_sales, summarize_kpis

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
    trend = monthly_sales(data)
    # Keep exact currency text for hover; floats are only used for plotting.
    monthly_dollars = [Decimal(f"{cents}e-2") for cents in trend['total_amount_cents']]
    month_labels = [month.strftime("%b %Y") for month in trend['month']]
    figure = go.Figure(go.Scatter(
        x=month_labels,
        y=[float(amount) for amount in monthly_dollars],
        mode="lines+markers",
        line=dict(color="#2563EB", width=2),
        marker=dict(size=6),
        customdata=[f"${amount:,.2f}" for amount in monthly_dollars],
        hovertemplate="%{x}<br>Sales: %{customdata}<extra></extra>",
    ))
    figure.update_layout(
        template="plotly_white",
        height=360,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="Month", type="category", categoryorder="array",
                   categoryarray=month_labels, showgrid=False),
        yaxis=dict(title="Sales (USD)", tickprefix="$", tickformat=",.0f",
                   rangemode="tozero", gridcolor="#E5E7EB"),
        showlegend=False,
    )
    st.plotly_chart(figure, width="stretch", config={"displaylogo": False})

category_column, region_column = st.columns(2)
with category_column:
    with st.container(border=True):
        st.subheader("Sales by Category")
        st.caption("Category breakdown coming soon.")
with region_column:
    with st.container(border=True):
        st.subheader("Sales by Region")
        st.caption("Regional breakdown coming soon.")
