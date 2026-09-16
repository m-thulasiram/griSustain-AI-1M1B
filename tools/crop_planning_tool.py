"""
AgriSustain AI — Crop Planning Tool
Extracts and validates crop planning parameters from user input.
Aligned with SDG 2 (Zero Hunger) and SDG 12 (Responsible Consumption).
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def extract_crop_planning_info(
    user_input: str,
    location: str = "",
    crop: str = "",
    variety: str = "",
    soil_type: str = "",
    water_availability: str = "",
    sowing_period: str = "",
    farming_stage: str = "",
) -> dict:
    """
    Extracts and structures crop planning information provided by the user.
    Returns a structured summary of the farming context to guide the AI response.

    Args:
        user_input: The raw natural-language input from the user.
        location: The user's location or region (optional).
        crop: The crop the user intends to grow (optional).
        variety: The crop variety or cultivar (optional).
        soil_type: The type of soil available (optional).
        water_availability: Water availability level: low, medium, or high (optional).
        sowing_period: The planned sowing month or season (optional).
        farming_stage: The current stage: planning, sowing, growing, harvest (optional).

    Returns:
        A structured dictionary with all available crop planning context.
    """
    context = {
        "user_input": user_input,
        "location": location or "Not provided",
        "crop": crop or "Not specified",
        "variety": variety or "Not specified",
        "soil_type": soil_type or "Not provided",
        "water_availability": water_availability or "Not specified",
        "sowing_period": sowing_period or "Not provided",
        "farming_stage": farming_stage or "Not specified",
        "missing_fields": [],
    }

    if not location:
        context["missing_fields"].append("location")
    if not crop:
        context["missing_fields"].append("crop")
    if not water_availability:
        context["missing_fields"].append("water_availability")

    context["ready_for_assessment"] = len(context["missing_fields"]) < 2

    return context
