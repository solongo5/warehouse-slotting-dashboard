import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import altair as alt

st.set_page_config(
    page_title="KDP Warehouse Slotting Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME & GLOBAL CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0b0d14 !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: #111420 !important;
    border-right: 1px solid #1e2235 !important;
}

[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

.main .block-container {
    padding-top: 0rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

h1, h2, h3 {
    font-family: 'IBM Plex Sans', sans-serif !important;
    color: #f1f5f9 !important;
}

[data-testid="stDataFrame"] {
    background: #111420 !important;
}

[data-testid="stMetric"] {
    background: transparent !important;
}

[data-testid="stSelectbox"] > div,
[data-baseweb="select"] {
    background-color: #1a1f2e !important;
    border-color: #2d3450 !important;
    color: #e2e8f0 !important;
}

div[data-baseweb="popover"] {
    background-color: #1a1f2e !important;
}

[data-testid="stSlider"] > div > div > div > div {
    background: #00c9a7 !important;
}

hr {
    border-color: #1e2235 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #64748b !important;
}

[data-testid="stDownloadButton"] button {
    background: #1a1f2e !important;
    border: 1px solid #2d3450 !important;
    color: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER BAR
# =========================================================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #0f1523 0%, #141929 100%);
    border-bottom: 1px solid #1e2d4a;
    padding: 14px 24px;
    margin: -1rem -2rem 1.5rem -2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
">
    <div>
        <span style="
            font-family: 'IBM Plex Mono', monospace;
            font-size: 13px;
            font-weight: 600;
            color: #00c9a7;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        ">KEURIG DR PEPPER</span>
        <span style="color: #334155; margin: 0 10px;">|</span>
        <span style="
            font-family: 'IBM Plex Mono', monospace;
            font-size: 13px;
            color: #94a3b8;
            letter-spacing: 0.05em;
        ">SUMNER DC — WAREHOUSE RE-SLOTTING DASHBOARD</span>
        <span style="color: #334155; margin: 0 10px;">|</span>
        <span style="
            font-family: 'IBM Plex Mono', monospace;
            font-size: 12px;
            color: #475569;
        ">MSBA TEAM 3 · PUBLIC DEMO</span>
    </div>
    <div style="
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        color: #475569;
    ">Last Refresh: Q1 2026 &nbsp;|&nbsp; Simulated Data</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
df_original = pd.read_csv("data.csv")

# Normalize column names so the app works with your new simulated dataset
if "Current_Zone" in df_original.columns and "Zone" not in df_original.columns:
    df_original["Zone"] = df_original["Current_Zone"]

if "Recommended_Zone" not in df_original.columns:
    df_original["Recommended_Zone"] = df_original["Zone"]

if "Needs_Relocation" in df_original.columns:
    df_original["Needs_Relocation"] = df_original["Needs_Relocation"].astype(int).astype(bool)
else:
    df_original["Needs_Relocation"] = df_original["Current_Location"] != df_original["Optimal_Location"]


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown("""
<div style="
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.1em;
    color: #00c9a7;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e2235;
">⚙ Dashboard Controls</div>
""", unsafe_allow_html=True)

selected_class = st.sidebar.selectbox("ABC Class", ["All", "A", "B", "C"])
min_movements = st.sidebar.slider("Minimum Movements", 0, int(df_original["Movements"].max()), 0)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="font-family:'IBM Plex Mono',monospace; font-size:11px; color:#00c9a7; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:10px;">Zone Breakdown</div>
<table style="width:100%; font-size:12px; border-collapse:collapse; color:#94a3b8;">
  <tr style="color:#475569; font-size:11px;">
    <td>LOCATION</td><td align="right">FREE</td><td align="right">OCC</td><td align="right">BLK</td><td align="right">TOT</td>
  </tr>
  <tr><td style="color:#e2e8f0;">Z1 Prime</td><td align="right" style="color:#52c41a;">885</td><td align="right" style="color:#f59e0b;">83</td><td align="right" style="color:#ef4444;">13</td><td align="right">981</td></tr>
  <tr><td style="color:#e2e8f0;">Z2 Secondary</td><td align="right" style="color:#52c41a;">715</td><td align="right" style="color:#f59e0b;">198</td><td align="right" style="color:#ef4444;">70</td><td align="right">983</td></tr>
  <tr><td style="color:#e2e8f0;">Z3 Cold</td><td align="right" style="color:#52c41a;">61</td><td align="right" style="color:#f59e0b;">0</td><td align="right" style="color:#ef4444;">0</td><td align="right">61</td></tr>
  <tr><td style="color:#e2e8f0;">DR Flex</td><td align="right" style="color:#52c41a;">0</td><td align="right" style="color:#f59e0b;">0</td><td align="right" style="color:#ef4444;">0</td><td align="right">0</td></tr>
</table>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="font-size:11px; color:#475569; font-family:'IBM Plex Mono',monospace;">
ABC: {selected_class} &nbsp;|&nbsp; Min Moves: {min_movements}
</div>
""", unsafe_allow_html=True)


# =========================================================
# FILTER DATA
# =========================================================
df = df_original.copy()

if selected_class != "All":
    df = df[df["ABC_Class"] == selected_class]

df = df[df["Movements"] >= min_movements].copy()

# Keep relocation flag from data.csv so total remains 59 in unfiltered view
df["Needs_Relocation"] = df["Needs_Relocation"].astype(bool)

# Assumptions for directional impact estimate
df["Time_Saved_Min"] = df["Needs_Relocation"].apply(lambda x: 10 if x else 0)
df["Labor_Impact"] = df["Time_Saved_Min"] * (25 / 60)

total_skus = len(df)
misaligned = int(df["Needs_Relocation"].sum())
misalignment_pct = round((misaligned / total_skus) * 100, 1) if total_skus else 0

estimated_time_saved = round(df["Time_Saved_Min"].sum() / 60, 1)
estimated_labor = round(df["Labor_Impact"].sum(), 0)

a_count = int((df["ABC_Class"] == "A").sum())
b_count = int((df["ABC_Class"] == "B").sum())
c_count = int((df["ABC_Class"] == "C").sum())

priority_df = df_original[
    (df_original["ABC_Class"] == "A") &
    (df_original["Movements"] > 100)
].copy()

priority_pct = round((len(priority_df) / len(df_original)) * 100, 1)

prime_misplaced = df[
    (df["ABC_Class"] == "A") &
    (df["Zone"] != "Prime") &
    (df["Needs_Relocation"])
]

low_in_prime = df[
    (df["ABC_Class"] == "C") &
    (df["Zone"] == "Prime")
]


# =========================================================
# KPI CARDS
# =========================================================
def kpi_card(label, value, color="#00c9a7", sub=None):
    sub_html = (
        f'<div style="font-size:11px;color:#475569;margin-top:4px;">{sub}</div>'
        if sub else ""
    )

    return f"""
    <div style="
        background:#111420;
        border:1px solid #1e2235;
        border-top:2px solid {color};
        border-radius:10px;
        padding:18px 20px;
        text-align:left;
        min-height:95px;
    ">
        <div style="
            font-size:11px;
            color:#475569;
            font-family:'IBM Plex Mono',monospace;
            letter-spacing:0.08em;
            text-transform:uppercase;
            margin-bottom:8px;
        ">
            {label}
        </div>

        <div style="
            font-size:28px;
            font-weight:700;
            color:{color};
            font-family:'IBM Plex Sans',sans-serif;
            line-height:1;
        ">
            {value}
        </div>

        {sub_html}
    </div>
    """


# =========================================================
# EXECUTIVE KPI ROW
# =========================================================

cols = st.columns(8)

cards = [
    (
        "Total SKUs",
        str(total_skus),
        "#e2e8f0",
        "active finished-goods SKUs"
    ),

    (
        "Relocation SKUs",
        str(misaligned),
        "#f59e0b",
        "recommended to move"
    ),

    (
        "Relocation %",
        f"{misalignment_pct:.1f}%",
        "#ef4444",
        "of analyzed SKUs"
    ),

    (
        "Storage Bins",
        "5,617",
        "#ec4899",
        "facility storage locations"
    ),

    (
        "SAP Records",
        "423K",
        "#3b82f6",
        "movement transactions analyzed"
    ),

    (
        "Facility Size",
        "224K",
        "#00c9a7",
        "square feet"
    ),

    (
        "Est. Time Saved",
        "9.8 hrs/wk",
        "#14b8a6",
        "illustrative estimate"
    ),

    (
        "Est. Labor Impact",
        "$246/wk",
        "#a78bfa",
        "at $25/hr labor rate"
    ),
]

for col, (label, value, color, sub) in zip(cols, cards):
    with col:
        st.markdown(
            kpi_card(label, value, color, sub),
            unsafe_allow_html=True
        )

st.markdown(
    "<div style='margin-top:10px;'></div>",
    unsafe_allow_html=True
)


# =========================================================
# INSIGHT BANNERS
# =========================================================
def banner(icon, label, text, bg, border):
    return f"""
    <div style="
        background:{bg};
        border-left:4px solid {border};
        border-radius:8px;
        padding:14px 18px;
        margin:6px 0;
        font-size:14px;
        color:#e2e8f0;
    "><span style="color:{border};font-weight:700;">{icon} {label}</span> {text}</div>"""


b1, b2 = st.columns(2)

with b1:
    st.markdown(banner(
        "⚡", "Impact:",
        f"Identified {misaligned} relocation opportunities across {total_skus} SKUs ({misalignment_pct}%).",
        "#0f2a1a", "#00c9a7"
    ), unsafe_allow_html=True)

with b2:
    st.markdown(banner(
        "🎯", "Key Finding:",
        "A-class SKUs should be prioritized for Prime zones, while lower-priority inventory can be shifted to secondary storage.",
        "#1a1a0f", "#f59e0b"
    ), unsafe_allow_html=True)

st.markdown("<div style='margin:12px 0; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)


# =========================================================
# WAREHOUSE BIN MAP
# =========================================================
st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">
▦ Recommended Warehouse Bin Map
</div>
<div style="font-size:13px;color:#475569;margin-bottom:12px;">
Synthetic lane-level view — bin occupancy and ABC class distribution (simulated from operational logic)
</div>
""", unsafe_allow_html=True)


def generate_synthetic_map(seed=42):
    random.seed(seed)

    sku_pool = df_original[["SKU_ID", "ABC_Class", "Zone", "Needs_Relocation"]].copy()

    zone_lanes = {
        "Zone 1 Prime": ["HA", "HB", "HC", "HD", "HE", "HF", "HG", "HH", "HI", "HJ", "HK", "HL", "HM"],
        "Zone 2 Secondary": ["RG", "RF", "RE", "RD", "RC", "RB", "RA", "RH"],
        "Zone 3 Cold": ["WI"],
    }

    zone_occ = {
        "Zone 1 Prime": 0.065,
        "Zone 2 Secondary": 0.17,
        "Zone 3 Cold": 0.02,
    }

    zone_blk = {
        "Zone 1 Prime": 0.01,
        "Zone 2 Secondary": 0.06,
        "Zone 3 Cold": 0.0,
    }

    rows = []

    for zone, lanes in zone_lanes.items():
        occ_rate = zone_occ[zone]
        blk_rate = zone_blk[zone]

        for lane in lanes:
            n_bins = 48

            for i in range(n_bins):
                r = random.random()

                if r < blk_rate:
                    status, abc, sku = "Blocked", "", ""

                elif r < blk_rate + occ_rate:
                    status = "Occupied"
                    zone_short = zone.split()[1]
                    pool = sku_pool[sku_pool["Zone"] == zone_short]

                    if pool.empty:
                        pool = sku_pool

                    row = pool.sample(1).iloc[0]
                    abc = row["ABC_Class"]
                    sku = row["SKU_ID"]

                else:
                    status, abc, sku = "Available", "", ""

                rows.append({
                    "Location": f"{lane}-{i+1:03d}",
                    "Lane": lane,
                    "Zone": zone,
                    "Bin_Status": status,
                    "ABC_Class": abc,
                    "SKU": sku,
                })

    return pd.DataFrame(rows)


def get_bin_color(status, abc):
    status = str(status)

    if isinstance(abc, pd.Series):
        abc = abc.iloc[0] if len(abc) > 0 else ""

    abc = str(abc).strip().upper()

    if status == "Blocked":
        return "#3a1a1a"

    if status == "Available":
        return "#12211a"

    color_map = {
        "A": "#ef4444",
        "B": "#f59e0b",
        "C": "#22c55e"
    }

    return color_map.get(abc, "#1e40af")


def render_bin_map(map_df):
    zones = ["Zone 1 Prime", "Zone 2 Secondary", "Zone 3 Cold"]

    html = """
    <style>
    body { margin:0; background:#0b0d14; font-family:'IBM Plex Mono',monospace; }
    .map-wrap { padding: 0; }
    .zone-header {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #00c9a7;
        margin: 20px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #1e2235;
    }
    .lanes-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 8px;
    }
    .lane-block {
        background: #111420;
        border: 1px solid #1e2235;
        border-radius: 8px;
        padding: 10px 10px 8px;
        min-width: 110px;
    }
    .lane-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.1em;
        color: #64748b;
        margin-bottom: 7px;
        text-align: center;
    }
    .bin-grid {
        display: grid;
        grid-template-columns: repeat(6, 14px);
        gap: 3px;
    }
    .bin {
        width: 14px;
        height: 14px;
        border-radius: 2px;
    }
    .legend {
        display: flex;
        gap: 18px;
        flex-wrap: wrap;
        margin-bottom: 14px;
        font-size: 11px;
        color: #64748b;
        letter-spacing: 0.05em;
    }
    .legend-item { display: flex; align-items: center; gap: 6px; }
    .legend-dot { width: 12px; height: 12px; border-radius: 2px; }
    </style>

    <div class="map-wrap">
    <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background:#ef4444;"></div>A-Class</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;"></div>B-Class</div>
        <div class="legend-item"><div class="legend-dot" style="background:#22c55e;"></div>C-Class</div>
        <div class="legend-item"><div class="legend-dot" style="background:#12211a;border:1px solid #1e3a2a;"></div>Available</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3a1a1a;border:1px solid #5a2222;"></div>Blocked</div>
    </div>
    """

    for zone in zones:
        zone_df = map_df[map_df["Zone"] == zone]

        if zone_df.empty:
            continue

        lanes = zone_df["Lane"].unique()

        html += f'<div class="zone-header">{zone}</div>'
        html += '<div class="lanes-row">'

        for lane in lanes:
            lane_df = zone_df[zone_df["Lane"] == lane]
            html += f'<div class="lane-block"><div class="lane-label">{lane}</div><div class="bin-grid">'

            for _, row in lane_df.iterrows():
                color = get_bin_color(row["Bin_Status"], row["ABC_Class"])
                tooltip = f"Loc: {row['Location']} | SKU: {row['SKU']} | ABC: {row['ABC_Class']} | {row['Bin_Status']}"
                html += f'<div class="bin" style="background:{color};" title="{tooltip}"></div>'

            html += "</div></div>"

        html += "</div>"

    html += "</div>"

    return html


map_df = generate_synthetic_map()
bin_map_html = render_bin_map(map_df)
components.html(bin_map_html, height=680, scrolling=True)

st.markdown("<div style='margin:16px 0; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)


# =========================================================
# KEY INSIGHTS
# =========================================================
st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;">
▸ Key Optimization Insights
</div>
""", unsafe_allow_html=True)

i1, i2, i3 = st.columns(3)

insight_cards = [
    ("A-Class Outside Prime", str(len(prime_misplaced)), "#ef4444", "SKUs to pull into Zone 1"),
    ("C-Class in Prime", str(len(low_in_prime)), "#f59e0b", "Prime space being used"),
    ("Total Relocation Needed", str(misaligned), "#00c9a7", f"{misalignment_pct}% of filtered SKUs"),
]

for col, (label, val, color, sub) in zip([i1, i2, i3], insight_cards):
    col.markdown(kpi_card(label, val, color, sub), unsafe_allow_html=True)

st.markdown("<div style='margin:12px 0;'></div>", unsafe_allow_html=True)

st.markdown(banner(
    "✅", "Recommended Action:",
    "Prioritize the 59 relocation candidates first, especially A-class SKUs outside Prime zones, instead of re-slotting the entire warehouse.",
    "#0a1a12", "#00c9a7"
), unsafe_allow_html=True)

st.markdown("<div style='margin:16px 0; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)


# =========================================================
# TOP 10 PRIORITY MOVES
# =========================================================
st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">
▸ Top 10 Priority Moves — Highest Impact
</div>
""", unsafe_allow_html=True)

top_moves = df[df["Needs_Relocation"]].sort_values(
    by=["ABC_Class", "Movements", "Stock_Qty"],
    ascending=[True, False, False]
).head(10)

st.dataframe(
    top_moves[[
        "SKU_ID",
        "ABC_Class",
        "Speed_Class",
        "Zone",
        "Recommended_Zone",
        "Current_Location",
        "Movements",
        "Stock_Qty",
        "Optimal_Location"
    ]],
    use_container_width=True,
    hide_index=True
)

st.markdown("<div style='margin:16px 0; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)


# =========================================================
# A-CLASS CRITICAL SKUS
# =========================================================
st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#ef4444;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">
▸ A-Class High-Movement SKUs — Critical Items
</div>
""", unsafe_allow_html=True)

st.dataframe(
    priority_df.sort_values(by="Movements", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.caption("These SKUs represent the highest operational impact and should be reviewed first for Prime-zone placement.")

st.markdown("<div style='margin:16px 0; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)


# =========================================================
# BEFORE VS AFTER
# =========================================================
st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">
▸ Before vs. After Optimization
</div>
""", unsafe_allow_html=True)

before_after = pd.DataFrame({
    "Scenario": ["Current State", "After Optimization"],
    "Relocation Candidates": [misaligned, 0],
    "Picking Time Saved (hrs/week)": [0, estimated_time_saved],
    "Labor Impact ($/week)": [0, int(estimated_labor)],
})

st.dataframe(before_after, use_container_width=True, hide_index=True)

st.markdown("<div style='margin:16px 0; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)


# =========================================================
# CHARTS
# =========================================================
st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;">
▸ Operational Patterns & Optimization Opportunities
</div>
""", unsafe_allow_html=True)

chart_cfg = alt.theme.enable("dark") if hasattr(alt.theme, "enable") else None

DARK_CHART = {
    "config": {
        "background": "#111420",
        "view": {"fill": "#111420", "stroke": "transparent"},
        "axis": {
            "gridColor": "#1e2235",
            "domainColor": "#1e2235",
            "tickColor": "#1e2235",
            "labelColor": "#64748b",
            "titleColor": "#94a3b8",
        },
        "legend": {"labelColor": "#94a3b8", "titleColor": "#94a3b8"},
        "title": {"color": "#e2e8f0"},
    }
}

c1, c2 = st.columns(2)

with c1:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>Zone Utilization Current</div>", unsafe_allow_html=True)

    zone_counts = df["Zone"].value_counts().reset_index()
    zone_counts.columns = ["Zone", "Count"]

    zone_color = alt.Color(
        "Zone:N",
        scale=alt.Scale(
            domain=["Prime", "Secondary", "Reserve"],
            range=["#00c9a7", "#3b82f6", "#f59e0b"]
        )
    )

    chart1 = (
        alt.Chart(zone_counts)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Zone:N", axis=alt.Axis(labelAngle=0)),
            y="Count:Q",
            color=zone_color
        )
        .properties(height=220)
        .configure(**DARK_CHART["config"])
    )

    st.altair_chart(chart1, use_container_width=True)

with c2:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>ABC Class Mix Optimization Opportunity</div>", unsafe_allow_html=True)

    abc_counts = df["ABC_Class"].value_counts().reset_index()
    abc_counts.columns = ["Class", "Count"]

    abc_color = alt.Color(
        "Class:N",
        scale=alt.Scale(
            domain=["A", "B", "C"],
            range=["#ef4444", "#f59e0b", "#22c55e"]
        )
    )

    chart2 = (
        alt.Chart(abc_counts)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Class:N", axis=alt.Axis(labelAngle=0)),
            y="Count:Q",
            color=abc_color
        )
        .properties(height=220)
        .configure(**DARK_CHART["config"])
    )

    st.altair_chart(chart2, use_container_width=True)


# =========================================================
# FOOTER
# =========================================================
st.markdown("<div style='margin:24px 0 8px; border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#334155;text-align:center;padding:8px 0 16px;">
    Portfolio Project &nbsp;|&nbsp; Warehouse Slotting Optimization &nbsp;|&nbsp; Python · SQL · Streamlit
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <span style="color:#1e3a5f;">⚠ Simulated data — no proprietary information shared</span>
</div>
""", unsafe_allow_html=True)
