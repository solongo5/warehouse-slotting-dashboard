import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Warehouse Slotting Optimization Tool",
    layout="wide"
)

# ---------- Custom styling ----------
st.markdown("""
<style>
    .main {
        background-color: #f3f4f6;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        color: #111827;
        font-weight: 700;
    }

    h2, h3 {
        color: #111827;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #111827;
        font-weight: 700;
    }

    .insight-box {
        background-color: #e0f2fe;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #0284c7;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #0f172a;
    }

    .summary-box {
        background-color: #e8f5e9;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #16a34a;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #14532d;
    }

    .small-note {
        color: #6b7280;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load simulated data ----------
df = pd.read_csv("data.csv")

# ---------- Filter ----------
st.subheader("Filters")
selected_class = st.selectbox("ABC Class", ["All", "A", "B", "C"])

if selected_class != "All":
    df = df[df["ABC_Class"] == selected_class].copy()
else:
    df = df.copy()

st.caption(f"Current filter: {selected_class}")

# ---------- KPI calculations ----------
df["Needs_Relocation"] = df["Current_Location"] != df["Optimal_Location"]

total_skus = len(df)
misaligned = df["Needs_Relocation"].sum()
misalignment_pct = round((misaligned / total_skus) * 100, 1) if total_skus > 0 else 0.0

priority_df = df[(df["ABC_Class"] == "A") & (df["Movements"] > 100)].copy()
priority_relocation_rate = round((len(priority_df) / total_skus) * 100, 1) if total_skus > 0 else 0.0

# ---------- Insight logic ----------
prime_misplaced = df[
    (df["ABC_Class"] == "A") &
    (df["Zone"] != "Prime") &
    (df["Needs_Relocation"])
]

low_in_prime = df[
    (df["ABC_Class"] == "C") &
    (df["Zone"] == "Prime")
]

# ---------- Title ----------
st.title("Warehouse Slotting Optimization Tool")
st.write(
    "Data-driven slotting analysis using simulated warehouse data to identify "
    "SKU misalignment and relocation opportunities."
)

st.markdown("###")

# ---------- KPI cards ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total SKUs", total_skus)

with col2:
    st.metric("Misaligned SKUs", misaligned)

with col3:
    st.metric("Misalignment %", f"{misalignment_pct}%")

with col4:
    st.metric("High-Priority Segment %", f"{priority_relocation_rate}%")

# ---------- Insights ----------
st.subheader("Key Optimization Insights")

st.write(
    f"- {len(prime_misplaced)} high-priority (A-class) SKUs are outside Prime zones → relocation opportunity\n"
    f"- {len(low_in_prime)} low-priority (C-class) SKUs occupy Prime space → inefficient utilization\n"
    f"- {misaligned} SKUs ({misalignment_pct}%) require relocation based on slotting mismatch"
)

st.markdown(
    f"""
    <div class="summary-box">
        <b>{misaligned} SKUs ({misalignment_pct}%)</b> require relocation based on slotting mismatch.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- Relocation candidates ----------
st.subheader("Relocation Candidates")

relocation_candidates = df[df["Needs_Relocation"]].sort_values(
    by="Movements", ascending=False
)

st.dataframe(relocation_candidates, use_container_width=True)

st.markdown("---")

# ---------- High-priority segment ----------
st.subheader("High-Priority SKU Segment")

st.dataframe(
    priority_df.sort_values(by="Movements", ascending=False),
    use_container_width=True
)

st.markdown("---")

# ---------- Charts ----------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Zone Distribution")
    zone_counts = df["Zone"].value_counts()
    st.bar_chart(zone_counts)

with chart_col2:
    st.subheader("ABC Class Distribution")
    abc_counts = df["ABC_Class"].value_counts()
    st.bar_chart(abc_counts)

# ---------- Insight box ----------
st.markdown(
    """
    <div class="insight-box">
        <b>Interpretation:</b> The strongest optimization opportunities come from
        high-movement A-class SKUs outside Prime zones and lower-priority SKUs
        occupying Prime storage space.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<p class="small-note">This public version uses simulated data for demonstration purposes.</p>',
    unsafe_allow_html=True
)
