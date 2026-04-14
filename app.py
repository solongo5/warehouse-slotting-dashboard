import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Warehouse Slotting Optimization Tool",
    layout="wide"
)

# ---------- Styling ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f3f4f6;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #111827;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.insight-box {
    background-color: #e0f2fe;
    padding: 16px;
    border-radius: 10px;
    border-left: 5px solid #0284c7;
    margin-top: 10px;
    margin-bottom: 10px;
}

.summary-box {
    background-color: #e8f5e9;
    padding: 16px;
    border-radius: 10px;
    border-left: 5px solid #16a34a;
    margin-top: 10px;
    margin-bottom: 10px;
}

.impact-box {
    background-color: #fff7ed;
    padding: 16px;
    border-radius: 10px;
    border-left: 5px solid #f59e0b;
    margin-top: 10px;
    margin-bottom: 10px;
}

.small-note {
    color: #6b7280;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Load data ----------
df_original = pd.read_csv("data.csv")

st.write("Rows:", len(df_original))
st.write(
    "Misaligned:",
    int((df_original["Current_Location"] != df_original["Optimal_Location"]).sum())
)
st.write(df_original[["Current_Location", "Optimal_Location"]].head(10))

st.write(df[["Zone", "Optimal_Location"]].head())

# ---------- Filters ----------
st.subheader("Filters")
col1, col2 = st.columns(2)

with col1:
    selected_class = st.selectbox("ABC Class", ["All", "A", "B", "C"])

with col2:
    min_movements = st.slider("Minimum Movements", 0, int(df_original["Movements"].max()), 0)

df = df_original.copy()

if selected_class != "All":
    df = df[df["ABC_Class"] == selected_class]

df = df[df["Movements"] >= min_movements].copy()

st.caption(f"Current filter: ABC Class = {selected_class} | Minimum Movements = {min_movements}")

# ---------- Core Logic ----------
df["Needs_Relocation"] = df["Current_Location"] != df["Optimal_Location"]

# 🔥 YOUR FINAL ASSUMPTION (aligned with screenshot)
df["Time_Saved_Min"] = df["Needs_Relocation"].apply(lambda x: 10 if x else 0)
df["Labor_Impact"] = df["Time_Saved_Min"] * (25 / 60)

# KPIs
total_skus = len(df)
misaligned = int(df["Needs_Relocation"].sum())
misalignment_pct = round((misaligned / total_skus) * 100, 1)

estimated_time_saved = round(df["Time_Saved_Min"].sum() / 60, 1)
estimated_labor = round(df["Labor_Impact"].sum(), 0)

priority_df = df_original[
    (df_original["ABC_Class"] == "A") & (df_original["Movements"] > 100)
]

priority_pct = round((len(priority_df) / len(df_original)) * 100, 1)

# ---------- Title ----------
st.title("Warehouse Slotting Optimization Tool")

st.caption("End-to-end warehouse analytics solution built using Python, Streamlit, and simulated operational data.")

st.write("""
Data-driven slotting analysis designed to identify SKU misalignment, prioritize relocation actions,
and improve warehouse picking efficiency and zone utilization.
""")

st.caption("""
Analyzed SKU-level movement and inventory data to identify misalignment, prioritize high-impact relocations,
and simulate operational efficiency gains.
""")

# ---------- KPIs ----------
k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric("Total SKUs", total_skus)
k2.metric("Misaligned SKUs", misaligned)
k3.metric("Misalignment %", f"{misalignment_pct}%")
k4.metric("High-Priority Segment %", f"{priority_pct}%")
k5.metric("Est. Picking Time Saved", f"{estimated_time_saved} hrs/week")
k6.metric("Est. Labor Impact", f"${estimated_labor:,.0f}")

st.caption("""
Illustrative estimate based on assumed 10 min weekly efficiency gain per misaligned SKU and $25/hour labor rate.
Actual impact would require operational validation.
""")

# ---------- Impact ----------
st.markdown(f"""
<div class="impact-box">
<b>Impact:</b> Identified {misaligned} relocation opportunities across the analyzed SKU set,
prioritizing high-movement A-class items to improve picking efficiency and optimize Prime zone utilization.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="impact-box">
<b>Top Finding:</b> High-movement A-class SKUs are not consistently placed in Prime zones,
indicating missed opportunities to improve pick speed and space utilization.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
**Business Impact:** Potential to reduce pick effort by ~{estimated_time_saved} hours/week
through targeted relocation of misaligned high-demand SKUs.
""")

# ---------- Insights ----------
st.subheader("Key Optimization Insights")

prime_misplaced = df[(df["ABC_Class"] == "A") & (df["Zone"] != "Prime") & (df["Needs_Relocation"])]
low_in_prime = df[(df["ABC_Class"] == "C") & (df["Zone"] == "Prime")]

st.write(f"""
- {len(prime_misplaced)} high-priority (A-class) SKUs outside Prime zones → relocation opportunity  
- {len(low_in_prime)} low-priority (C-class) SKUs occupy Prime space → inefficient utilization  
- {misaligned} SKUs ({misalignment_pct}%) require relocation
""")

st.markdown(f"""
<div class="summary-box">
<b>{misaligned} SKUs ({misalignment_pct}%)</b> require relocation based on slotting mismatch.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
<b>Recommended Action:</b> Move high-movement A-class SKUs into Prime zones and reassign
lower-priority inventory to secondary storage.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- Top Moves ----------
st.subheader("Top 10 Priority Moves (Highest Impact)")

top_moves = df[df["Needs_Relocation"]].sort_values(by="Movements", ascending=False).head(10)

st.caption(f"Showing {len(top_moves)} high-impact relocation opportunities based on current filters.")

st.dataframe(top_moves[
    ["SKU_ID","ABC_Class","Zone","Current_Location","Movements","Stock_Qty","Optimal_Location","Needs_Relocation"]
], use_container_width=True)

st.markdown("---")

# ---------- Critical SKUs ----------
st.subheader("A-Class High-Movement SKUs (Critical Items)")

st.dataframe(priority_df.sort_values(by="Movements", ascending=False), use_container_width=True)

st.caption("These SKUs represent the highest operational impact and should be prioritized.")

st.markdown("---")

# ---------- Before vs After ----------
st.subheader("Before vs. After Optimization Summary")

before_after = pd.DataFrame({
    "Scenario": ["Current State", "After Optimization"],
    "Misaligned SKUs": [misaligned, 0],
    "Picking Time Saved (hrs/week)": [0, estimated_time_saved],
    "Labor Impact ($/week)": [0, estimated_labor]
})

st.dataframe(before_after, use_container_width=True)

st.markdown("---")

# ---------- Charts ----------
st.subheader("Operational Patterns & Optimization Opportunities")

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Current Zone Utilization (Imbalance)")
    zone = df["Zone"].value_counts().reset_index()
    zone.columns = ["Zone","Count"]

    st.altair_chart(
        alt.Chart(zone).mark_bar().encode(
            x="Zone",
            y="Count",
            color="Zone"
        ),
        use_container_width=True
    )

with c2:
    st.markdown("### Inventory Mix by ABC Class (Optimization Opportunity)")
    abc = df["ABC_Class"].value_counts().reset_index()
    abc.columns = ["Class","Count"]

    st.altair_chart(
        alt.Chart(abc).mark_bar().encode(
            x="Class",
            y="Count",
            color="Class"
        ),
        use_container_width=True
    )

# ---------- Interpretation ----------
st.markdown("""
<div class="insight-box">
<b>Interpretation:</b> The strongest optimization opportunities come from high-movement
A-class SKUs outside Prime zones and lower-priority SKUs occupying Prime space.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.caption("Portfolio Project | Warehouse Slotting Optimization | Python, SQL, Streamlit")
st.markdown('<p class="small-note">This public version uses simulated data.</p>', unsafe_allow_html=True)
