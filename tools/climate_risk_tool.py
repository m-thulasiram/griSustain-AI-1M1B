"""
AgriSustain AI — Climate and Weather Risk Tool
Provides general climate risk information for agricultural planning.
Aligned with SDG 13 (Climate Action).
NOTE: This tool uses general knowledge only. It does NOT provide live weather data
unless a live weather API tool is actually connected.
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def assess_climate_risk(
    location: str,
    crop: str,
    season: str = "",
    reported_conditions: str = "",
) -> dict:
    """
    Provides general climate-risk considerations for agricultural planning.
    This tool uses general agricultural knowledge only — it does NOT access
    live weather data. Users should verify current conditions from official sources.

    Args:
        location: The location or region of the farm.
        crop: The crop being considered.
        season: The growing season or month (optional).
        reported_conditions: Any weather conditions described by the user (optional).

    Returns:
        A dictionary with climate risk considerations and caveats.
    """
    risk_assessment = {
        "location": location,
        "crop": crop,
        "season": season or "Not specified",
        "reported_conditions": reported_conditions or "Not provided",
        "data_source": "General agricultural knowledge — NOT live weather data",
        "live_weather_available": False,
        "general_risks": [],
        "mitigation_guidance": [],
        "important_caveat": (
            "Live weather data is not currently connected to this system. "
            "The information below is based on general agricultural knowledge only. "
            "Please check current weather forecasts from your local meteorological service "
            "before making farm management decisions."
        ),
    }

    risk_assessment["general_risks"] = [
        "Excess or unseasonal rainfall can cause waterlogging, fungal disease, and nutrient leaching.",
        "Dry spells or drought can stress crops, particularly at flowering and grain-fill stages.",
        "High temperatures above crop-specific thresholds can reduce yield.",
        "Cold nights or unexpected frost can damage sensitive crops.",
        "High humidity increases the risk of fungal diseases such as late blight, powdery mildew, and rust.",
        "Strong winds can cause lodging in tall cereals and physical crop damage.",
    ]

    risk_assessment["mitigation_guidance"] = [
        "Plan sowing dates to align critical crop stages with favorable weather windows.",
        "Maintain field drainage to reduce waterlogging risk.",
        "Use windbreaks or shelter crops in high-wind areas.",
        "Select climate-resilient or locally adapted crop varieties where available.",
        "Monitor crop conditions regularly and adjust irrigation and management accordingly.",
        "Keep a weather diary or use a free weather app to track local conditions.",
    ]

    if reported_conditions:
        risk_assessment["user_reported_note"] = (
            f"You reported: '{reported_conditions}'. "
            "This has been noted but cannot be independently verified by this system. "
            "Please consult a local agricultural expert for site-specific guidance."
        )

    return risk_assessment
