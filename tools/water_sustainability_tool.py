"""
AgriSustain AI — Water Sustainability Advisor Tool
Provides water-management guidance based on crop and availability inputs.
Aligned with SDG 6 (Clean Water and Sanitation).
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def assess_water_sustainability(
    crop: str,
    water_availability: str,
    soil_type: str = "",
    irrigation_method: str = "",
    season: str = "",
) -> dict:
    """
    Assesses water sustainability requirements for a given crop and context.
    Returns water-management guidance and conservation recommendations.

    Args:
        crop: The crop being grown.
        water_availability: Water availability level: low, medium, or high.
        soil_type: The soil type (optional, affects water retention).
        irrigation_method: Type of irrigation used, e.g. drip, flood, sprinkler (optional).
        season: The growing season (optional).

    Returns:
        A dictionary with water sustainability guidance.
    """
    water_level = water_availability.lower() if water_availability else "unknown"

    guidance = {
        "crop": crop,
        "water_availability": water_level,
        "soil_type": soil_type or "Not specified",
        "irrigation_method": irrigation_method or "Not specified",
        "season": season or "Not specified",
        "recommendations": [],
        "conservation_tips": [],
        "risk_level": "moderate",
    }

    if water_level == "low":
        guidance["risk_level"] = "high"
        guidance["recommendations"] = [
            "Prioritize drought-tolerant crop varieties.",
            "Use drip or micro-irrigation to minimize water loss.",
            "Mulch around plants to retain soil moisture.",
            "Monitor soil moisture regularly to avoid over- or under-irrigation.",
            "Consider rainwater harvesting if feasible.",
        ]
        guidance["conservation_tips"] = [
            "Irrigate during early morning or late evening to reduce evaporation.",
            "Avoid irrigation on windy days.",
            "Use soil moisture sensors or simple finger-test to check moisture levels.",
        ]
    elif water_level == "medium":
        guidance["risk_level"] = "moderate"
        guidance["recommendations"] = [
            "Follow crop-stage-based irrigation scheduling.",
            "Avoid irrigation when rainfall is expected.",
            "Consider furrow or sprinkler irrigation for efficiency.",
        ]
        guidance["conservation_tips"] = [
            "Combine organic matter into soil to improve water retention.",
            "Maintain field bunds to reduce runoff.",
        ]
    elif water_level == "high":
        guidance["risk_level"] = "low"
        guidance["recommendations"] = [
            "Ensure adequate field drainage to prevent waterlogging.",
            "Avoid excess irrigation that could leach nutrients.",
        ]
        guidance["conservation_tips"] = [
            "Monitor for waterlogging, especially in clay or low-lying soils.",
            "Avoid applying fertilizers just before or after heavy rain.",
        ]

    guidance["note"] = (
        "These are general water-management principles. "
        "Local agricultural extension guidance should be consulted for site-specific recommendations."
    )

    return guidance
