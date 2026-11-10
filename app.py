"""
app.py
======
AcrePulse | Precision Agronomy & Crop Health Intelligence
Production-grade Agri-Tech web application for automated foliar pathology,
microclimate intelligence, and variable-rate irrigation.
"""

import os
import time
import json
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
import altair as alt

# Import internal modules
from src.classifier import EdgePlantClassifier
from src.remedies import get_remedy
from src.soil_advisor import evaluate_soil_and_irrigation

# -----------------------------------------------------------------------------
# App Configuration & Metadata
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AgroEdge AI | Autonomous Agronomy Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# Enterprise High-End UI Stylesheet
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1350px;
    }

    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 14px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }
    .brand-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-logo {
        background: linear-gradient(135deg, #10B981, #059669);
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.35);
    }
    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #F9FAFB;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .brand-tag {
        font-size: 11px;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin: 0;
    }
    .nav-status-group {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .pill-badge {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 500;
        color: #D1D5DB;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }

    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .kpi-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px 20px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        border-color: rgba(16, 185, 129, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #F9FAFB;
        line-height: 1.1;
    }
    .kpi-subtext {
        font-size: 12px;
        margin-top: 6px;
        font-weight: 500;
    }
    .text-green { color: #10B981; }
    .text-amber { color: #F59E0B; }
    .text-blue { color: #3B82F6; }

    /* Custom Glass Cards */
    .glass-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .section-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 18px;
    }
    .section-title {
        font-size: 17px;
        font-weight: 700;
        color: #F3F4F6;
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 0;
    }
    .section-desc {
        font-size: 13px;
        color: #9CA3AF;
        margin-top: 3px;
    }

    /* Diagnosis Result Card */
    .diagnosis-banner {
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .diag-healthy {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .diag-pathogen {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    .diag-title {
        font-size: 22px;
        font-weight: 800;
        margin: 0 0 6px 0;
    }
    .diag-sub {
        font-size: 13px;
        color: #D1D5DB;
        margin: 0;
    }

    /* Valve Status Banner */
    .valve-card-active {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(185, 28, 28, 0.25));
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 14px;
        padding: 20px;
    }
    .valve-card-standby {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12), rgba(5, 150, 105, 0.2));
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 14px;
        padding: 20px;
    }

    /* Tab Custom Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #1F2937;
        border-radius: 10px;
        padding: 10px 20px;
        color: #9CA3AF;
        border: 1px solid rgba(255, 255, 255, 0.05);
        font-weight: 600;
        font-size: 13px;
    }
    .stTabs [aria-selected="true"] {
        background: #10B981 !important;
        color: #FFFFFF !important;
        border-color: #10B981 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Initialize Core Classifier
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_classifier():
    return EdgePlantClassifier()

classifier = get_classifier()

# -----------------------------------------------------------------------------
# Top Navigation Bar (Production SaaS Style)
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-nav">
    <div class="brand-group">
        <div class="brand-logo">🌿</div>
        <div>
            <h1 class="brand-title">AgroEdge AI</h1>
            <p class="brand-tag">Autonomous Precision Agronomy & Foliar Pathology</p>
        </div>
    </div>
    <div class="nav-status-group">
        <div class="pill-badge">
            <span class="pulse-dot"></span>
            <span>Edge Node: <strong>Active (Offline-First)</strong></span>
        </div>
        <div class="pill-badge">
            <span>📍 GreenValley Estate • Block 4</span>
        </div>
        <div class="pill-badge">
            <span>⛅ 26°C • Humidity 64% • Clear</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Executive KPI Metric Strip
# -----------------------------------------------------------------------------
st.markdown("""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">Canopy Health Score</div>
        <div class="kpi-value text-green">94.8%</div>
        <div class="kpi-subtext text-green">↑ 2.1% from last inspection</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Active Soil Hydration</div>
        <div class="kpi-value text-blue">42.5%</div>
        <div class="kpi-subtext" style="color:#9CA3AF;">Optimal Field Capacity</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Disease Outbreak Risk</div>
        <div class="kpi-value text-amber">Low / Caution</div>
        <div class="kpi-subtext" style="color:#9CA3AF;">High humidity forecast at 20:00</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Local Diagnostic Engine</div>
        <div class="kpi-value" style="color:#E5E7EB;">18 ms</div>
        <div class="kpi-subtext text-green">● INT8 Neural Model (2.56 MB)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Main Operational Modules
# -----------------------------------------------------------------------------
tab_diagnostics, tab_irrigation, tab_analytics, tab_station = st.tabs([
    "🔬 Foliar Pathology & AI Clinic",
    "💧 Microclimate & Closed-Loop Irrigation",
    "📈 Field Telemetry & Sensor Analytics",
    "🚜 Field Station & Agronomy Profile"
])

# =============================================================================
# MODULE 1: AI CROP CLINIC & PATHOLOGY
# =============================================================================
with tab_diagnostics:
    col_upload_panel, col_results_panel = st.columns([1.1, 1.4], gap="large")

    with col_upload_panel:
        st.markdown("""
        <div class="glass-card">
            <h3 class="section-title">📷 Crop Foliage Scanner</h3>
            <p class="section-desc">Submit leaf photography to perform rapid on-device cellular and tissue pathology diagnostics.</p>
        </div>
        """, unsafe_allow_html=True)

        scan_method = st.radio(
            "Input Method",
            ["Preset Inspection Library", "Upload Field Photo", "Live Camera Scanner"],
            horizontal=True,
            label_visibility="collapsed"
        )

        active_image = None

        if scan_method == "Preset Inspection Library":
            sample_dir = os.path.join(os.path.dirname(__file__), "sample_images")
            samples = {
                "Apple Scab (Venturia inaequalis)": os.path.join(sample_dir, "apple_scab.jpg"),
                "Tomato Early Blight (Alternaria linariae)": os.path.join(sample_dir, "tomato_early_blight.jpg"),
                "Healthy Foliage (Clean Specimen)": os.path.join(sample_dir, "healthy_apple_leaf.jpg")
            }
            selection = st.selectbox("Select Specimen Sample", list(samples.keys()))
            sample_file = samples[selection]
            if os.path.exists(sample_file):
                active_image = Image.open(sample_file)
            else:
                st.warning("Sample image not found on disk.")

        elif scan_method == "Upload Field Photo":
            uploaded_file = st.file_uploader(
                "Drag & drop leaf photo (JPEG, PNG)",
                type=["jpg", "jpeg", "png"],
                help="Recommended: high-contrast top-down view of infected foliage"
            )
            if uploaded_file is not None:
                active_image = Image.open(uploaded_file)

        elif scan_method == "Live Camera Scanner":
            cam_shot = st.camera_input("Capture live foliage image")
            if cam_shot is not None:
                active_image = Image.open(cam_shot)

        if active_image is not None:
            st.image(active_image, caption="Analyzed Specimen", use_container_width=True)

    with col_results_panel:
        if active_image is not None:
            # Execute on-device inference
            with st.spinner("Analyzing foliar morphology and tissue lesions..."):
                analysis = classifier.predict(active_image)
                remedy = get_remedy(analysis["prediction"])

            # Diagnostic Status Header
            if analysis["is_healthy"]:
                st.markdown(f"""
                <div class="diagnosis-banner diag-healthy">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 class="diag-title" style="color:#10B981;">✅ {analysis['prediction']}</h2>
                        <span style="background:rgba(16,185,129,0.2); color:#10B981; font-weight:700; padding:6px 12px; border-radius:8px; font-size:13px;">HEALTHY SPECIMEN</span>
                    </div>
                    <p class="diag-sub">No necrotic lesions, chlorosis, or active sporulation detected on the foliar surface.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="diagnosis-banner diag-pathogen">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h2 class="diag-title" style="color:#EF4444;">⚠️ {analysis['prediction']}</h2>
                        <span style="background:rgba(239,68,68,0.2); color:#EF4444; font-weight:700; padding:6px 12px; border-radius:8px; font-size:13px;">ACTIVE PATHOGEN DETECTED</span>
                    </div>
                    <p class="diag-sub">Pathology classification matches active infectious foliar disease. Immediate remediation recommended.</p>
                </div>
                """, unsafe_allow_html=True)

            # Metrics Row
            col_conf, col_speed, col_model = st.columns(3)
            with col_conf:
                st.metric("Pathology Confidence", f"{analysis['confidence']}%")
            with col_speed:
                st.metric("Analysis Latency", f"{analysis['latency_ms']} ms", delta="Local CPU")
            with col_model:
                st.metric("Model Footprint", f"{analysis['model_size_mb']} MB", delta="INT8 Quantized")

            st.write("")
            st.markdown("##### 🧬 Top Pathological Matches")
            for item in analysis["top_3"]:
                col_name, col_pct = st.columns([3, 1])
                with col_name:
                    st.write(f"**{item['label']}**")
                with col_pct:
                    st.write(f"{item['confidence']}%")
                st.progress(min(1.0, item['confidence'] / 100.0))

            st.write("")
            # Treatment Plan Accordion
            st.markdown("### 💊 Agronomic Prescription & Intervention Guide")
            
            with st.expander("🌿 Bio-Fungicide & Organic Treatment Protocol", expanded=True):
                st.markdown(f"**Target Pathogen:** {remedy.get('pathogen', 'N/A')}")
                st.markdown(f"**Symptom Profile:** {remedy.get('symptoms', 'N/A')}")
                st.success(f"**Organic Recommendation:** {remedy.get('organic', 'N/A')}")

            with st.expander("🧪 Targeted Chemical Fungicide & Application Rate", expanded=True):
                st.warning(f"**Chemical Recommendation:** {remedy.get('chemical', 'N/A')}")
                st.info("⚠️ *Always observe pre-harvest intervals (PHI) and local agricultural environmental regulations.*")

            with st.expander("📅 14-Day Cultural Hygiene & Field Prevention", expanded=False):
                st.write(remedy.get('prevention', 'N/A'))
        else:
            st.info("👈 Select a sample from the inspection library or capture a photo to initiate diagnostic analysis.")

# =============================================================================
# MODULE 2: MICROCLIMATE & CLOSED-LOOP IRRIGATION
# =============================================================================
with tab_irrigation:
    col_controls, col_valve_status = st.columns([1, 1], gap="large")

    with col_controls:
        st.markdown("""
        <div class="glass-card">
            <h3 class="section-title">🎛️ Real-Time Telemetry Controls</h3>
            <p class="section-desc">Simulate soil moisture sensors, weather stations, and soil nutrient levels.</p>
        </div>
        """, unsafe_allow_html=True)

        soil_moisture = st.slider("Volumetric Soil Moisture (%)", 5.0, 95.0, 24.0, 1.0, help="Field Capacity: 30% - 60%")
        air_temp = st.slider("Ambient Canopy Temperature (°C)", 10.0, 45.0, 29.0, 0.5)
        air_humidity = st.slider("Relative Air Humidity (%)", 15.0, 100.0, 84.0, 1.0)

        st.markdown("##### 🧪 Soil N-P-K Fertility Matrix (kg/ha)")
        col_n, col_p, col_k = st.columns(3)
        with col_n:
            val_n = st.number_input("Nitrogen (N)", 0, 300, 48)
        with col_p:
            val_p = st.number_input("Phosphorus (P)", 0, 150, 32)
        with col_k:
            val_k = st.number_input("Potassium (K)", 0, 200, 55)

    with col_valve_status:
        st.markdown("""
        <div class="glass-card">
            <h3 class="section-title">⚡ Closed-Loop Solenoid Actuation</h3>
            <p class="section-desc">Automated on-device valve control without cloud dependency.</p>
        </div>
        """, unsafe_allow_html=True)

        decision = evaluate_soil_and_irrigation(soil_moisture, air_temp, air_humidity, val_n, val_p, val_k)

        if "ACTIVATED" in decision["valve_status"]:
            st.markdown(f"""
            <div class="valve-card-active">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color:#EF4444; margin:0; font-size:18px; font-weight:800;">🚨 VALVE 04: OPEN (PUMPING WATER)</h3>
                    <span style="background:#EF4444; color:white; font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px;">FLOW RATE: 45 L/MIN</span>
                </div>
                <p style="color:#E5E7EB; margin:10px 0 0 0; font-size:13px;">{decision['irrigation_action']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="valve-card-standby">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 style="color:#10B981; margin:0; font-size:18px; font-weight:800;">✅ VALVE 04: CLOSED (STANDBY)</h3>
                    <span style="background:#10B981; color:white; font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px;">FLOW RATE: 0 L/MIN</span>
                </div>
                <p style="color:#E5E7EB; margin:10px 0 0 0; font-size:13px;">{decision['irrigation_action']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### 🌦️ Foliar Disease Weather Matrix")
        if "HIGH" in decision["disease_risk"]:
            st.error(f"**Pathogen Sporulation Index:** {decision['disease_risk']}\n\n{decision['disease_risk_alert']}")
        elif "MODERATE" in decision["disease_risk"]:
            st.warning(f"**Pathogen Sporulation Index:** {decision['disease_risk']}\n\n{decision['disease_risk_alert']}")
        else:
            st.success(f"**Pathogen Sporulation Index:** {decision['disease_risk']}\n\n{decision['disease_risk_alert']}")

        st.markdown("#### 🌾 Soil Nutrition Summary")
        for tip in decision["npk_advisory"]:
            st.markdown(f"• {tip}")

# =============================================================================
# MODULE 3: SENSOR ANALYTICS & FIELD TELEMETRY
# =============================================================================
with tab_analytics:
    st.markdown("""
    <div class="glass-card">
        <h3 class="section-title">📊 24-Hour Diurnal Telemetry Dynamics</h3>
        <p class="section-desc">Soil moisture dry-down curve, automated irrigation replenishment cycle, and vapor pressure deficit.</p>
    </div>
    """, unsafe_allow_html=True)

    hours = [f"{h:02d}:00" for h in range(24)]
    moisture = [58, 57, 56, 55, 54, 52, 49, 44, 38, 32, 28, 24, 21, 18, 16, 54, 62, 61, 60, 59, 59, 58, 58, 57]
    ambient_temp = [21, 20, 20, 19, 19, 21, 23, 26, 29, 32, 34, 35, 35, 34, 32, 30, 28, 26, 25, 24, 23, 22, 22, 21]

    df_chart = pd.DataFrame({
        "Hour": hours,
        "Soil Moisture (%)": moisture,
        "Canopy Temperature (°C)": ambient_temp,
        "Critical Threshold (30%)": [30] * 24
    }).set_index("Hour")

    st.line_chart(df_chart, color=["#10B981", "#F59E0B", "#EF4444"])

    st.markdown("##### 📝 Autonomous Actuation & Synchronization Audit Log")
    log_data = [
        {"Timestamp": "14:48:02", "Node": "NODE-B4", "Sensor Event": "Soil Hydration < 30%", "Action": "Solenoid Valve 04 Opened", "Status": "Autonomous"},
        {"Timestamp": "15:18:40", "Node": "NODE-B4", "Sensor Event": "Soil Hydration 60%", "Action": "Solenoid Valve 04 Closed", "Status": "Autonomous"},
        {"Timestamp": "11:22:15", "Node": "CAM-02", "Sensor Event": "Apple Scab Detected (94.8%)", "Action": "Buffered in Local Flash", "Status": "Local Edge"},
        {"Timestamp": "12:00:00", "Node": "GATEWAY", "Sensor Event": "Cellular Uplink Restored", "Action": "Batch Telemetry Pushed to Cloud", "Status": "Synced"}
    ]
    st.dataframe(pd.DataFrame(log_data), use_container_width=True)

# =============================================================================
# MODULE 4: FIELD STATION & ENTERPRISE CONFIGURATION
# =============================================================================
with tab_station:
    col_meta1, col_meta2 = st.columns(2, gap="large")

    with col_meta1:
        st.markdown("""
        <div class="glass-card">
            <h3 class="section-title">🚜 Field Station Configuration</h3>
            <p class="section-desc">Manage farm acreage, crop boundaries, and agronomic thresholds.</p>
        </div>
        """, unsafe_allow_html=True)

        st.text_input("Farm Name / Estate Identifier", "GreenValley Commercial Estate")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.selectbox("Crop Variety", ["Honeycrisp Apple", "Roma Tomato", "Russet Potato", "Field Corn (Maize)", "Bell Pepper"])
        with col_c2:
            st.number_input("Total Monitored Acreage", value=145, min_value=1)

        st.selectbox("Irrigation Delivery Method", ["Drip Irrigation (Subsurface)", "Overhead Center Pivot", "Micro-Sprinklers"])
        st.button("Save Field Parameters", use_container_width=True)

    with col_meta2:
        st.markdown("""
        <div class="glass-card">
            <h3 class="section-title">⚡ On-Device Runtime Architecture</h3>
            <p class="section-desc">Physical hardware metrics and execution parameters.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        - **Inference Runtime:** `ONNX Runtime v1.31 (CPUExecutionProvider)`
        - **Precision Model:** `MobileNet INT8 Quantized`
        - **Graph Footprint:** `2.56 MB (Zero Network Dependency)`
        - **Target Latency:** `15 - 25 ms per foliage capture`
        - **Supported Foliar Classes:** `38 Standard Pathological Categories`
        - **Offline Telemetry Buffer:** `SQLite Local Persistent Store`
        - **Cloud Protocol:** `REST / HTTPS Gateway Sync`
        """)

# -----------------------------------------------------------------------------
# Global Footer
# -----------------------------------------------------------------------------
st.write("")
st.markdown("""
<div style="text-align:center; padding:20px; color:#6B7280; font-size:12px; border-top:1px solid rgba(255,255,255,0.06); margin-top:30px;">
    <strong>AgroEdge AI</strong> • Enterprise Autonomous Agronomy & Foliar Diagnostics Platform • Powered by ONNX Runtime Engine
</div>
""", unsafe_allow_html=True)
