import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import altair as alt

st.set_page_config(
    page_title="DC Slotting Dashboard",
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
[data-testid="stSidebar"] { background-color: #111420 !important; border-right: 1px solid #1e2235 !important; }
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
.main .block-container { padding-top: 0rem !important; padding-left: 2rem !important; padding-right: 2rem !important; max-width: 100% !important; }
h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif !important; color: #f1f5f9 !important; }
[data-testid="stDataFrame"] { background: #111420 !important; }
[data-testid="stMetric"] { background: transparent !important; }
[data-testid="stSelectbox"] > div, [data-baseweb="select"] { background-color: #1a1f2e !important; border-color: #2d3450 !important; color: #e2e8f0 !important; }
div[data-baseweb="popover"] { background-color: #1a1f2e !important; }
[data-testid="stSlider"] > div > div > div > div { background: #00c9a7 !important; }
hr { border-color: #1e2235 !important; }
[data-testid="stCaptionContainer"] p { color: #64748b !important; }
[data-testid="stDownloadButton"] button { background: #1a1f2e !important; border: 1px solid #2d3450 !important; color: #94a3b8 !important; }
[data-testid="stDataFrame"] > div { background-color: #111420 !important; }
iframe { color-scheme: dark !important; }
.stDataFrame [data-testid="stDataFrameResizable"] { background: #111420 !important; }
[data-testid="stTextInput"] input { background-color: #1a1f2e !important; border-color: #2d3450 !important; color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER BAR
# =========================================================
st.markdown("""
<div style="background:linear-gradient(90deg,#0f1523 0%,#141929 100%);border-bottom:1px solid #1e2d4a;padding:14px 24px;margin:-1rem -2rem 1.5rem -2rem;display:flex;align-items:center;justify-content:space-between;min-width:0;overflow:hidden;">
    <div style="display:flex;align-items:center;flex-wrap:nowrap;white-space:nowrap;overflow:hidden;min-width:0;">
        <span style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;color:#00c9a7;letter-spacing:0.08em;text-transform:uppercase;flex-shrink:0;">DISTRIBUTION CENTER</span>
        <span style="color:#334155;margin:0 10px;flex-shrink:0;">|</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:#94a3b8;letter-spacing:0.05em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">WAREHOUSE RE-SLOTTING DASHBOARD</span>
        <span style="color:#334155;margin:0 10px;flex-shrink:0;">|</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#475569;flex-shrink:0;">· Demo</span>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#475569;flex-shrink:0;margin-left:16px;white-space:nowrap;">Q1 2026 &nbsp;|&nbsp; Simulated</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
df_original = pd.read_csv("data.csv")
lane_df = pd.read_csv("lane.csv")

# Normalize lane data — deduplicate to unique bins
lane_df = lane_df.drop_duplicates(subset=["lane", "storage_bin"])
lane_df["zone"] = lane_df["zone"].str.strip()
lane_df["occupied"] = lane_df["material"].notna() & (lane_df["material"].astype(str).str.strip() != "")

# Zone mapping
ZONE_DISPLAY = {"Priority": "Zone 1 Priority", "Standard": "Zone 2 Standard", "Reserve": "Zone 3 Reserve"}
ZONE_COLOR   = {"Zone 1 Priority": "#00c9a7",  "Zone 2 Standard": "#3b82f6",   "Zone 3 Reserve": "#f59e0b"}

lane_df["zone_display"] = lane_df["zone"].map(ZONE_DISPLAY).fillna(lane_df["zone"])

# Normalize SKU data
if "Current_Zone" in df_original.columns and "Zone" not in df_original.columns:
    df_original["Zone"] = df_original["Current_Zone"]
if "Recommended_Zone" not in df_original.columns:
    df_original["Recommended_Zone"] = df_original["Zone"]
if "Needs_Relocation" in df_original.columns:
    df_original["Needs_Relocation"] = df_original["Needs_Relocation"].astype(int).astype(bool)
else:
    df_original["Needs_Relocation"] = df_original["Current_Location"] != df_original["Optimal_Location"]

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:0.1em;color:#00c9a7;text-transform:uppercase;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #1e2235;">
&#9881; Dashboard Controls
</div>
""", unsafe_allow_html=True)

selected_class = st.sidebar.selectbox("ABC Class", ["All", "A", "B", "C"])
min_movements = st.sidebar.slider("Minimum Movements", 0, int(df_original["Movements"].max()), 0)

st.sidebar.markdown("---")

# Zone breakdown from real lane data
zone_stats = lane_df.groupby("zone_display").agg(
    total=("storage_bin", "count"),
    occupied=("occupied", "sum")
).reset_index()
zone_stats["free"] = zone_stats["total"] - zone_stats["occupied"]

zone_rows = ""
for _, row in zone_stats.iterrows():
    short = row["zone_display"].replace("Zone 1 ", "Z1 ").replace("Zone 2 ", "Z2 ").replace("Zone 3 ", "Z3 ")
    zone_rows += f"""
    <tr>
      <td style="color:#e2e8f0;">{short}</td>
      <td align="right" style="color:#52c41a;">{int(row['free'])}</td>
      <td align="right" style="color:#f59e0b;">{int(row['occupied'])}</td>
      <td align="right">{int(row['total'])}</td>
    </tr>"""

st.sidebar.markdown(f"""
<div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:10px;">Zone Breakdown</div>
<table style="width:100%;font-size:12px;border-collapse:collapse;color:#94a3b8;">
  <tr style="color:#475569;font-size:11px;"><td>LOCATION</td><td align="right">FREE</td><td align="right">OCC</td><td align="right">TOT</td></tr>
  {zone_rows}
</table>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"<div style='font-size:11px;color:#475569;font-family:IBM Plex Mono,monospace;'>ABC: {selected_class} &nbsp;|&nbsp; Min Moves: {min_movements}</div>",
    unsafe_allow_html=True
)

# =========================================================
# FILTER SKU DATA
# =========================================================
df = df_original.copy()
if selected_class != "All":
    df = df[df["ABC_Class"] == selected_class]
df = df[df["Movements"] >= min_movements].copy()
df["Needs_Relocation"] = df["Needs_Relocation"].astype(bool)
df["Time_Saved_Min"] = df["Needs_Relocation"].apply(lambda x: 10 if x else 0)
df["Labor_Impact"] = df["Time_Saved_Min"] * (25 / 60)

total_skus = len(df)
misaligned = int(df["Needs_Relocation"].sum())
misalignment_pct = round((misaligned / total_skus) * 100, 1) if total_skus else 0
estimated_time_saved = round(df["Time_Saved_Min"].sum() / 60, 1)
estimated_labor = round(df["Labor_Impact"].sum(), 0)

priority_df = df_original[(df_original["ABC_Class"] == "A") & (df_original["Movements"] > 100)].copy()
prime_misplaced = df[(df["ABC_Class"] == "A") & (df["Zone"] != "Prime") & (df["Needs_Relocation"])]
low_in_prime = df[(df["ABC_Class"] == "C") & (df["Zone"] == "Prime")]

# =========================================================
# KPI CARDS
# =========================================================
total_bins = len(lane_df)
occupied_bins = int(lane_df["occupied"].sum())
free_bins = total_bins - occupied_bins

cards_data = [
    ("Total SKUs",      f"{total_skus:,}",          "#e2e8f0", "active FG SKUs"),
    ("Relocation SKUs", f"{misaligned:,}",           "#f59e0b", "recommended to move"),
    ("Relocation %",    f"{misalignment_pct:.1f}%",  "#ef4444", "of analyzed SKUs"),
    ("Storage Bins",    f"{total_bins:,}",            "#ec4899", "facility locations"),
    ("Available Bins",  f"{free_bins:,}",             "#22c55e", "ready for putaway"),
    ("SAP Records",     "423K",                       "#3b82f6", "movement records"),
    ("Time Saved",      f"{estimated_time_saved:.1f} hrs/wk", "#14b8a6", "estimated gain"),
    ("Labor Impact",    f"${int(estimated_labor):,}/wk",       "#a78bfa", "@ $25/hr"),
]

card_items_html = ""
for label, value, color, sub in cards_data:
    card_items_html += f"""
    <div class="kpi-card" style="border-top:2px solid {color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

kpi_html = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');
body { margin:0; background:#0b0d14; }
.kpi-grid { display:grid; grid-template-columns:repeat(8,1fr); gap:12px; }
.kpi-card { background:#111420; border:1px solid #1e2235; border-radius:10px; padding:16px 18px; min-height:100px; }
.kpi-label { font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:0.08em; text-transform:uppercase; color:#64748b; margin-bottom:10px; }
.kpi-value { font-family:'IBM Plex Sans',sans-serif; font-size:26px; font-weight:700; line-height:1; }
.kpi-sub { font-size:10px; color:#64748b; margin-top:7px; }
</style>
<div class="kpi-grid">
""" + card_items_html + "</div>"

components.html(kpi_html, height=140, scrolling=False)

# =========================================================
# INSIGHT BANNERS
# =========================================================
b1, b2 = st.columns(2)
with b1:
    st.markdown(
        f"<div style='background:#0f2a1a;border-left:4px solid #00c9a7;border-radius:8px;padding:14px 18px;margin:6px 0;font-size:14px;color:#e2e8f0;'>"
        f"<span style='color:#00c9a7;font-weight:700;'>&#9889; Impact:</span> "
        f"Identified {misaligned} relocation opportunities across {total_skus} SKUs ({misalignment_pct}%).</div>",
        unsafe_allow_html=True
    )
with b2:
    st.markdown(
        "<div style='background:#1a1a0f;border-left:4px solid #f59e0b;border-radius:8px;padding:14px 18px;margin:6px 0;font-size:14px;color:#e2e8f0;'>"
        "<span style='color:#f59e0b;font-weight:700;'>&#127919; Key Finding:</span> "
        "A-class SKUs should be prioritized for Priority zones, while lower-priority inventory can be shifted to Standard or Reserve.</div>",
        unsafe_allow_html=True
    )

st.markdown("<div style='margin:12px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# SKU BIN RECOMMENDATION SEARCH
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;'>&#9906; SKU Bin Recommendation</div>"
    "<div style='font-size:13px;color:#475569;margin-bottom:12px;'>Enter a material number to find the best available bin based on ABC class and velocity</div>",
    unsafe_allow_html=True
)

def get_recommended_zone(abc_class, speed_class):
    abc = str(abc_class).strip().upper()
    speed = str(speed_class).strip().capitalize() if speed_class else "Slow"
    if abc == "A" and speed in ["Fast", "Medium"]:
        return "Priority"
    if abc == "A" and speed == "Slow":
        return "Priority"
    if abc == "B" and speed == "Fast":
        return "Priority"
    if abc == "B" and speed in ["Medium", "Slow"]:
        return "Standard"
    return "Reserve"

search_col, btn_col = st.columns([4, 1])
with search_col:
    sku_input = st.text_input("", placeholder="Enter material number (e.g. SKU_124 or 5000367649)", label_visibility="collapsed")
with btn_col:
    search_btn = st.button("Find Bin →", use_container_width=True)

if search_btn and sku_input.strip():
    query = sku_input.strip()
    sku_row = None
    if "SKU_ID" in df_original.columns:
        match = df_original[df_original["SKU_ID"].astype(str).str.contains(query, case=False, na=False)]
        if not match.empty:
            sku_row = match.iloc[0]
    if sku_row is None:
        st.markdown(
            f"<div style='background:#1a0f0f;border-left:4px solid #ef4444;border-radius:8px;padding:14px 18px;color:#e2e8f0;'>"
            f"&#9888; Material <strong>{query}</strong> not found in the dataset.</div>",
            unsafe_allow_html=True
        )
    else:
        abc = sku_row.get("ABC_Class", "C")
        speed = sku_row.get("Speed_Class", "Slow")
        rec_zone = get_recommended_zone(abc, speed)
        zone_display = ZONE_DISPLAY.get(rec_zone, rec_zone)
        zone_color = ZONE_COLOR.get(zone_display, "#94a3b8")

        # Find available bins in recommended zone
        available = lane_df[
            (lane_df["zone"] == rec_zone) &
            (~lane_df["occupied"])
        ].sort_values("lane_rank")

        if available.empty:
            fallback_zones = ["Priority", "Standard", "Reserve"]
            for fz in fallback_zones:
                available = lane_df[(lane_df["zone"] == fz) & (~lane_df["occupied"])].sort_values("lane_rank")
                if not available.empty:
                    rec_zone = fz
                    zone_display = ZONE_DISPLAY.get(fz, fz)
                    zone_color = ZONE_COLOR.get(zone_display, "#94a3b8")
                    break

        if not available.empty:
            top_bin = available.iloc[0]
            top_lane = top_bin["lane"]
            top_storage = top_bin["storage_bin"]
            alt_bins = available.head(5)[["lane", "storage_bin"]].values.tolist()
            alt_html = " &nbsp;·&nbsp; ".join([f"{b[0]}/{b[1]}" for b in alt_bins])

            st.markdown(
                f"<div style='background:#0a1a12;border:1px solid #1e3a2a;border-left:4px solid {zone_color};"
                f"border-radius:10px;padding:20px 24px;margin:8px 0;'>"
                f"<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#475569;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;'>Recommendation for {query}</div>"
                f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:16px;'>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>ABC CLASS</div><div style='font-size:22px;font-weight:700;color:#ef4444;'>{abc}</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>VELOCITY</div><div style='font-size:22px;font-weight:700;color:#f59e0b;'>{speed}</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>RECOMMENDED ZONE</div><div style='font-size:18px;font-weight:700;color:{zone_color};'>{zone_display}</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>BEST AVAILABLE BIN</div><div style='font-size:22px;font-weight:700;color:#e2e8f0;'>{top_storage}</div><div style='font-size:11px;color:#64748b;'>Lane {top_lane}</div></div>"
                f"</div>"
                f"<div style='font-size:12px;color:#475569;'>&#9656; Other available bins in zone: <span style='color:#94a3b8;'>{alt_html}</span></div>"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background:#1a1a0f;border-left:4px solid #f59e0b;border-radius:8px;padding:14px 18px;color:#e2e8f0;'>"
                f"&#9888; No available bins found in any zone. The warehouse may be at full capacity.</div>",
                unsafe_allow_html=True
            )

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# WAREHOUSE BIN MAP — built from real lane data
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;'>&#9638; Warehouse Bin Map</div>"
    "<div style='font-size:13px;color:#475569;margin-bottom:12px;'>Lane-level view across 38 lanes — Priority, Standard, and Reserve zones</div>",
    unsafe_allow_html=True
)

def get_bin_color_from_lane(row):
    if not row["occupied"]:
        return "#12211a"
    mat = str(row.get("material", "")).strip()
    # Try to find ABC class from df_original
    if "SKU_ID" in df_original.columns:
        match = df_original[df_original["SKU_ID"].astype(str) == mat]
        if not match.empty:
            abc = match.iloc[0].get("ABC_Class", "")
            return {"A": "#ef4444", "B": "#f59e0b", "C": "#22c55e"}.get(str(abc).upper(), "#3b82f6")
    return "#3b82f6"

def render_bin_map_from_lanes(lane_data):
    zones_order = ["Zone 1 Priority", "Zone 2 Standard", "Zone 3 Reserve"]
    inner = ""

    for zone in zones_order:
        zone_data = lane_data[lane_data["zone_display"] == zone]
        if zone_data.empty:
            continue
        zone_color = ZONE_COLOR.get(zone, "#94a3b8")
        inner += f'<div class="zone-header" style="color:{zone_color};">{zone}</div><div class="lanes-row">'

        for lane in zone_data["lane"].unique():
            lane_bins = zone_data[zone_data["lane"] == lane]
            bins_html = ""
            for _, row in lane_bins.iterrows():
                color = get_bin_color_from_lane(row)
                tooltip = f"Bin:{row['storage_bin']} Mat:{row.get('material','')} {row['zone']}"
                bins_html += f'<div class="bin" style="background:{color};" title="{tooltip}"></div>'
            inner += f'<div class="lane-block"><div class="lane-label">{lane}</div><div class="bin-grid">{bins_html}</div></div>'

        inner += "</div>"

    html = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');
body { margin:0; background:#0b0d14; font-family:'IBM Plex Mono',monospace; }
.zone-header { font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;margin:20px 0 10px 0;padding-bottom:6px;border-bottom:1px solid #1e2235; }
.lanes-row { display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px; }
.lane-block { background:#111420;border:1px solid #1e2235;border-radius:8px;padding:10px 10px 8px; }
.lane-label { font-size:10px;font-weight:600;letter-spacing:0.1em;color:#64748b;margin-bottom:7px;text-align:center; }
.bin-grid { display:grid;grid-template-columns:repeat(6,14px);gap:3px; }
.bin { width:14px;height:14px;border-radius:2px; }
.legend { display:flex;gap:18px;flex-wrap:wrap;margin-bottom:14px;font-size:11px;color:#64748b; }
.legend-item { display:flex;align-items:center;gap:6px; }
.legend-dot { width:12px;height:12px;border-radius:2px; }
</style>
<div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#ef4444;"></div>A-Class</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;"></div>B-Class</div>
  <div class="legend-item"><div class="legend-dot" style="background:#22c55e;"></div>C-Class</div>
  <div class="legend-item"><div class="legend-dot" style="background:#3b82f6;"></div>Occupied (unknown class)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#12211a;border:1px solid #1e3a2a;"></div>Available</div>
</div>
""" + inner + "</div>"
    return html

components.html(render_bin_map_from_lanes(lane_df), height=800, scrolling=True)

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# KEY INSIGHTS
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;'>&#9656; Key Optimization Insights</div>",
    unsafe_allow_html=True
)

i1, i2, i3 = st.columns(3)

def kpi_card(label, value, color, sub=None):
    sub_html = f"<div style='font-size:11px;color:#475569;margin-top:4px;'>{sub}</div>" if sub else ""
    return (
        f"<div style='background:#111420;border:1px solid #1e2235;border-top:2px solid {color};"
        f"border-radius:10px;padding:18px 20px;text-align:left;'>"
        f"<div style='font-size:11px;color:#475569;font-family:IBM Plex Mono,monospace;"
        f"letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px;'>{label}</div>"
        f"<div style='font-size:28px;font-weight:700;color:{color};line-height:1;'>{value}</div>"
        f"{sub_html}</div>"
    )

i1.markdown(kpi_card("A-Class Outside Priority", str(len(prime_misplaced)), "#ef4444", "SKUs to pull into Zone 1"), unsafe_allow_html=True)
i2.markdown(kpi_card("C-Class in Priority", str(len(low_in_prime)), "#f59e0b", "Priority space being used"), unsafe_allow_html=True)
i3.markdown(kpi_card("Total Relocation Needed", str(misaligned), "#00c9a7", f"{misalignment_pct}% of filtered SKUs"), unsafe_allow_html=True)

st.markdown("<div style='margin:12px 0;'></div>", unsafe_allow_html=True)

st.markdown(
    f"<div style='background:#0a1a12;border-left:4px solid #00c9a7;border-radius:8px;padding:14px 18px;font-size:14px;color:#e2e8f0;'>"
    f"<span style='color:#00c9a7;font-weight:700;'>&#9989; Recommended Action:</span> "
    f"Prioritize the {misaligned} relocation candidates first, especially A-class SKUs outside Priority zones.</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# TOP 10 PRIORITY MOVES
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;'>&#9656; Top 10 Priority Moves — Highest Impact</div>",
    unsafe_allow_html=True
)

top_moves = df[df["Needs_Relocation"]].sort_values(
    by=["ABC_Class", "Movements", "Stock_Qty"], ascending=[True, False, False]
).head(10)

display_cols = [c for c in ["SKU_ID","ABC_Class","Speed_Class","Zone","Recommended_Zone",
                              "Current_Location","Movements","Stock_Qty","Optimal_Location"]
                if c in top_moves.columns]
st.dataframe(top_moves[display_cols], use_container_width=True, hide_index=True)

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# A-CLASS CRITICAL SKUS
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#ef4444;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;'>&#9656; A-Class High-Movement SKUs — Critical Items</div>",
    unsafe_allow_html=True
)
priority_cols = [c for c in ["SKU_ID","ABC_Class","Speed_Class","Zone","Recommended_Zone",
                               "Current_Location","Movements","Stock_Qty","Needs_Relocation","Optimal_Location"]
                 if c in priority_df.columns]
st.dataframe(priority_df[priority_cols].sort_values(by="Movements", ascending=False),
             use_container_width=True, hide_index=True)
st.caption("These SKUs represent the highest operational impact and should be reviewed first for Priority-zone placement.")

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# BEFORE VS AFTER
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;'>&#9656; Before vs. After Optimization</div>",
    unsafe_allow_html=True
)
st.markdown(
    f"<table style='width:100%;border-collapse:collapse;font-family:IBM Plex Sans,sans-serif;font-size:14px;"
    f"background:#111420;border:1px solid #1e2235;border-radius:10px;overflow:hidden;'>"
    f"<thead><tr style='background:#0f1523;border-bottom:1px solid #1e2235;'>"
    f"<th style='padding:12px 16px;text-align:left;color:#475569;font-family:IBM Plex Mono,monospace;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;'>Scenario</th>"
    f"<th style='padding:12px 16px;text-align:right;color:#475569;font-family:IBM Plex Mono,monospace;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;'>Relocation Candidates</th>"
    f"<th style='padding:12px 16px;text-align:right;color:#475569;font-family:IBM Plex Mono,monospace;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;'>Picking Time Saved (hrs/wk)</th>"
    f"<th style='padding:12px 16px;text-align:right;color:#475569;font-family:IBM Plex Mono,monospace;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;'>Labor Impact ($/wk)</th>"
    f"</tr></thead><tbody>"
    f"<tr style='border-bottom:1px solid #1e2235;'>"
    f"<td style='padding:14px 16px;color:#94a3b8;'>Current State</td>"
    f"<td style='padding:14px 16px;text-align:right;color:#ef4444;font-weight:600;'>{misaligned}</td>"
    f"<td style='padding:14px 16px;text-align:right;color:#475569;'>0</td>"
    f"<td style='padding:14px 16px;text-align:right;color:#475569;'>$0</td>"
    f"</tr><tr>"
    f"<td style='padding:14px 16px;color:#e2e8f0;font-weight:600;'>After Optimization</td>"
    f"<td style='padding:14px 16px;text-align:right;color:#475569;'>0</td>"
    f"<td style='padding:14px 16px;text-align:right;color:#00c9a7;font-weight:600;'>{estimated_time_saved} hrs</td>"
    f"<td style='padding:14px 16px;text-align:right;color:#a78bfa;font-weight:600;'>${int(estimated_labor):,}</td>"
    f"</tr></tbody></table>",
    unsafe_allow_html=True
)

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# CHARTS
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;'>&#9656; Operational Patterns &amp; Optimization Opportunities</div>",
    unsafe_allow_html=True
)

DARK_CFG = {
    "background": "#111420",
    "view": {"fill": "#111420", "stroke": "transparent"},
    "axis": {"gridColor": "#1e2235", "domainColor": "#1e2235", "tickColor": "#1e2235",
             "labelColor": "#64748b", "titleColor": "#94a3b8"},
    "legend": {"labelColor": "#94a3b8", "titleColor": "#94a3b8"},
    "title": {"color": "#e2e8f0"},
}

c1, c2 = st.columns(2)

with c1:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>Zone Utilization (Current)</div>", unsafe_allow_html=True)
    zone_chart_data = lane_df.groupby("zone_display").agg(
        Occupied=("occupied", "sum"),
        Available=("occupied", lambda x: (~x).sum())
    ).reset_index().melt(id_vars="zone_display", var_name="Status", value_name="Count")
    chart1 = (
        alt.Chart(zone_chart_data)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("zone_display:N", axis=alt.Axis(labelAngle=-15), title="Zone"),
            y="Count:Q",
            color=alt.Color("Status:N", scale=alt.Scale(
                domain=["Occupied", "Available"],
                range=["#ef4444", "#22c55e"]
            ))
        )
        .properties(height=220)
        .configure(**DARK_CFG)
    )
    st.altair_chart(chart1, use_container_width=True)

with c2:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>ABC Class Mix (Optimization Opportunity)</div>", unsafe_allow_html=True)
    abc_counts = df["ABC_Class"].value_counts().reset_index()
    abc_counts.columns = ["Class", "Count"]
    chart2 = (
        alt.Chart(abc_counts)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Class:N", axis=alt.Axis(labelAngle=0)),
            y="Count:Q",
            color=alt.Color("Class:N", scale=alt.Scale(
                domain=["A", "B", "C"],
                range=["#ef4444", "#f59e0b", "#22c55e"]
            ))
        )
        .properties(height=220)
        .configure(**DARK_CFG)
    )
    st.altair_chart(chart2, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("<div style='margin:24px 0 8px;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#334155;text-align:center;padding:8px 0 16px;'>"
    "Portfolio Project &nbsp;|&nbsp; Warehouse Slotting Optimization &nbsp;|&nbsp; Python &middot; SQL &middot; Streamlit"
    " &nbsp;&nbsp;&middot;&nbsp;&nbsp; "
    "<span style='color:#1e3a5f;'>&#9888; Simulated data &mdash; no proprietary information shared</span>"
    "</div>",
    unsafe_allow_html=True
)
