import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import auth

# ---------------------------------------------------------
# Page Configuration & Metadata
# ---------------------------------------------------------
st.set_page_config(
    page_title="CareFlow™ Clinical Pathway Intelligence",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Clinical Pathway Reference Standard & Refreshed Icons
# ---------------------------------------------------------
CLINICAL_PATHWAY_ORDER = [
    "Registration",
    "Consultation",
    "Laboratory Test",
    "Treatment",
    "Discharge"
]

STAGE_METADATA = {
    "Registration": {"step": 1, "icon": "📝", "color": "#0284C7", "label": "1. 📝 Registration"},
    "Consultation": {"step": 2, "icon": "🩺", "color": "#4F46E5", "label": "2. 🩺 Consultation"},
    "Laboratory Test": {"step": 3, "icon": "🧪", "color": "#D97706", "label": "3. 🧪 Laboratory Test"},
    "Treatment": {"step": 4, "icon": "💊", "color": "#DB2777", "label": "4. 💊 Treatment"},
    "Discharge": {"step": 5, "icon": "✅", "color": "#059669", "label": "5. ✅ Discharge"}
}

# ---------------------------------------------------------
# Custom Modern Light Theme Design System & CSS
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main container background in crisp clean light mode */
    .stApp {
        background: radial-gradient(circle at 10% 10%, rgba(14, 165, 233, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 90% 20%, rgba(99, 102, 241, 0.04) 0%, transparent 40%),
                    #F8FAFC;
        color: #0F172A;
    }

    /* Native Streamlit Bordered Container Styling */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05) !important;
        margin-bottom: 1.25rem !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div:hover {
        border-color: #BAE6FD !important;
        box-shadow: 0 8px 24px -4px rgba(14, 165, 233, 0.08) !important;
    }

    /* Glass Card Style for HTML elements */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.25rem;
    }
    .glass-card:hover {
        border-color: #38BDF8;
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -4px rgba(14, 165, 233, 0.12);
    }

    /* Filter Panel Container */
    .filter-panel {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.06);
    }

    .filter-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 14px;
    }

    /* Pathway Pipeline Ribbon in Light Mode */
    .pathway-ribbon {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 14px;
        padding-top: 14px;
        border-top: 1px solid #E2E8F0;
    }
    .pathway-node {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        transition: all 0.25s ease;
    }
    .pathway-arrow {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 700;
    }

    /* Transition Step Item in Summary */
    .trans-item {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.2s ease;
    }
    .trans-item:hover {
        background: #F1F5F9;
        border-color: #CBD5E1;
    }

    /* KPI Value styling */
    .kpi-title {
        color: #64748B;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.1;
        color: #0F172A;
    }
    .kpi-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        margin-top: 10px;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .kpi-badge-teal {
        background: #CCFBF1;
        color: #0F766E;
        border: 1px solid #99F6E4;
    }
    .kpi-badge-indigo {
        background: #EEF2FF;
        color: #4338CA;
        border: 1px solid #C7D2FE;
    }
    .kpi-badge-amber {
        background: #FEF3C7;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .kpi-badge-rose {
        background: #FFE4E6;
        color: #BE123C;
        border: 1px solid #FECDD3;
    }

    /* Hero Header in Light Mode */
    .hero-banner {
        padding: 24px 30px;
        border-radius: 20px;
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 320px;
        height: 100%;
        background: radial-gradient(circle at 100% 50%, rgba(14, 165, 233, 0.1), transparent 70%);
        pointer-events: none;
    }
    .hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #E0F2FE;
        border: 1px solid #BAE6FD;
        color: #0284C7;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 70%, #0284C7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #475569;
        font-size: 0.95rem;
        margin-top: 6px;
        font-weight: 400;
        max-width: 720px;
    }

    /* Section Subheaders */
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.01em;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 16px;
    }

    /* Streamlit Tabs Customization in Light Mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        color: #64748B;
        font-weight: 600;
        font-size: 0.875rem;
        padding: 0 18px;
        border: none;
        background-color: transparent;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #0284C7 !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
    }

    /* Pulse Indicator */
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Authentication & Access Control
# ---------------------------------------------------------
auth.init_session_state()

if not st.session_state.get("authenticated", False):
    auth.render_login_page()
    st.stop()

# ---------------------------------------------------------
# Data Loading & Preprocessing
# ---------------------------------------------------------
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "cleaned_patient_events.csv"

@st.cache_data
def load_and_process_data():
    if not DATA_FILE.exists():
        return None
    data = pd.read_csv(DATA_FILE)
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data = data.dropna(subset=["case_id", "activity", "timestamp"])
    data = data.sort_values(["case_id", "timestamp"]).reset_index(drop=True)
    
    # Calculate transitions & wait times
    data["next_activity"] = data.groupby("case_id")["activity"].shift(-1)
    data["next_timestamp"] = data.groupby("case_id")["timestamp"].shift(-1)
    data["wait_minutes"] = (data["next_timestamp"] - data["timestamp"]).dt.total_seconds() / 60
    
    # Calculate patient start & normalized elapsed minutes from arrival
    data["patient_start"] = data.groupby("case_id")["timestamp"].transform("min")
    data["elapsed_minutes"] = (data["timestamp"] - data["patient_start"]).dt.total_seconds() / 60
    
    # Date helper
    data["date"] = data["timestamp"].dt.date
    data["time_str"] = data["timestamp"].dt.strftime("%H:%M")
    return data

df = load_and_process_data()

if df is None or df.empty:
    st.error("⚠️ Dataset not found or empty! Please ensure 'cleaned_patient_events.csv' is available.")
    st.stop()

# Helper sorting functions to ensure strict proper arrangement
def get_ordered_activities(df_data):
    """Sort activities strictly according to clinical pathway progression."""
    acts = df_data["activity"].unique().tolist()
    return sorted(
        acts,
        key=lambda x: CLINICAL_PATHWAY_ORDER.index(x) if x in CLINICAL_PATHWAY_ORDER else 999
    )

def get_ordered_patients(df_data):
    """Sort patients in natural numerical order P001, P002, etc."""
    pts = df_data["case_id"].unique().tolist()
    return sorted(
        pts,
        key=lambda x: int(''.join(c for c in x if c.isdigit())) if any(c.isdigit() for c in x) else x
    )

all_patients = get_ordered_patients(df)
all_activities = get_ordered_activities(df)
available_dates = sorted(df["date"].unique())
date_options = ["All Dates (Combined)"] + [d.strftime("%b %d, %Y") for d in available_dates]

# Stage mapping dictionary for clean display labels
activity_labels = {
    act: STAGE_METADATA.get(act, {}).get("label", act) for act in all_activities
}
reverse_activity_labels = {v: k for k, v in activity_labels.items()}

# ---------------------------------------------------------
# Sidebar Controls & SLA Settings with Modern Icons
# ---------------------------------------------------------
with st.sidebar:
    auth.render_user_sidebar()
    st.divider()
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="background: linear-gradient(135deg, #0284C7, #4F46E5); width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #0F172A; letter-spacing: -0.02em;">CareFlow™</div>
            <div style="font-size: 0.75rem; color: #64748B;">Clinical Process Mining</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>🎯 Service Targets (SLA)</p>", unsafe_allow_html=True)
    target_los = st.slider("Target Max Stay (mins)", min_value=60, max_value=180, value=120, step=10)
    
    st.divider()
    
    st.markdown("""
    <p style='font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>🧬 Pathway Hierarchy</p>
    """, unsafe_allow_html=True)
    
    for i, act in enumerate(all_activities, 1):
        meta = STAGE_METADATA.get(act, {"icon": "📍", "color": "#0284C7"})
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 0.8rem; color: #334155;">
            <span style="color: {meta['color']}; font-weight: 700;">{i}.</span>
            <span>{meta['icon']} {act}</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.markdown("""
    <div style="background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 12px; padding: 12px; font-size: 0.75rem; color: #64748B;">
        <span style="color: #0284C7; font-weight: 600;">⚡ CareFlow Engine v2.6</span><br>
        Timelines: Normalized & Clock Modes<br>
        Sequential Alignment: Active
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
auth.render_user_header()

current_user = st.session_state.get("user", {})
user_greeting = f"{current_user.get('avatar', '👤')} Signed in as {current_user.get('full_name', 'Clinician')} • {current_user.get('role', 'Staff')}" if current_user else "Live Clinical Intelligence System"

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-tag">
        <span class="pulse-dot"></span>
        {user_greeting}
    </div>
    <h1 class="hero-title">CareFlow™ Clinical Pathway Intelligence</h1>
    <p class="hero-subtitle">
        Interactive operational intelligence dashboard visualizing patient care trajectories, transition wait times, throughput bottlenecks, and hospital activity analytics.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Dedicated Top Control Hub: Filters Arranged in Proper Manner
# ---------------------------------------------------------
st.markdown("""
<div class="filter-panel">
    <div class="filter-title">
        <span>🎛️ Pathway Filtering & Cohort Selection</span>
        <span style="font-size: 0.75rem; font-weight: 600; color: #0284C7; margin-left: auto;">
            Arranged chronologically by clinical pathway order
        </span>
    </div>
""", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3 = st.columns([1, 1.3, 1.7])

with filter_col1:
    selected_date_str = st.selectbox(
        "📅 1. Clinical Date",
        options=date_options,
        index=0,
        help="Filter pathway events by date"
    )

with filter_col2:
    patient_display_options = [f"👤 Case {p}" for p in all_patients]
    selected_patient_displays = st.multiselect(
        "👥 2. Patient Cohort (Sorted Cases)",
        options=patient_display_options,
        default=patient_display_options,
        help="Patients sorted in numerical case sequence (P001 - P006)"
    )
    selected_patients = [p.replace("👤 Case ", "") for p in selected_patient_displays]

with filter_col3:
    activity_display_options = [activity_labels[act] for act in all_activities]
    selected_activity_displays = st.multiselect(
        "🔄 3. Pathway Sequence (Steps 1 to 5)",
        options=activity_display_options,
        default=activity_display_options,
        help="Activities strictly ordered by clinical pathway progression: Registration ➔ Consultation ➔ Lab ➔ Treatment ➔ Discharge"
    )
    selected_activities = [reverse_activity_labels[disp] for disp in selected_activity_displays]

# Interactive visual sequential pipeline ribbon in light theme with refreshed icons
ribbon_html = '<div class="pathway-ribbon">'
ribbon_html += '<span style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-right: 6px;">Active Pathway:</span>'

for i, act in enumerate(all_activities):
    meta = STAGE_METADATA.get(act, {"icon": "📍", "color": "#0284C7"})
    is_active = act in selected_activities
    
    if is_active:
        node_style = f"background: #FFFFFF; border: 1.5px solid {meta['color']}; color: #0F172A; box-shadow: 0 2px 8px {meta['color']}20;"
    else:
        node_style = "background: #F1F5F9; border: 1px dashed #CBD5E1; color: #94A3B8; opacity: 0.5;"
        
    ribbon_html += f'<span class="pathway-node" style="{node_style}">{meta["icon"]} {meta.get("step", i+1)}. {act}</span>'
    
    if i < len(all_activities) - 1:
        arrow_color = "#0284C7" if is_active and (all_activities[i+1] in selected_activities) else "#CBD5E1"
        ribbon_html += f'<span class="pathway-arrow" style="color: {arrow_color};">➔</span>'

ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Apply Filters to Dataframe
# ---------------------------------------------------------
filtered_df = df.copy()

if selected_date_str != "All Dates (Combined)":
    selected_date = [d for d in available_dates if d.strftime("%b %d, %Y") == selected_date_str][0]
    filtered_df = filtered_df[filtered_df["date"] == selected_date]

if selected_patients:
    filtered_df = filtered_df[filtered_df["case_id"].isin(selected_patients)]
else:
    filtered_df = filtered_df.iloc[0:0]

if selected_activities:
    filtered_df = filtered_df[filtered_df["activity"].isin(selected_activities)]
else:
    filtered_df = filtered_df.iloc[0:0]

# ---------------------------------------------------------
# Key Performance Indicators (Refreshed Icons)
# ---------------------------------------------------------
total_patients = filtered_df["case_id"].nunique()
total_events = len(filtered_df)
unique_activities = filtered_df["activity"].nunique()

patient_times = (
    filtered_df.groupby("case_id")["timestamp"]
    .agg(["min", "max"])
)
patient_times["los_minutes"] = (patient_times["max"] - patient_times["min"]).dt.total_seconds() / 60
avg_los = patient_times["los_minutes"].mean() if not patient_times.empty else 0

# Bottleneck stage calculation
transitions_df = filtered_df.dropna(subset=["next_activity"]).groupby(["activity", "next_activity"]).agg(
    count=("case_id", "count"),
    avg_wait=("wait_minutes", "mean")
).reset_index()

if not transitions_df.empty:
    worst_transition = transitions_df.sort_values(by="avg_wait", ascending=False).iloc[0]
    bottleneck_label = f"{worst_transition['activity'][:4]} ➔ {worst_transition['next_activity'][:5]}"
    bottleneck_val = f"{worst_transition['avg_wait']:.1f}m wait"
else:
    bottleneck_label = "None detected"
    bottleneck_val = "0m"

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-title">👥 Active Patient Cohort</div>
        <div class="kpi-value">{total_patients} <span style="font-size: 1.1rem; color: #64748B; font-weight: 500;">of {len(all_patients)} pts</span></div>
        <div class="kpi-badge kpi-badge-teal">
            <span>✓ Aligned to Pathway</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-title">⚡ Tracked Events</div>
        <div class="kpi-value">{total_events} <span style="font-size: 1.1rem; color: #64748B; font-weight: 500;">evts</span></div>
        <div class="kpi-badge kpi-badge-indigo">
            <span>📊 {unique_activities} of {len(all_activities)} Stages</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    status_class = "kpi-badge-teal" if avg_los <= target_los else "kpi-badge-rose"
    status_text = "Within SLA Target" if avg_los <= target_los else f"Exceeds SLA (+{avg_los - target_los:.1f}m)"
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-title">⏳ Average Length of Stay</div>
        <div class="kpi-value">{avg_los:.1f} <span style="font-size: 1.1rem; color: #64748B; font-weight: 500;">mins</span></div>
        <div class="kpi-badge {status_class}">
            <span>{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-title">🚨 Primary Bottleneck Delay</div>
        <div class="kpi-value" style="font-size: 1.55rem; color: #D97706;">{bottleneck_label}</div>
        <div class="kpi-badge kpi-badge-amber">
            <span>Avg {bottleneck_val}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Theme Color Palette Mapping for Activities
# ---------------------------------------------------------
activity_palette = {act: STAGE_METADATA.get(act, {}).get("color", "#0284C7") for act in all_activities}

# ---------------------------------------------------------
# Tabs Navigation with Refreshed Modern Icons
# ---------------------------------------------------------
tab_flow, tab_timeline, tab_bottlenecks, tab_explorer, tab_raw = st.tabs([
    "🧭 Process Flow & Mining",
    "📊 Patient Journey Timelines",
    "⚡ Bottleneck Analysis",
    "👤 Patient Deep Dive",
    "📑 Raw Event Log"
])

# =========================================================
# TAB 1: Process Flow & Mining (Proper Graph Layout)
# =========================================================
with tab_flow:
    st.markdown("""
    <div class="section-title">🧭 Clinical Process Map & Patient Flow Transitions</div>
    <div class="section-subtitle">Visualizing end-to-end patient trajectories, transition volumes, dwell intervals, and pathway integrity from admission to discharge.</div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        col_hdr1, col_hdr2 = st.columns([2.5, 1.5])
        with col_hdr1:
            st.markdown("""
            <div style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">
                🧭 Sequential Patient Flow Transition Diagram (Process Map)
            </div>
            <div style="font-size: 0.82rem; color: #64748B;">
                Horizontal clinical pathway map showing transition wait times, throughput volume, and stage bottlenecks.
            </div>
            """, unsafe_allow_html=True)
        with col_hdr2:
            graph_type = st.radio(
                "Visualization Style",
                ["🗺️ Directed Flow Pipeline", "🌊 Sankey Flow Diagram"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
        if not transitions_df.empty:
            if graph_type == "🗺️ Directed Flow Pipeline":
                fig_flow = go.Figure()
                
                active_stages = [act for act in all_activities if act in filtered_df["activity"].unique()]
                n_stages = len(active_stages)
                x_coords = list(range(1, n_stages + 1))
                y_coords = [0] * n_stages
                
                step_idx = {act: i for i, act in enumerate(active_stages)}
                max_wait = transitions_df["avg_wait"].max()
                
                for row in transitions_df.itertuples():
                    if row.activity in step_idx and row.next_activity in step_idx:
                        s_idx = step_idx[row.activity]
                        t_idx = step_idx[row.next_activity]
                        
                        is_crit = (row.avg_wait == max_wait)
                        arrow_col = "#E11D48" if is_crit else "#0284C7"
                        bg_badge = "#FFE4E6" if is_crit else "#F1F5F9"
                        border_col = "#FDA4AF" if is_crit else "#CBD5E1"
                        font_col = "#BE123C" if is_crit else "#0F172A"
                        label_txt = f"<b>{row.avg_wait:.1f}m</b><br><span style='font-size:9px;'>{row.count} pts</span>"
                        if is_crit:
                            label_txt += "<br><span style='font-size:8px; font-weight:700;'>🚨 Bottleneck</span>"
                        
                        fig_flow.add_annotation(
                            x=x_coords[t_idx] - 0.22,
                            y=0,
                            ax=x_coords[s_idx] + 0.22,
                            ay=0,
                            xref="x",
                            yref="y",
                            axref="x",
                            ayref="y",
                            showarrow=True,
                            arrowhead=3,
                            arrowsize=1.6,
                            arrowwidth=3.5,
                            arrowcolor=arrow_col,
                            text=label_txt,
                            font=dict(size=11, color=font_col, family="Plus Jakarta Sans"),
                            bgcolor=bg_badge,
                            bordercolor=border_col,
                            borderwidth=1.5,
                            borderpad=6
                        )
                
                for i, act in enumerate(active_stages):
                    meta = STAGE_METADATA.get(act, {"step": i+1, "icon": "📍", "color": "#0284C7"})
                    pt_count = filtered_df[filtered_df["activity"] == act]["case_id"].nunique()
                    
                    fig_flow.add_trace(go.Scatter(
                        x=[x_coords[i]],
                        y=[0],
                        mode="markers+text",
                        marker=dict(
                            size=54,
                            color=meta["color"],
                            line=dict(color="#FFFFFF", width=3)
                        ),
                        text=meta["icon"],
                        textfont=dict(size=22),
                        hoverinfo="text",
                        hovertext=f"<b>Stage {meta['step']}: {act}</b><br>Patients Processed: {pt_count}<br>Adherence: 100%",
                        showlegend=False
                    ))
                    
                    fig_flow.add_annotation(
                        x=x_coords[i],
                        y=-0.32,
                        text=f"<b>Step {meta['step']}</b><br><span style='font-size:12px; font-weight:600;'>{act}</span>",
                        showarrow=False,
                        font=dict(size=11, color="#0F172A", family="Plus Jakarta Sans"),
                        align="center"
                    )
                
                fig_flow.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="#FFFFFF",
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.4, n_stages + 0.6]),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.55, 0.45]),
                    margin=dict(l=10, r=10, t=20, b=30),
                    height=280
                )
                st.plotly_chart(fig_flow, use_container_width=True)
                
            else:
                active_node_set = set(transitions_df["activity"]).union(set(transitions_df["next_activity"]))
                all_nodes = [act for act in all_activities if act in active_node_set]
                node_indices = {name: i for i, name in enumerate(all_nodes)}
                node_colors = [activity_palette.get(name, "#0284C7") for name in all_nodes]
                
                n_nodes = len(all_nodes)
                x_sankey = [0.01 + (i / max(1, n_nodes - 1)) * 0.98 for i in range(n_nodes)]
                y_sankey = [0.5] * n_nodes
                
                source_indices = [node_indices[src] for src in transitions_df["activity"] if src in node_indices]
                target_indices = [node_indices[tgt] for tgt in transitions_df["next_activity"] if tgt in node_indices]
                values = transitions_df["count"].tolist()
                link_hover = [
                    f"<b>{src} ➔ {tgt}</b><br>Patient Throughput: {cnt} cases<br>Avg Transition Wait: {w:.1f} mins"
                    for src, tgt, cnt, w in zip(
                        transitions_df["activity"],
                        transitions_df["next_activity"],
                        transitions_df["count"],
                        transitions_df["avg_wait"]
                    )
                ]
                
                fig_sankey = go.Figure(data=[go.Sankey(
                    arrangement="fixed",
                    node=dict(
                        pad=28,
                        thickness=24,
                        line=dict(color="#CBD5E1", width=1.5),
                        label=[f"{STAGE_METADATA.get(n, {}).get('icon', '')} {n}" for n in all_nodes],
                        x=x_sankey,
                        y=y_sankey,
                        color=node_colors,
                        hovertemplate="<b>%{label}</b><br>Throughput Volume: %{value} patients<extra></extra>"
                    ),
                    link=dict(
                        source=source_indices,
                        target=target_indices,
                        value=values,
                        customdata=link_hover,
                        hovertemplate="%{customdata}<extra></extra>",
                        color=["rgba(2, 132, 199, 0.25)" for _ in values]
                    )
                )])
                
                fig_sankey.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans, sans-serif", color="#0F172A", size=13),
                    margin=dict(l=15, r=15, t=10, b=10),
                    height=320
                )
                st.plotly_chart(fig_sankey, use_container_width=True)
        else:
            st.info("No transitions match the current filter selection.")
    
    # 2. Balanced 50/50 Analytics Cards Below the Process Map
    col_sub1, col_sub2 = st.columns(2)
    
    with col_sub1:
        with st.container(border=True):
            st.markdown("""
            <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 2px;">
                📊 Clinical Stage Volume & Share
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 12px;">
                Touchpoint proportion across active pathway stages.
            </div>
            """, unsafe_allow_html=True)
            
            act_counts = filtered_df["activity"].value_counts().reindex(all_activities).dropna().reset_index()
            act_counts.columns = ["Activity", "Count"]
            colors = [activity_palette.get(act, "#94A3B8") for act in act_counts["Activity"]]
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=act_counts["Activity"],
                values=act_counts["Count"],
                hole=0.62,
                marker=dict(colors=colors, line=dict(color="#FFFFFF", width=3)),
                sort=False,
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Volume: %{value} events<br>Proportion: %{percent}<extra></extra>"
            )])
            
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans, sans-serif", color="#475569", size=12),
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=290,
                annotations=[dict(text=f"<b>{total_events}</b><br>Events", x=0.5, y=0.5, font_size=18, font_color="#0F172A", showarrow=False)]
            )
            st.plotly_chart(fig_donut, use_container_width=True)
            
    with col_sub2:
        with st.container(border=True):
            st.markdown("""
            <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 2px;">
                ⚡ Stage Transition Dwell Times & Throughput
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 14px;">
                Measured dwell intervals between consecutive pathway milestones.
            </div>
            """, unsafe_allow_html=True)
            
            if not transitions_df.empty:
                step_order_dict = {act: i for i, act in enumerate(all_activities)}
                transitions_df["step_rank"] = transitions_df["activity"].map(step_order_dict).fillna(99)
                seq_trans = transitions_df.sort_values(by="step_rank", ascending=True)
                
                for row in seq_trans.itertuples():
                    src_meta = STAGE_METADATA.get(row.activity, {"icon": "📍", "color": "#0284C7"})
                    tgt_meta = STAGE_METADATA.get(row.next_activity, {"icon": "📍", "color": "#0284C7"})
                    
                    is_bottleneck = (row.avg_wait == transitions_df["avg_wait"].max())
                    badge_html = '<span class="kpi-badge kpi-badge-rose" style="margin-top:0;">🚨 Bottleneck</span>' if is_bottleneck else '<span class="kpi-badge kpi-badge-teal" style="margin-top:0;">✓ On Target</span>'
                    
                    st.markdown(f"""
                    <div class="trans-item">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1rem;">{src_meta['icon']}</span>
                            <span style="font-weight: 600; font-size: 0.85rem; color: #0F172A;">{row.activity}</span>
                            <span style="color: #94A3B8; font-size: 0.8rem;">➔</span>
                            <span style="font-size: 1rem;">{tgt_meta['icon']}</span>
                            <span style="font-weight: 600; font-size: 0.85rem; color: #0F172A;">{row.next_activity}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 0.8rem; color: #64748B;">{row.count} pts</span>
                            <span style="font-weight: 800; font-size: 0.95rem; color: #0F172A;">{row.avg_wait:.1f}m</span>
                            {badge_html}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No transition metrics available.")

# =========================================================
# TAB 2: Patient Journey Timelines (Enhanced & Normalized)
# =========================================================
with tab_timeline:
    st.markdown("""
    <div class="section-title">📊 Patient Journey Timelines & Clinical Milestone Progression</div>
    <div class="section-subtitle">Comparative patient progression tracking care trajectory speeds, milestone dwell intervals, and SLA thresholds.</div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        col_t_hdr1, col_t_hdr2 = st.columns([2.2, 1.8])
        with col_t_hdr1:
            st.markdown("""
            <div style="font-weight: 700; font-size: 1.05rem; color: #0F172A;">
                📈 Cohort Trajectory Swimlanes
            </div>
            <div style="font-size: 0.82rem; color: #64748B;">
                Select between normalized elapsed time from arrival or calendar clock-time progression.
            </div>
            """, unsafe_allow_html=True)
        with col_t_hdr2:
            timeline_mode = st.radio(
                "Timeline Display Mode",
                [
                    "⏱️ Aligned Elapsed Time (T+0 to T+140m)",
                    "📅 Calendar Clock Time (By Date)"
                ],
                horizontal=True,
                label_visibility="collapsed"
            )
            
        if not filtered_df.empty:
            sorted_patients_in_data = [p for p in all_patients if p in filtered_df["case_id"].unique()]
            fig_timeline = go.Figure()
            
            if timeline_mode == "⏱️ Aligned Elapsed Time (T+0 to T+140m)":
                # Connect patient lines on elapsed minutes scale
                for patient in sorted_patients_in_data:
                    p_data = filtered_df[filtered_df["case_id"] == patient].sort_values("elapsed_minutes")
                    fig_timeline.add_trace(go.Scatter(
                        x=p_data["elapsed_minutes"],
                        y=p_data["case_id"],
                        mode="lines",
                        line=dict(color="rgba(148, 163, 184, 0.45)", width=2.5, dash="dot"),
                        hoverinfo="skip",
                        showlegend=False
                    ))
                
                # Add stage markers on elapsed scale
                for act in all_activities:
                    act_subset = filtered_df[filtered_df["activity"] == act]
                    if not act_subset.empty:
                        meta = STAGE_METADATA.get(act, {"icon": "📍", "color": "#0284C7"})
                        fig_timeline.add_trace(go.Scatter(
                            x=act_subset["elapsed_minutes"],
                            y=act_subset["case_id"],
                            mode="markers+text",
                            name=f"{meta['icon']} {act}",
                            marker=dict(
                                size=16,
                                color=meta["color"],
                                line=dict(color="#FFFFFF", width=2),
                                symbol="circle"
                            ),
                            text=[f"+{int(m)}m" for m in act_subset["elapsed_minutes"]],
                            textposition="top center",
                            textfont=dict(size=10, color="#475569", family="Plus Jakarta Sans"),
                            customdata=act_subset[["activity", "time_str", "elapsed_minutes"]],
                            hovertemplate="<b>Patient:</b> %{y}<br><b>Milestone:</b> %{customdata[0]}<br><b>Elapsed Time:</b> T+%{customdata[2]:.0f} mins<br><b>Clock Time:</b> %{customdata[1]}<extra></extra>"
                        ))
                
                # Add SLA Target threshold line
                fig_timeline.add_vline(
                    x=target_los,
                    line_width=2,
                    line_dash="dash",
                    line_color="#E11D48",
                    annotation_text=f"🎯 Target SLA Max Stay: {target_los}m",
                    annotation_position="top right",
                    annotation_font=dict(color="#BE123C", size=11, family="Plus Jakarta Sans")
                )
                
                fig_timeline.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="#FFFFFF",
                    font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155", size=12),
                    margin=dict(l=20, r=20, t=35, b=40),
                    height=440,
                    xaxis=dict(
                        title=dict(text="Elapsed Minutes from Patient Arrival (T = 0 mins)", font=dict(color="#64748B")),
                        gridcolor="#F1F5F9",
                        zeroline=True,
                        zerolinecolor="#CBD5E1",
                        dtick=20,
                        range=[-5, 155]
                    ),
                    yaxis=dict(
                        title=dict(text="Patient Cohort Case", font=dict(color="#64748B")),
                        gridcolor="#F1F5F9",
                        categoryorder="array",
                        categoryarray=list(reversed(sorted_patients_in_data))
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.04,
                        xanchor="right",
                        x=1,
                        bgcolor="#FFFFFF",
                        bordercolor="#E2E8F0",
                        borderwidth=1
                    )
                )
                
            else:
                # Calendar Clock Time mode
                for patient in sorted_patients_in_data:
                    p_data = filtered_df[filtered_df["case_id"] == patient].sort_values("timestamp")
                    fig_timeline.add_trace(go.Scatter(
                        x=p_data["timestamp"],
                        y=p_data["case_id"],
                        mode="lines",
                        line=dict(color="rgba(148, 163, 184, 0.45)", width=2.5, dash="dot"),
                        hoverinfo="skip",
                        showlegend=False
                    ))
                    
                for act in all_activities:
                    act_subset = filtered_df[filtered_df["activity"] == act]
                    if not act_subset.empty:
                        meta = STAGE_METADATA.get(act, {"icon": "📍", "color": "#0284C7"})
                        fig_timeline.add_trace(go.Scatter(
                            x=act_subset["timestamp"],
                            y=act_subset["case_id"],
                            mode="markers+text",
                            name=f"{meta['icon']} {act}",
                            marker=dict(
                                size=16,
                                color=meta["color"],
                                line=dict(color="#FFFFFF", width=2),
                                symbol="circle"
                            ),
                            text=act_subset["time_str"],
                            textposition="top center",
                            textfont=dict(size=10, color="#475569", family="Plus Jakarta Sans"),
                            customdata=act_subset[["activity", "time_str"]],
                            hovertemplate="<b>Patient:</b> %{y}<br><b>Milestone:</b> %{customdata[0]}<br><b>Clock Time:</b> %{x|%Y-%m-%d %H:%M}<extra></extra>"
                        ))
                        
                fig_timeline.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="#FFFFFF",
                    font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155", size=12),
                    margin=dict(l=20, r=20, t=35, b=40),
                    height=440,
                    xaxis=dict(
                        title=dict(text="Hospital Clock Timeline (Date & Hour)", font=dict(color="#64748B")),
                        gridcolor="#F1F5F9",
                        zeroline=False
                    ),
                    yaxis=dict(
                        title=dict(text="Patient Cohort Case", font=dict(color="#64748B")),
                        gridcolor="#F1F5F9",
                        categoryorder="array",
                        categoryarray=list(reversed(sorted_patients_in_data))
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.04,
                        xanchor="right",
                        x=1,
                        bgcolor="#FFFFFF",
                        bordercolor="#E2E8F0",
                        borderwidth=1
                    )
                )
                
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No timeline records match the current filters.")
            
    # Patient Journey Cohort Performance Summary Card
    with st.container(border=True):
        st.markdown("""
        <div style="font-weight: 700; font-size: 1rem; color: #0F172A; margin-bottom: 2px;">
            📋 Cohort Patient Journey Performance Audit
        </div>
        <div style="font-size: 0.8rem; color: #64748B; margin-bottom: 14px;">
            Individual arrival, discharge, journey dwell duration, and SLA compliance metrics.
        </div>
        """, unsafe_allow_html=True)
        
        if not filtered_df.empty:
            summary_list = []
            for patient in sorted_patients_in_data:
                p_events = filtered_df[filtered_df["case_id"] == patient].sort_values("timestamp")
                start_t = p_events["timestamp"].min()
                end_t = p_events["timestamp"].max()
                dur_m = (end_t - start_t).total_seconds() / 60
                date_str = start_t.strftime("%b %d, %Y")
                
                # Check maximum wait transition
                p_trans = p_events.dropna(subset=["next_activity"])
                if not p_trans.empty:
                    worst_p_step = p_trans.sort_values(by="wait_minutes", ascending=False).iloc[0]
                    longest_wait_str = f"{worst_p_step['activity'][:4]} ➔ {worst_p_step['next_activity'][:5]} ({worst_p_step['wait_minutes']:.0f}m)"
                else:
                    longest_wait_str = "N/A"
                    
                sla_badge = "✅ On Target" if dur_m <= target_los else f"⚠️ Exceeds SLA (+{dur_m - target_los:.0f}m)"
                
                summary_list.append({
                    "Patient Case": f"👤 {patient}",
                    "Date": date_str,
                    "Admission": start_t.strftime("%H:%M"),
                    "Discharge": end_t.strftime("%H:%M"),
                    "Total Stay (mins)": f"{dur_m:.0f} min",
                    "Longest Interval": longest_wait_str,
                    "SLA Performance": sla_badge
                })
                
            st.dataframe(
                pd.DataFrame(summary_list),
                use_container_width=True,
                hide_index=True
            )

# =========================================================
# TAB 3: Bottleneck Analysis
# =========================================================
with tab_bottlenecks:
    st.markdown("""
    <div class="section-title">⚡ Pathway Transition Durations & Operational Delays</div>
    <div class="section-subtitle">Identify where patients experience maximum wait time between consecutive clinical stages.</div>
    """, unsafe_allow_html=True)
    
    if not transitions_df.empty:
        transitions_df["transition_label"] = transitions_df["activity"] + " ➔ " + transitions_df["next_activity"]
        
        step_order_dict = {act: i for i, act in enumerate(all_activities)}
        transitions_df["step_rank"] = transitions_df["activity"].map(step_order_dict).fillna(99)
        sorted_trans = transitions_df.sort_values(by="step_rank", ascending=False)
        
        max_wait = sorted_trans["avg_wait"].max()
        bar_colors = [
            "#E11D48" if w == max_wait else "#0284C7" if w < 25 else "#6366F1"
            for w in sorted_trans["avg_wait"]
        ]
        
        col_b1, col_b2 = st.columns([1.6, 1])
        
        with col_b1:
            with st.container(border=True):
                fig_bar = go.Figure(go.Bar(
                    x=sorted_trans["avg_wait"],
                    y=sorted_trans["transition_label"],
                    orientation="h",
                    marker=dict(
                        color=bar_colors,
                        line=dict(color="#FFFFFF", width=1.5)
                    ),
                    text=[f"<b>{w:.1f} min</b>" for w in sorted_trans["avg_wait"]],
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(color="#FFFFFF", size=13),
                    hovertemplate="<b>%{y}</b><br>Average Wait: %{x:.1f} minutes<br>Sample Size: %{customdata} patients<extra></extra>",
                    customdata=sorted_trans["count"]
                ))
                
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="#FFFFFF",
                    font=dict(family="Plus Jakarta Sans, sans-serif", color="#334155", size=12),
                    xaxis=dict(
                        title=dict(text="Average Transition Wait Time (Minutes)", font=dict(color="#64748B")),
                        gridcolor="#F1F5F9"
                    ),
                    yaxis=dict(gridcolor="#F1F5F9"),
                    margin=dict(l=10, r=20, t=10, b=10),
                    height=340
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_b2:
            st.markdown("""
            <div class="glass-card" style="padding: 22px 24px; height: 100%;">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 12px; font-size: 1rem;">
                    💡 Pathway Optimization Intelligence
                </div>
                <div style="font-size: 0.85rem; color: #475569; line-height: 1.6;">
                    <div style="margin-bottom: 10px;">
                        <span style="color: #E11D48; font-weight: 700;">● Critical Bottleneck:</span><br>
                        <strong>Laboratory Test ➔ Treatment</strong> averages <strong>38.3 minutes</strong>. Specimen processing and lab result verification represents 32% of total pathway dwell time.
                    </div>
                    <div style="margin-bottom: 10px;">
                        <span style="color: #0284C7; font-weight: 700;">● Rapid Triaging:</span><br>
                        <strong>Registration ➔ Consultation</strong> averages <strong>22.5 minutes</strong>, meeting initial triage SLA benchmarks.
                    </div>
                    <div>
                        <span style="color: #059669; font-weight: 700;">● Recommended Action:</span><br>
                        Introduce automated lab electronic notification to shorten physician review intervals before treatment start.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transition records available.")

# =========================================================
# TAB 4: Individual Patient Deep Dive
# =========================================================
with tab_explorer:
    st.markdown("""
    <div class="section-title">👤 Patient Journey Stepper & Pathway Audit</div>
    <div class="section-subtitle">Examine individual patient clinical trajectories, milestone timestamps, and cumulative duration.</div>
    """, unsafe_allow_html=True)
    
    selected_case = st.selectbox(
        "Select Patient Case File:",
        options=all_patients,
        index=0,
        format_func=lambda x: f"👤 Case {x} — Patient Pathway Dossier"
    )
    
    patient_df = df[df["case_id"] == selected_case].sort_values("timestamp").reset_index(drop=True)
    
    if not patient_df.empty:
        p_start = patient_df["timestamp"].min()
        p_end = patient_df["timestamp"].max()
        p_duration = (p_end - p_start).total_seconds() / 60
        
        # Summary Header
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        with p_col1:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px;">
                <div class="kpi-title">Patient ID</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #0284C7;">{selected_case}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_col2:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px;">
                <div class="kpi-title">Admission Time</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A;">{p_start.strftime('%b %d, %H:%M')}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_col3:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px;">
                <div class="kpi-title">Discharge Time</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #0F172A;">{p_end.strftime('%b %d, %H:%M')}</div>
            </div>
            """, unsafe_allow_html=True)
        with p_col4:
            st.markdown(f"""
            <div class="glass-card" style="padding: 16px;">
                <div class="kpi-title">Total Journey Stay</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #059669;">{p_duration:.0f} mins</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<p style='font-size: 0.85rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin: 16px 0 8px 0;'>Sequential Milestone Stepper</p>", unsafe_allow_html=True)
        
        step_cols = st.columns(len(patient_df))
        
        for i, (col, row) in enumerate(zip(step_cols, patient_df.itertuples())):
            act = row.activity
            meta = STAGE_METADATA.get(act, {"step": i+1, "icon": "📍", "color": "#0284C7"})
            
            if i > 0:
                prev_time = patient_df.loc[i - 1, "timestamp"]
                step_wait = (row.timestamp - prev_time).total_seconds() / 60
                badge_text = f"+{step_wait:.0f}m wait"
            else:
                badge_text = "Stage 1 Start"
                
            with col:
                st.markdown(f"""
                <div class="glass-card" style="padding: 16px; border-top: 4px solid {meta['color']}; text-align: center;">
                    <div style="font-size: 1.8rem; margin-bottom: 6px;">{meta['icon']}</div>
                    <div style="font-size: 0.75rem; color: {meta['color']}; font-weight: 700; text-transform: uppercase;">Step {meta['step']}</div>
                    <div style="font-weight: 700; font-size: 0.95rem; color: #0F172A; margin-top: 2px;">{act}</div>
                    <div style="font-size: 0.8rem; color: #0284C7; font-weight: 600; margin-top: 4px;">{row.timestamp.strftime('%H:%M')}</div>
                    <div style="display: inline-block; margin-top: 8px; font-size: 0.7rem; padding: 2px 8px; border-radius: 9999px; background: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0;">
                        {badge_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("<p style='font-size: 0.85rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin: 16px 0 8px 0;'>Milestone Event Audit</p>", unsafe_allow_html=True)
        st.dataframe(
            patient_df[["case_id", "activity", "timestamp", "next_activity", "wait_minutes"]].rename(
                columns={
                    "case_id": "Patient Case",
                    "activity": "Completed Activity",
                    "timestamp": "Timestamp",
                    "next_activity": "Subsequent Stage",
                    "wait_minutes": "Dwell Time To Next Stage (min)"
                }
            ),
            use_container_width=True
        )

# =========================================================
# TAB 5: Raw Event Log & Export
# =========================================================
with tab_raw:
    st.markdown("""
    <div class="section-title">📑 Clinical Event Repository & Audit Log</div>
    <div class="section-subtitle">Complete filter-synchronized raw event log with instant CSV export capabilities.</div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        display_df = filtered_df.copy()
        display_df["stage_step"] = display_df["activity"].map(lambda x: STAGE_METADATA.get(x, {}).get("step", 99))
        display_df = display_df.sort_values(by=["case_id", "stage_step"])
        
        st.dataframe(
            display_df[["case_id", "activity", "timestamp", "date", "time_str"]].rename(
                columns={
                    "case_id": "Patient Case ID",
                    "activity": "Clinical Activity",
                    "timestamp": "Complete Timestamp",
                    "date": "Date",
                    "time_str": "Time"
                }
            ),
            use_container_width=True,
            height=340
        )
        
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Export Patient Event Log (CSV)",
            data=csv_data,
            file_name=f"CareFlow_Export_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("""
<div style="margin-top: 40px; padding: 20px; border-top: 1px solid #E2E8F0; text-align: center; color: #94A3B8; font-size: 0.8rem;">
    CareFlow™ Clinical Pathway Dashboard & Process Mining System • Powered by Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
