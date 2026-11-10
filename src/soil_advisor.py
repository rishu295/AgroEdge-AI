"""
soil_advisor.py
===============
Agronomic decision engine for Soil Health, Microclimate Monitoring,
and Automated Irrigation Thresholds.
"""

def evaluate_soil_and_irrigation(soil_moisture: float, temperature: float, humidity: float, 
                                 nitrogen: float, phosphorus: float, potassium: float) -> dict:
    """
    Evaluate real-time IoT farm telemetry and determine:
    1. Irrigation Solenoid Valve Action (ON / OFF / CAUTION)
    2. Soil Moisture Health Status
    3. Fungal Microclimate Risk Level
    4. NPK Soil Fertility Status
    5. Actionable Farm Advisory
    """
    # 1. Irrigation Decision Logic based on Volumetric Soil Moisture %
    if soil_moisture < 30.0:
        valve_status = "ACTIVATED (ON)"
        valve_color = "error" # Red in Streamlit
        moisture_status = "Severely Dry / Wilting Point"
        irrigation_action = "🚨 Irrigation Solenoid Valve OPENED: Pumping water until soil reaches 50% field capacity."
    elif 30.0 <= soil_moisture <= 65.0:
        valve_status = "STANDBY (OFF)"
        valve_color = "success" # Green
        moisture_status = "Optimal Field Capacity"
        irrigation_action = "✅ Soil hydration is in the ideal range. No irrigation required. Conserving water."
    else:
        valve_status = "STANDBY (OFF)"
        valve_color = "warning" # Yellow/Orange
        moisture_status = "Waterlogged / Oversaturated"
        irrigation_action = "⚠️ Soil is oversaturated (>65%). Stop all irrigation. Check field drainage to avoid root rot."

    # 2. Disease / Fungal Weather Risk Matrix
    # High humidity (>80%) + warm temperature (22 - 32 C) accelerates fungal spores (e.g. Blight, Mildew)
    if humidity >= 80.0 and (22.0 <= temperature <= 32.0):
        disease_risk = "HIGH (Fungal Spore Outbreak Risk)"
        disease_risk_alert = "Warm temperatures combined with high humidity create ideal conditions for fungal pathogens (Blight/Rust). Inspect foliage and avoid overhead irrigation."
    elif humidity >= 70.0 and temperature > 32.0:
        disease_risk = "MODERATE (Heat & Moisture Stress)"
        disease_risk_alert = "Crop canopy is under elevated evapotranspiration stress. Ensure morning moisture levels are sufficient."
    else:
        disease_risk = "LOW (Microclimate Stable)"
        disease_risk_alert = "Environmental microclimate parameters are balanced and do not favor rapid fungal sporulation."

    # 3. NPK Nutrient Evaluation (Target baseline kg/ha)
    # Typical balanced crop targets: N: 60-140, P: 30-70, K: 30-80
    npk_status = []
    if nitrogen < 50:
        npk_status.append("Low Nitrogen (N) ➡️ Risk of stunted vegetative growth and yellowing older leaves. Add urea or blood meal.")
    elif nitrogen > 150:
        npk_status.append("Excess Nitrogen (N) ➡️ Promotes lush, disease-susceptible foliage. Cut back nitrogen feeding.")
    else:
        npk_status.append("Optimal Nitrogen (N) Level.")

    if phosphorus < 25:
        npk_status.append("Low Phosphorus (P) ➡️ Weak root structure and delayed flowering. Apply rock phosphate or bone meal.")
    else:
        npk_status.append("Adequate Phosphorus (P) Level.")

    if potassium < 25:
        npk_status.append("Low Potassium (K) ➡️ Reduced drought resistance and weak stems. Apply potash.")
    else:
        npk_status.append("Adequate Potassium (K) Level.")

    return {
        "valve_status": valve_status,
        "valve_color": valve_color,
        "moisture_status": moisture_status,
        "irrigation_action": irrigation_action,
        "disease_risk": disease_risk,
        "disease_risk_alert": disease_risk_alert,
        "npk_advisory": npk_status
    }

