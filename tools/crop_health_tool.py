"""
AgriSustain AI — Crop Health Assistant Tool
Provides preliminary crop health assessment based on described symptoms.
Aligned with SDG 2 (Zero Hunger) and responsible AI guidelines.
"""

from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def assess_crop_symptoms(
    crop: str,
    symptoms: str,
    affected_part: str = "",
    symptom_spread: str = "",
    recent_weather: str = "",
) -> dict:
    """
    Performs a preliminary assessment of crop health based on user-described symptoms.
    Returns possible categories of issues and recommended safe next steps.
    NOTE: This tool does NOT provide a definitive diagnosis. It supports the user in
    understanding possible issues and seeking expert help if required.

    Args:
        crop: The crop being assessed.
        symptoms: A description of the visible symptoms observed.
        affected_part: The part of the plant affected: leaves, stem, root, fruit, whole plant (optional).
        symptom_spread: How widespread the symptoms are: single plant, patch, whole field (optional).
        recent_weather: Recent weather conditions if known (optional).

    Returns:
        A dictionary with possible issue categories and recommended actions.
    """
    assessment = {
        "crop": crop,
        "symptoms_described": symptoms,
        "affected_part": affected_part or "Not specified",
        "symptom_spread": symptom_spread or "Not specified",
        "recent_weather": recent_weather or "Not specified",
        "possible_categories": [],
        "recommended_actions": [],
        "disclaimer": (
            "This assessment is based solely on the described symptoms. "
            "Symptoms described may be consistent with multiple conditions. "
            "A definitive diagnosis requires physical inspection by a qualified "
            "agricultural professional. Do not apply any chemical treatment based "
            "solely on this assessment."
        ),
    }

    symptoms_lower = symptoms.lower() if symptoms else ""

    if any(w in symptoms_lower for w in ["yellow", "yellowing", "pale", "chlorosis"]):
        assessment["possible_categories"].append(
            "Nutrient deficiency (e.g. nitrogen, iron, magnesium) or early disease symptom"
        )
    if any(w in symptoms_lower for w in ["spot", "lesion", "brown", "black", "rust", "blight"]):
        assessment["possible_categories"].append(
            "Possible fungal or bacterial disease — further inspection required"
        )
    if any(w in symptoms_lower for w in ["wilt", "droop", "limp", "collapse"]):
        assessment["possible_categories"].append(
            "Possible wilting due to water stress, root disease, or vascular infection"
        )
    if any(w in symptoms_lower for w in ["hole", "eaten", "insect", "pest", "bite"]):
        assessment["possible_categories"].append(
            "Possible insect or pest damage — scouting is recommended"
        )
    if any(w in symptoms_lower for w in ["curl", "distort", "mosaic", "wrinkle"]):
        assessment["possible_categories"].append(
            "Possible viral infection or mite/aphid damage — inspect undersides of leaves"
        )

    if not assessment["possible_categories"]:
        assessment["possible_categories"].append(
            "Symptoms are not clearly classifiable from the description alone"
        )

    assessment["recommended_actions"] = [
        "Collect a clear photograph or sample of the affected plant part.",
        "Check nearby plants for similar symptoms.",
        "Consult a local agricultural extension officer or agronomist.",
        "Avoid applying chemical treatments without expert confirmation.",
        "If symptoms are spreading rapidly, isolate affected plants where possible.",
    ]

    return assessment
