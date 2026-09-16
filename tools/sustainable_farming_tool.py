"""
AgriSustain AI — Sustainable Farming Advisor Tool
Provides sustainable and resource-efficient farming practice recommendations.
Aligned with SDG 2, SDG 6, SDG 12, SDG 13.
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def get_sustainable_farming_practices(
    crop: str,
    farming_challenge: str = "",
    soil_type: str = "",
    farm_size: str = "",
    region: str = "",
) -> dict:
    """
    Returns sustainable farming practice recommendations relevant to the user's context.
    Prioritizes integrated, resource-efficient, and environmentally responsible approaches.

    Args:
        crop: The crop being farmed.
        farming_challenge: A specific challenge the farmer is facing (optional).
        soil_type: The type of soil on the farm (optional).
        farm_size: The size of the farm, e.g. small, medium, large (optional).
        region: The general geographic region (optional).

    Returns:
        A dictionary with sustainable farming practice recommendations.
    """
    practices = {
        "crop": crop,
        "farming_challenge": farming_challenge or "General sustainable farming",
        "soil_type": soil_type or "Not specified",
        "farm_size": farm_size or "Not specified",
        "region": region or "Not specified",
        "soil_health": [],
        "water_efficiency": [],
        "integrated_pest_management": [],
        "resource_reduction": [],
        "climate_resilience": [],
        "sdg_alignment": [
            "SDG 2 — Zero Hunger: sustainable crop production",
            "SDG 6 — Clean Water: efficient water use and protection",
            "SDG 12 — Responsible Consumption: reducing agricultural waste and inputs",
            "SDG 13 — Climate Action: climate-resilient farming practices",
        ],
    }

    practices["soil_health"] = [
        "Add organic matter (compost, green manure) to improve soil structure and fertility.",
        "Practice crop rotation to break pest and disease cycles and restore soil nutrients.",
        "Minimize tillage where possible to preserve soil structure and moisture.",
        "Use cover crops in the off-season to prevent erosion and improve soil biology.",
        "Avoid overuse of chemical fertilizers — test soil before applying nutrients.",
    ]

    practices["water_efficiency"] = [
        "Use drip irrigation to deliver water directly to the root zone.",
        "Mulch around plants to reduce evaporation.",
        "Harvest rainwater and store it for dry-period use.",
        "Irrigate based on soil moisture readings, not fixed schedules.",
        "Maintain field bunds and contours to reduce water runoff.",
    ]

    practices["integrated_pest_management"] = [
        "Scout fields regularly to detect pests and diseases early.",
        "Use resistant or tolerant crop varieties where available.",
        "Encourage natural predators by maintaining field margins.",
        "Use biological control agents where available and appropriate.",
        "Apply pesticides only as a last resort and follow label instructions carefully.",
    ]

    practices["resource_reduction"] = [
        "Compost crop residues instead of burning them.",
        "Reuse packaging and containers appropriately.",
        "Calibrate equipment to apply precise amounts of inputs.",
        "Track input use and yields to identify waste and inefficiency.",
    ]

    practices["climate_resilience"] = [
        "Diversify crops to reduce risk from single crop failure.",
        "Plant trees or windbreaks to protect soil and crops from extreme weather.",
        "Adjust sowing dates based on local climate trends.",
        "Maintain seed of locally adapted varieties for climate resilience.",
    ]

    return practices
