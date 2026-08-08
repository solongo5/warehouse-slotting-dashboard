import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import altair as alt

st.set_page_config(
    page_title="DC Slotting Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background-color:#0b0d14!important;color:#e2e8f0!important;font-family:'IBM Plex Sans',sans-serif!important;}
[data-testid="stSidebar"]{background-color:#111420!important;border-right:1px solid #1e2235!important;}
[data-testid="stSidebar"] *{color:#cbd5e1!important;}
.main .block-container{padding-top:0rem!important;padding-left:2rem!important;padding-right:2rem!important;max-width:100%!important;}
h1,h2,h3{font-family:'IBM Plex Sans',sans-serif!important;color:#f1f5f9!important;}
[data-testid="stDataFrame"]{background:#111420!important;}
[data-testid="stMetric"]{background:transparent!important;}
[data-testid="stSelectbox"]>div,[data-baseweb="select"]{background-color:#1a1f2e!important;border-color:#2d3450!important;color:#e2e8f0!important;}
div[data-baseweb="popover"]{background-color:#1a1f2e!important;}
[data-testid="stSlider"]>div>div>div>div{background:#00c9a7!important;}
hr{border-color:#1e2235!important;}
[data-testid="stCaptionContainer"] p{color:#64748b!important;}
[data-testid="stDataFrame"]>div{background-color:#111420!important;}
iframe{color-scheme:dark!important;}
[data-testid="stTextInput"] input{background-color:#1a1f2e!important;border-color:#2d3450!important;color:#e2e8f0!important;}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div style="background:linear-gradient(90deg,#0f1523 0%,#141929 100%);border-bottom:1px solid #1e2d4a;padding:14px 24px;margin:-1rem -2rem 1.5rem -2rem;display:flex;align-items:center;justify-content:space-between;min-width:0;overflow:hidden;">
    <div style="display:flex;align-items:center;flex-wrap:nowrap;white-space:nowrap;overflow:hidden;min-width:0;">
        <span style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;color:#00c9a7;letter-spacing:0.08em;text-transform:uppercase;flex-shrink:0;">DISTRIBUTION CENTER</span>
        <span style="color:#334155;margin:0 10px;flex-shrink:0;">|</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:13px;color:#94a3b8;letter-spacing:0.05em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">WAREHOUSE RE-SLOTTING ENGINE</span>
        <span style="color:#334155;margin:0 10px;flex-shrink:0;">|</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#475569;flex-shrink:0;">· Demo</span>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#475569;flex-shrink:0;margin-left:16px;white-space:nowrap;">Q1 2026 &nbsp;|&nbsp; Simulated</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# CONSTANTS
# =========================================================
# A=green, B=amber, C=red (per user request)
ABC_COLOR   = {"A": "#22c55e", "B": "#f59e0b", "C": "#ef4444"}
ZONE_DISPLAY = {
    "Priority": "Zone 1 Priority",
    "Standard": "Zone 2 Standard",
    "Reserve":  "Zone 3 Reserve"
}
ZONE_COLOR = {
    "Zone 1 Priority": "#00c9a7",
    "Zone 2 Standard": "#3b82f6",
    "Zone 3 Reserve":  "#f59e0b"
}

# =========================================================
# LOAD DATA — lane.csv is the single source of truth
# =========================================================
lane_df = pd.read_csv("lane.csv")
lane_df["zone"]        = lane_df["zone"].str.strip()
lane_df["material"]    = lane_df["material"].fillna("").astype(str).str.strip()
lane_df["abc_class"]   = lane_df["abc_class"].fillna("").astype(str).str.strip()
lane_df["speed_class"] = lane_df["speed_class"].fillna("").astype(str).str.strip()
lane_df["occupied"]    = lane_df["occupied"].astype(bool)
lane_df["zone_display"] = lane_df["zone"].map(ZONE_DISPLAY).fillna(lane_df["zone"])

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;letter-spacing:0.1em;"
    "color:#00c9a7;text-transform:uppercase;margin-bottom:16px;padding-bottom:8px;"
    "border-bottom:1px solid #1e2235;'>&#9881; Engine Controls</div>",
    unsafe_allow_html=True
)

selected_class = st.sidebar.selectbox("ABC Class", ["All", "A", "B", "C"])
selected_zone  = st.sidebar.selectbox("Zone", ["All", "Zone 1 Priority", "Zone 2 Standard", "Zone 3 Reserve"])
selected_speed = st.sidebar.selectbox("Speed Class", ["All", "Fast", "Medium", "Slow"])

st.sidebar.markdown("---")

# Zone breakdown from real data
st.sidebar.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;"
    "letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;'>Zone Breakdown</div>",
    unsafe_allow_html=True
)

zone_order = ["Zone 1 Priority", "Zone 2 Standard", "Zone 3 Reserve"]
hdr = st.sidebar.columns([3, 1, 1, 1])
for col, label in zip(hdr, ["LOCATION", "FREE", "OCC", "TOT"]):
    col.markdown(f"<span style='font-size:10px;color:#475569;'>{label}</span>", unsafe_allow_html=True)

zone_stats = lane_df.groupby("zone_display").agg(
    total=("storage_bin","count"),
    occupied=("occupied","sum")
).reset_index()
zone_stats["free"] = zone_stats["total"] - zone_stats["occupied"]
zone_stats["_sort"] = zone_stats["zone_display"].map({z: i for i, z in enumerate(zone_order)})
zone_stats = zone_stats.sort_values("_sort")

for _, row in zone_stats.iterrows():
    short = row["zone_display"].replace("Zone 1 ","Z1 ").replace("Zone 2 ","Z2 ").replace("Zone 3 ","Z3 ")
    rc = st.sidebar.columns([3, 1, 1, 1])
    rc[0].markdown(f"<span style='font-size:12px;color:#e2e8f0;'>{short}</span>", unsafe_allow_html=True)
    rc[1].markdown(f"<span style='font-size:12px;color:#22c55e;'>{int(row['free'])}</span>", unsafe_allow_html=True)
    rc[2].markdown(f"<span style='font-size:12px;color:#f59e0b;'>{int(row['occupied'])}</span>", unsafe_allow_html=True)
    rc[3].markdown(f"<span style='font-size:12px;color:#94a3b8;'>{int(row['total'])}</span>", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Misplacement insight in sidebar
misplaced_bins = lane_df[
    lane_df["occupied"] & (
        ((lane_df["abc_class"] == "A") & (lane_df["zone"] != "Priority")) |
        ((lane_df["abc_class"] == "C") & (lane_df["zone"] == "Priority"))
    )
]
total_occupied = lane_df["occupied"].sum()
mis_pct = round(len(misplaced_bins) / total_occupied * 100, 1) if total_occupied else 0

st.sidebar.markdown(
    f"<div style='font-size:11px;color:#475569;font-family:IBM Plex Mono,monospace;margin-bottom:6px;'>"
    f"Misplaced bins: <span style='color:#ef4444;font-weight:700;'>{len(misplaced_bins)}</span> "
    f"<span style='color:#475569;'>({mis_pct}% of occupied)</span></div>",
    unsafe_allow_html=True
)

# =========================================================
# FILTER lane_df for map
# =========================================================
map_df = lane_df.copy()
if selected_class != "All":
    map_df = map_df[(map_df["abc_class"] == selected_class) | (~map_df["occupied"])]
if selected_zone != "All":
    map_df = map_df[map_df["zone_display"] == selected_zone]
if selected_speed != "All":
    map_df = map_df[(map_df["speed_class"] == selected_speed) | (~map_df["occupied"])]

# =========================================================
# KPI METRICS
# =========================================================
total_bins   = len(lane_df)
occupied_cnt = int(lane_df["occupied"].sum())
free_cnt     = total_bins - occupied_cnt
occ_pct      = round(occupied_cnt / total_bins * 100, 1)

a_outside_priority = int(((lane_df["abc_class"]=="A") & (lane_df["zone"]!="Priority") & lane_df["occupied"]).sum())
c_in_priority      = int(((lane_df["abc_class"]=="C") & (lane_df["zone"]=="Priority") & lane_df["occupied"]).sum())
total_misplaced    = a_outside_priority + c_in_priority
mis_pct_kpi        = round(total_misplaced / occupied_cnt * 100, 1) if occupied_cnt else 0

cards_data = [
    ("Total Bins",        f"{total_bins:,}",    "#e2e8f0", "storage locations"),
    ("Occupied",          f"{occupied_cnt:,}",  "#f59e0b", f"{occ_pct}% utilization"),
    ("Available",         f"{free_cnt:,}",      "#22c55e", "ready for putaway"),
    ("Misplaced Bins",    f"{total_misplaced:,}","#ef4444", f"{mis_pct_kpi}% of occupied"),
    ("A Outside Priority",f"{a_outside_priority:,}","#ef4444","high-value misplaced"),
    ("C in Priority",     f"{c_in_priority:,}", "#f59e0b", "low-value in prime zone"),
    ("Priority Lanes",    "15",                 "#00c9a7", "closest to dock"),
    ("Reserve Lanes",     "10",                 "#3b82f6", "furthest from dock"),
]

card_items_html = "".join([
    f'<div class="kpi-card" style="border-top:2px solid {c};">'
    f'<div class="kpi-label">{l}</div>'
    f'<div class="kpi-value" style="color:{c};">{v}</div>'
    f'<div class="kpi-sub">{s}</div></div>'
    for l, v, c, s in cards_data
])

components.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');
body{{margin:0;background:#0b0d14;}}
.kpi-grid{{display:grid;grid-template-columns:repeat(8,1fr);gap:12px;}}
.kpi-card{{background:#111420;border:1px solid #1e2235;border-radius:10px;padding:16px 18px;min-height:100px;}}
.kpi-label{{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:0.08em;text-transform:uppercase;color:#64748b;margin-bottom:10px;}}
.kpi-value{{font-family:'IBM Plex Sans',sans-serif;font-size:26px;font-weight:700;line-height:1;}}
.kpi-sub{{font-size:10px;color:#64748b;margin-top:7px;}}
</style>
<div class="kpi-grid">{card_items_html}</div>
""", height=140, scrolling=False)

# =========================================================
# INSIGHT BANNERS
# =========================================================
b1, b2 = st.columns(2)
with b1:
    st.markdown(
        f"<div style='background:#0f2a1a;border-left:4px solid #00c9a7;border-radius:8px;"
        f"padding:14px 18px;margin:6px 0;font-size:14px;color:#e2e8f0;'>"
        f"<span style='color:#00c9a7;font-weight:700;'>&#9889; Impact:</span> "
        f"{total_misplaced} bins are misplaced ({mis_pct_kpi}% of occupied) — "
        f"{a_outside_priority} high-value SKUs outside Priority zones and "
        f"{c_in_priority} low-priority SKUs occupying prime space.</div>",
        unsafe_allow_html=True
    )
with b2:
    st.markdown(
        "<div style='background:#1a1a0f;border-left:4px solid #f59e0b;border-radius:8px;"
        "padding:14px 18px;margin:6px 0;font-size:14px;color:#e2e8f0;'>"
        "<span style='color:#f59e0b;font-weight:700;'>&#127919; Slotting Logic:</span> "
        "A-class (green) → Zone 1 Priority &nbsp;|&nbsp; "
        "B-class (amber) → Zone 2 Standard &nbsp;|&nbsp; "
        "C-class (red) → Zone 3 Reserve</div>",
        unsafe_allow_html=True
    )

st.markdown("<div style='margin:12px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# SKU BIN RECOMMENDATION
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;"
    "letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;'>&#9906; SKU Bin Recommendation</div>"
    "<div style='font-size:13px;color:#475569;margin-bottom:12px;'>"
    "Enter a SKU ID to find the best available bin based on ABC class and movement velocity</div>",
    unsafe_allow_html=True
)

def get_recommended_zone(abc, speed):
    abc = str(abc).strip().upper()
    speed = str(speed).strip().capitalize()
    if abc == "A":
        return "Priority"
    if abc == "B" and speed == "Fast":
        return "Priority"
    if abc == "B":
        return "Standard"
    return "Reserve"

sc, bc = st.columns([4, 1])
with sc:
    sku_input = st.text_input("", placeholder="e.g. SKU_53 or SKU_124", label_visibility="collapsed")
with bc:
    search_btn = st.button("Find Bin →", use_container_width=True)

if search_btn and sku_input.strip():
    query = sku_input.strip()
    sku_row = lane_df[lane_df["material"].str.upper() == query.upper()]

    if sku_row.empty:
        st.markdown(
            f"<div style='background:#1a0f0f;border-left:4px solid #ef4444;border-radius:8px;"
            f"padding:14px 18px;color:#e2e8f0;'>&#9888; SKU <b>{query}</b> not found. "
            f"Try SKU_1 through SKU_153.</div>",
            unsafe_allow_html=True
        )
    else:
        found = sku_row.iloc[0]
        abc   = found["abc_class"]
        speed = found["speed_class"]
        current_zone = found["zone"]
        current_bin  = found["storage_bin"]
        current_lane = found["lane"]
        rec_zone = get_recommended_zone(abc, speed)
        zone_display = ZONE_DISPLAY.get(rec_zone, rec_zone)
        zone_color   = ZONE_COLOR.get(zone_display, "#94a3b8")
        abc_color    = ABC_COLOR.get(abc, "#94a3b8")
        is_misplaced = current_zone != rec_zone

        # Find best available bin
        available = lane_df[(lane_df["zone"] == rec_zone) & (~lane_df["occupied"])].sort_values("lane_rank")
        if available.empty:
            for fz in ["Priority", "Standard", "Reserve"]:
                available = lane_df[(lane_df["zone"] == fz) & (~lane_df["occupied"])].sort_values("lane_rank")
                if not available.empty:
                    rec_zone = fz
                    zone_display = ZONE_DISPLAY.get(fz, fz)
                    zone_color = ZONE_COLOR.get(zone_display, "#94a3b8")
                    break

        misplaced_badge = (
            f"<span style='background:#3a0f0f;color:#ef4444;font-size:11px;padding:3px 8px;"
            f"border-radius:4px;margin-left:8px;'>&#9888; MISPLACED</span>"
            if is_misplaced else
            f"<span style='background:#0f2a1a;color:#22c55e;font-size:11px;padding:3px 8px;"
            f"border-radius:4px;margin-left:8px;'>&#10003; CORRECTLY PLACED</span>"
        )

        if not available.empty:
            top = available.iloc[0]
            alt_bins = " &nbsp;·&nbsp; ".join(
                [f"{r['lane']}/{r['storage_bin']}" for _, r in available.head(5).iterrows()]
            )
            st.markdown(
                f"<div style='background:#0a1a12;border:1px solid #1e3a2a;border-left:4px solid {zone_color};"
                f"border-radius:10px;padding:20px 24px;margin:8px 0;'>"
                f"<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#475569;"
                f"letter-spacing:0.1em;text-transform:uppercase;margin-bottom:14px;'>"
                f"Recommendation for {query} {misplaced_badge}</div>"
                f"<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-bottom:16px;'>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>ABC CLASS</div>"
                f"<div style='font-size:22px;font-weight:700;color:{abc_color};'>{abc}</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>SPEED</div>"
                f"<div style='font-size:22px;font-weight:700;color:#94a3b8;'>{speed}</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>CURRENT LOCATION</div>"
                f"<div style='font-size:16px;font-weight:700;color:#94a3b8;'>{current_bin}</div>"
                f"<div style='font-size:11px;color:#64748b;'>Lane {current_lane} ({current_zone})</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>OPTIMAL ZONE</div>"
                f"<div style='font-size:16px;font-weight:700;color:{zone_color};'>{zone_display}</div></div>"
                f"<div><div style='font-size:11px;color:#475569;margin-bottom:4px;'>RECOMMENDED BIN</div>"
                f"<div style='font-size:22px;font-weight:700;color:#e2e8f0;'>{top['storage_bin']}</div>"
                f"<div style='font-size:11px;color:#64748b;'>Lane {top['lane']}</div></div>"
                f"</div>"
                f"<div style='font-size:12px;color:#475569;'>&#9656; Other available bins: "
                f"<span style='color:#94a3b8;'>{alt_bins}</span></div></div>",
                unsafe_allow_html=True
            )

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# WAREHOUSE BIN MAP
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;"
    "letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;'>&#9638; Warehouse Bin Map</div>"
    "<div style='font-size:13px;color:#475569;margin-bottom:12px;'>"
    "38 lanes · 1,934 bins · green=A-class · amber=B-class · red=C-class · dark=available</div>",
    unsafe_allow_html=True
)

def render_bin_map(data):
    inner = ""
    for zone in zone_order:
        zdf = data[data["zone_display"] == zone]
        if zdf.empty:
            continue
        zcolor = ZONE_COLOR.get(zone, "#94a3b8")
        inner += f'<div class="zone-header" style="color:{zcolor};">{zone}</div><div class="lanes-row">'
        for lane in sorted(zdf["lane"].unique(), key=lambda x: zdf[zdf["lane"]==x]["lane_rank"].iloc[0]):
            ldf = zdf[zdf["lane"] == lane]
            bins_html = ""
            for _, row in ldf.iterrows():
                if not row["occupied"]:
                    color = "#12211a"
                    border = "border:1px solid #1e3a2a;"
                else:
                    color = ABC_COLOR.get(str(row["abc_class"]).upper(), "#3b82f6")
                    border = ""
                abc_txt   = row["abc_class"] if row["occupied"] else "Empty"
                speed_txt = row["speed_class"] if row["occupied"] else ""
                tooltip   = f"Bin:{row['storage_bin']} SKU:{row['material']} ABC:{abc_txt} Speed:{speed_txt} Zone:{row['zone']}"
                bins_html += f'<div class="bin" style="background:{color};{border}" title="{tooltip}"></div>'
            inner += (
                f'<div class="lane-block">'
                f'<div class="lane-label">{lane}</div>'
                f'<div class="bin-grid">{bins_html}</div>'
                f'</div>'
            )
        inner += "</div>"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');
body{{margin:0;background:#0b0d14;font-family:'IBM Plex Mono',monospace;}}
.zone-header{{font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;
  margin:20px 0 10px 0;padding-bottom:6px;border-bottom:1px solid #1e2235;}}
.lanes-row{{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px;}}
.lane-block{{background:#111420;border:1px solid #1e2235;border-radius:8px;padding:10px 10px 8px;}}
.lane-label{{font-size:10px;font-weight:600;letter-spacing:0.1em;color:#64748b;margin-bottom:7px;text-align:center;}}
.bin-grid{{display:grid;grid-template-columns:repeat(6,14px);gap:3px;}}
.bin{{width:14px;height:14px;border-radius:2px;cursor:pointer;}}
.legend{{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:14px;font-size:11px;color:#64748b;}}
.legend-item{{display:flex;align-items:center;gap:6px;}}
.legend-dot{{width:12px;height:12px;border-radius:2px;}}
</style>
<div>
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#22c55e;"></div>A-Class (High Value)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;"></div>B-Class (Medium Value)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#ef4444;"></div>C-Class (Low Value)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#12211a;border:1px solid #1e3a2a;"></div>Available</div>
</div>
{inner}
</div>"""

components.html(render_bin_map(map_df), height=1000, scrolling=True)

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# MISPLACEMENT TABLE
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#ef4444;"
    "letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;'>"
    "&#9656; Misplaced SKUs — Relocation Candidates</div>",
    unsafe_allow_html=True
)

misplaced_df = lane_df[
    lane_df["occupied"] & (
        ((lane_df["abc_class"] == "A") & (lane_df["zone"] != "Priority")) |
        ((lane_df["abc_class"] == "C") & (lane_df["zone"] == "Priority"))
    )
].copy()

misplaced_df["Recommended Zone"] = misplaced_df.apply(
    lambda r: get_recommended_zone(r["abc_class"], r["speed_class"]), axis=1
)

show_cols = ["material","lane","storage_bin","zone","abc_class","speed_class","soh_pallets","pallets_space","Recommended Zone"]
show_cols = [c for c in show_cols if c in misplaced_df.columns]

rename_map = {
    "material": "SKU",
    "lane": "Lane",
    "storage_bin": "Current Bin",
    "zone": "Current Zone",
    "abc_class": "ABC",
    "speed_class": "Speed",
    "soh_pallets": "SOH Pallets",
    "pallets_space": "Capacity"
}

st.dataframe(
    misplaced_df[show_cols].rename(columns=rename_map).sort_values("ABC"),
    use_container_width=True,
    hide_index=True
)
st.caption(f"{len(misplaced_df)} bins identified as misplaced — A-class outside Priority zones or C-class occupying Priority space.")

st.markdown("<div style='margin:16px 0;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)

# =========================================================
# CHARTS
# =========================================================
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#00c9a7;"
    "letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;'>"
    "&#9656; Operational Patterns &amp; Optimization Opportunities</div>",
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

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>Zone Utilization</div>", unsafe_allow_html=True)
    zone_chart = lane_df.groupby("zone_display").agg(
        Occupied=("occupied","sum"),
        Available=("occupied", lambda x: (~x).sum())
    ).reset_index().melt(id_vars="zone_display", var_name="Status", value_name="Count")
    chart1 = (
        alt.Chart(zone_chart)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("zone_display:N", axis=alt.Axis(labelAngle=-20), title="Zone"),
            y="Count:Q",
            color=alt.Color("Status:N", scale=alt.Scale(
                domain=["Occupied","Available"], range=["#f59e0b","#22c55e"]
            ))
        ).properties(height=220).configure(**DARK_CFG)
    )
    st.altair_chart(chart1, use_container_width=True)

with c2:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>ABC Class by Zone</div>", unsafe_allow_html=True)
    abc_zone = lane_df[lane_df["occupied"]].groupby(["zone_display","abc_class"]).size().reset_index(name="Count")
    chart2 = (
        alt.Chart(abc_zone)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("zone_display:N", axis=alt.Axis(labelAngle=-20), title="Zone"),
            y="Count:Q",
            color=alt.Color("abc_class:N", scale=alt.Scale(
                domain=["A","B","C"], range=["#22c55e","#f59e0b","#ef4444"]
            ))
        ).properties(height=220).configure(**DARK_CFG)
    )
    st.altair_chart(chart2, use_container_width=True)

with c3:
    st.markdown("<div style='font-size:13px;font-weight:600;color:#94a3b8;margin-bottom:8px;'>Speed Class Distribution</div>", unsafe_allow_html=True)
    speed_chart = lane_df[lane_df["occupied"]].groupby("speed_class").size().reset_index(name="Count")
    chart3 = (
        alt.Chart(speed_chart)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("speed_class:N", axis=alt.Axis(labelAngle=0), title="Speed Class"),
            y="Count:Q",
            color=alt.Color("speed_class:N", scale=alt.Scale(
                domain=["Fast","Medium","Slow"], range=["#00c9a7","#3b82f6","#475569"]
            ))
        ).properties(height=220).configure(**DARK_CFG)
    )
    st.altair_chart(chart3, use_container_width=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("<div style='margin:24px 0 8px;border-bottom:1px solid #1e2235;'></div>", unsafe_allow_html=True)
st.markdown(
    "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:#334155;"
    "text-align:center;padding:8px 0 16px;'>"
    "Portfolio Project &nbsp;|&nbsp; Warehouse Slotting Optimization &nbsp;|&nbsp; Python &middot; SQL &middot; Streamlit"
    " &nbsp;&nbsp;&middot;&nbsp;&nbsp; "
    "<span style='color:#1e3a5f;'>&#9888; Simulated data &mdash; no proprietary information shared</span>"
    "</div>",
    unsafe_allow_html=True
)
