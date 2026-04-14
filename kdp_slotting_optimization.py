import pandas as pd
import streamlit as st

# Load data
df = pd.read_csv("data.csv")

# KPI calculations
total_skus = len(df)
misaligned = (df["Current_Location"] != df["Optimal_Location"]).sum()
misalignment_pct = round(misaligned / total_skus * 100, 1)

# Identify relocation needs
df["Needs_Relocation"] = df["Current_Location"] != df["Optimal_Location"]

# Priority SKUs (A class + high movement)
priority_df = df[(df["ABC_Class"] == "A") & (df["Movements"] > 100)]

# Streamlit UI
st.set_page_config(page_title="Warehouse Optimization", layout="wide")

st.title("📦 Warehouse Slotting Optimization Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total SKUs", total_skus)
col2.metric("Misaligned SKUs", misaligned)
col3.metric("Misalignment %", f"{misalignment_pct}%")

st.divider()

st.subheader("🔧 SKUs Requiring Relocation")
st.dataframe(df[df["Needs_Relocation"] == True])

st.subheader("🔥 High Priority SKUs (A + High Movement)")
st.dataframe(priority_df)
