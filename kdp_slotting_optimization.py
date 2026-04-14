import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="Warehouse Slotting Optimization Tool",
    layout="wide"
)

# ---------- Custom styling ----------
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6;
    }

    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    .main .block-container {
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

    .impact-box {
        background-color: #fff7ed;
        padding: 16px;
        border-radius: 10px;
        border-left: 5px solid #f59e0b;
        margin-top: 10px;
        margin-bottom: 10px;
        color: #7c2d12;
    }

    .small-note {
        color: #6b7280;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Load simulated data ----------
df_original = pd.read_csv("data.csv")

# ---------- Filter ----------
st.subheader("Filters")
selected_class = st.selectbox("ABC Class", ["All", "A", "B", "C"])

if selected_class != "All":
    df = df_original[df_original["ABC_Class"] == selected_class].copy()
else:
    df = df_original.copy()

st.caption(f"Current filter: {selected_class}")

# ---------- KPI calculations ----------
df["Needs_Relocation"] = df["Current_Location"] != df["Optimal_Location"]

total_skus = len(df)
misaligned = int(df["Needs_Relocation"].sum())
misalignment_pct = round((misaligned / total_skus) * 100, 1) if total_skus > 0 else 0.0

# A-class / high-movement segment calculated on full dataset
priority_df = df_original[
    (df_original["ABC_Class"] == "A") & (df_original["Movements"] > 100)
].copy()

priority_segment_pct = round((len(priority_df) / len(df_original)) * 100, 1) if len(df_original) > 0 else 0.0

# Estimated impact metric
estimated_time_saved = round(misaligned * 0.5, 1)  # simple demo assumption

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

relocation_candidates = df[df["Needs_Relocation"]].sort_values(
    by="Movements", ascending=False
)

top_moves = relocation_candidates[
    (relocation_candidates["ABC_Class"] == "A") &
    (relocation_candidates["Movements"] > 100)
].sort_values(by="Movements", ascending=False).head(10)


# ---------- Title ----------
st.title("Warehouse Slotting Optimization Tool")
st.caption("End-to-end warehouse analytics solution built using Python, Streamlit, and simulated operational data.")
st.write(
    "Data-driven slotting analysis designed to identify SKU misalignment, prioritize relocation actions, "
    "and improve warehouse picking efficiency and zone utilization."
)

st.caption(
    "Analyzed SKU-level movement and inventory data to identify misalignment, prioritize high-impact relocations, "
    "and simulate operational efficiency gains."
)

st.markdown("<br>", unsafe_allow_html=True)


# ---------- KPI cards ----------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total SKUs", total_skus)

with col2:
    st.metric("Misaligned SKUs", misaligned)

with col3:
    st.metric("Misalignment %", f"{misalignment_pct}%")

with col4:
    st.metric("High-Priority Segment %", f"{priority_segment_pct}%")

with col5:
    st.metric("Est. Picking Time Saved", f"{estimated_time_saved} hrs/week")
    
st.caption("Assumes ~0.5 min reduction per pick after relocation (illustrative estimate)")
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Impact framing ----------
st.markdown(
    """
    <div class="impact-box">
        <b>Impact:</b> Identified relocation opportunities across the analyzed SKU set, prioritizing
        high-movement A-class items to improve picking efficiency and optimize Prime zone utilization.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="impact-box">
        <b>Top Finding:</b> High-movement A-class SKUs are not consistently placed in Prime zones,
        indicating missed opportunities to improve pick speed and space utilization.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

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

st.markdown(
    """
    <div class="insight-box">
        <b>Recommended Action:</b> Move high-movement A-class SKUs into Prime zones and reassign
        lower-priority inventory to secondary storage to improve pick speed and reduce congestion.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Top priority moves ----------
st.subheader("Top 10 Priority Moves (Highest Impact)")
st.dataframe(top_moves, use_container_width=True, height=350)

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Recommended relocation actions ----------
st.subheader("Recommended Relocation Actions")
st.dataframe(relocation_candidates, use_container_width=True)

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Critical items ----------
st.subheader("A-Class High-Movement SKUs (Critical Items)")

priority_display = priority_df.sort_values(by="Movements", ascending=False)

if priority_display.empty:
    st.info("No A-class high-movement SKUs found under current data conditions.")
else:
    st.dataframe(priority_display, use_container_width=True)

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)

# ---------- Charts ----------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Current Zone Utilization (Potential Imbalance)")
    zone_counts = df["Zone"].value_counts().reset_index()
    zone_counts.columns = ["Zone", "Count"]

    zone_chart = alt.Chart(zone_counts).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X("Zone:N", sort="-y", title=""),
        y=alt.Y("Count:Q", title=""),
        color=alt.Color(
            "Zone:N",
            scale=alt.Scale(
                domain=["Prime", "Secondary", "Reserve"],
                range=["#2563eb", "#16a34a", "#f59e0b"]
            ),
            legend=None
        ),
        tooltip=["Zone", "Count"]
    ).properties(
        height=300
    )

    st.altair_chart(zone_chart, use_container_width=True, theme=None)

with chart_col2:
    st.subheader("Inventory Mix by ABC Class (Optimization Opportunity)")
    abc_counts = df["ABC_Class"].value_counts().reset_index()
    abc_counts.columns = ["ABC_Class", "Count"]

    abc_chart = alt.Chart(abc_counts).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X("ABC_Class:N", title=""),
        y=alt.Y("Count:Q", title=""),
        color=alt.Color(
            "ABC_Class:N",
            scale=alt.Scale(
                domain=["A", "B", "C"],
                range=["#dc2626", "#2563eb", "#16a34a"]
            ),
            legend=None
        ),
        tooltip=["ABC_Class", "Count"]
    ).properties(
        height=300
    )

    st.altair_chart(abc_chart, use_container_width=True, theme=None)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Interpretation ----------
st.markdown(
    """
    <div class="insight-box">
        <b>Interpretation:</b> The strongest optimization opportunities come from high-movement
        A-class SKUs outside Prime zones and lower-priority SKUs occupying Prime storage space.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<p class="small-note">This public version uses simulated data for demonstration purposes.</p>',
    unsafe_allow_html=True
)
