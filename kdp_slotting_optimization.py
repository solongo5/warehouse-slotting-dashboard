import pandas as pd
import streamlit as st

st.set_page_config(page_title="Warehouse Slotting Optimization Tool", layout="wide")

# Load simulated data
df = pd.read_csv("data.csv")

# KPI calculations
total_skus = len(df)
misaligned = (df["Current_Location"] != df["Optimal_Location"]).sum()
misalignment_pct = round(misaligned / total_skus * 100, 1)

# Identify relocation needs
df["Needs_Relocation"] = df["Current_Location"] != df["Optimal_Location"]

# Priority SKUs: A-class + high movement
priority_df = df[(df["ABC_Class"] == "A") & (df["Movements"] > 100)]

# Dashboard title and description
st.title("📦 Warehouse Slotting Optimization Tool")
st.write(
    "Data-driven slotting analysis using simulated warehouse data to identify SKU misalignment "
    "and relocation opportunities."
)

# KPI section
col1, col2, col3 = st.columns(3)
col1.metric("Total SKUs", total_skus)
col2.metric("Misaligned SKUs", misaligned)
col3.metric("Misalignment %", f"{misalignment_pct}%")

# Business summary
st.success(f"{misaligned} SKUs ({misalignment_pct}%) require relocation based on slotting mismatch.")

st.divider()

# Relocation candidates
st.subheader("🔧 SKUs Requiring Relocation")
st.dataframe(df[df["Needs_Relocation"] == True], use_container_width=True)

# High-priority SKUs
st.subheader("🔥 High Priority SKUs (A + High Movement)")
st.dataframe(priority_df, use_container_width=True)

# Zone distribution chart
st.subheader("Zone Distribution")
zone_counts = df["Zone"].value_counts()
st.bar_chart(zone_counts)

# ABC class distribution chart
st.subheader("ABC Class Distribution")
abc_counts = df["ABC_Class"].value_counts()
st.bar_chart(abc_counts)

# Insight block
st.info(
    "Insight: High-movement A-class SKUs located outside prime zones represent the strongest "
    "relocation opportunities. Lower-priority SKUs occupying prime zones indicate inefficient "
    "space utilization."
)
