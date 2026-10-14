from pathlib import Path
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import plotly.express as px

from src.data_cleaning import clean_sales_data
from src.sales_analysis import (calculate_kpis, monthly_sales_trend, yearly_sales_trend,
    product_performance, category_performance, region_performance, segment_performance,
    discount_profit_analysis, low_performing_products)
from src.visualizations import monthly_trend_chart, revenue_profit_chart, horizontal_bar
from src.ai_insights import generate_rule_based_insights, generate_llm_summary

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

st.set_page_config(page_title="Sales Analytics & AI Insights", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")
st.markdown("""
<style>
.block-container {padding-top: 1.3rem; padding-bottom: 2rem;}
div[data-testid="stMetric"] {background: #f4f7fb; border: 1px solid #e1e8f0;
  padding: 14px 16px; border-radius: 12px;}
section[data-testid="stSidebar"] {background: #f8fafc;}
h1, h2, h3 {letter-spacing: -0.02em;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Sales Data Analysis & AI-Powered Insights")
st.caption("Interactive sales performance dashboard • Rule-based insights work without an API key")

@st.cache_data
def load_data(path: str, mtime: float):
    raw = pd.read_csv(path)
    return clean_sales_data(raw), len(raw)

default_csv = ROOT / "sales_data.csv"
uploaded = st.sidebar.file_uploader("Upload a sales CSV (optional)", type=["csv"])
try:
    if uploaded is not None:
        raw = pd.read_csv(uploaded)
        data = clean_sales_data(raw)
        raw_count = len(raw)
    else:
        data, raw_count = load_data(str(default_csv), default_csv.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load or clean the dataset: {exc}")
    st.stop()

if data.empty:
    st.warning("No usable rows remain after cleaning. Check the CSV fields and values.")
    st.stop()

st.sidebar.header("Filters")
min_date, max_date = data["Order Date"].min().date(), data["Order Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
regions = sorted(data["Region"].dropna().unique().tolist())
categories = sorted(data["Product Category"].dropna().unique().tolist())
segments = sorted(data["Customer Segment"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Product category", categories, default=categories)
selected_segments = st.sidebar.multiselect("Customer segment", segments, default=segments)
products = sorted(data["Product Name"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect("Product", products, default=products)

filtered = data.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    filtered = filtered[filtered["Order Date"].between(start, end)]
filtered = filtered[
    filtered["Region"].isin(selected_regions) &
    filtered["Product Category"].isin(selected_categories) &
    filtered["Customer Segment"].isin(selected_segments) &
    filtered["Product Name"].isin(selected_products)
]
if filtered.empty:
    st.warning("No rows match these filters. Change one or more filters.")
    st.stop()

k = calculate_kpis(filtered)
st.caption(f"Showing {len(filtered):,} cleaned rows from {raw_count:,} raw CSV rows. Exact duplicate rows and unusable records are removed during cleaning.")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"${k['total_revenue']:,.0f}")
c2.metric("Total Profit", f"${k['total_profit']:,.0f}")
c3.metric("Distinct Orders", f"{k['total_orders']:,}")
c4.metric("Units Sold", f"{k['units_sold']:,}")
c5.metric("Avg. Order Value", f"${k['average_order_value']:,.2f}")
st.metric("Profit Margin", f"{k['profit_margin_pct']:.1f}%")

tab_overview, tab_products, tab_customers, tab_ai, tab_data = st.tabs(
    ["Overview", "Products & Categories", "Regions & Customers", "AI Insights", "Data & Export"])

with tab_overview:
    trend = monthly_sales_trend(filtered)
    left, right = st.columns(2)
    with left:
        st.plotly_chart(monthly_trend_chart(trend), use_container_width=True)
    with right:
        st.plotly_chart(revenue_profit_chart(trend), use_container_width=True)
    st.subheader("Yearly performance")
    st.dataframe(yearly_sales_trend(filtered), use_container_width=True, hide_index=True)
    growth = None
    if len(trend) >= 2 and float(trend.iloc[-2]["Revenue"]) != 0:
        growth = (float(trend.iloc[-1]["Revenue"]) - float(trend.iloc[-2]["Revenue"])) / float(trend.iloc[-2]["Revenue"]) * 100
    st.info(f"Latest month-over-month revenue growth: {growth:.1f}%" if growth is not None else "Month-over-month growth requires at least two months and non-zero previous-month revenue.")

with tab_products:
    products_df = product_performance(filtered)
    categories_df = category_performance(filtered)
    left, right = st.columns(2)
    with left:
        st.plotly_chart(horizontal_bar(products_df.head(10), "Revenue", "Product Name", "Top 10 Products by Revenue"), use_container_width=True)
    with right:
        st.plotly_chart(px.bar(categories_df, x="Product Category", y="Profit", title="Profit by Category"), use_container_width=True)
    st.subheader("Lowest-profit products to review")
    st.dataframe(low_performing_products(filtered, 10), use_container_width=True, hide_index=True)
    st.subheader("Discount versus profit")
    disc = discount_profit_analysis(filtered)
    st.plotly_chart(px.bar(disc, x="Discount Band", y="Profit", title="Profit by Discount Band"), use_container_width=True)

with tab_customers:
    left, right = st.columns(2)
    with left:
        region_df = region_performance(filtered)
        st.plotly_chart(px.bar(region_df, x="Region", y="Revenue", title="Revenue by Region"), use_container_width=True)
    with right:
        segment_df = segment_performance(filtered)
        st.plotly_chart(px.pie(segment_df, names="Customer Segment", values="Revenue", title="Revenue by Customer Segment"), use_container_width=True)
    st.subheader("Regional performance")
    st.dataframe(region_df, use_container_width=True, hide_index=True)
    st.subheader("Customer segment performance")
    st.dataframe(segment_df, use_container_width=True, hide_index=True)

with tab_ai:
    st.subheader("Rule-based insights (calculated from filtered data)")
    insights = generate_rule_based_insights(filtered)
    for item in insights["insights"]:
        st.write("• " + item)
    st.subheader("Recommended actions")
    for item in insights["recommendations"]:
        st.write("• " + item)
    st.caption("These findings are deterministic calculations and rules, not LLM-generated facts.")
    if st.button("Generate optional LLM executive summary"):
        with st.spinner("Requesting optional LLM summary..."):
            summary, error = generate_llm_summary(insights)
        if summary:
            st.subheader("LLM-generated explanation")
            st.write(summary)
            st.caption("LLM-generated narrative; verify recommendations against source data.")
        else:
            st.warning(error or "LLM summary unavailable.")

with tab_data:
    st.subheader("Filtered data")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", data=csv_bytes,
                       file_name="filtered_sales_data.csv", mime="text/csv")
    st.download_button("Download KPI summary CSV",
        data=pd.DataFrame([k]).to_csv(index=False).encode("utf-8"),
        file_name="sales_kpi_summary.csv", mime="text/csv")
    st.caption("Cleaning policy: exact duplicates removed; invalid dates and rows missing core numeric fields removed; missing descriptive fields set to Unknown; missing discounts set to 0.")
