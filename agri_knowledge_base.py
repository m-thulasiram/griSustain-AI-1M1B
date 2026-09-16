"""
AgriSustain AI — Agricultural Knowledge Base
A structured in-process RAG knowledge base organized into seven categories.
All content is general agricultural guidance. No live data. No fabricated statistics.

Categories:
  1. Crop Management
  2. Water Management
  3. Sustainable Farming
  4. Crop Health
  5. Climate Risk
  6. Soil Health
  7. Integrated Pest Management (IPM)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


# ──────────────────────────────────────────────────────────────────────────────
# DATA MODEL
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class KnowledgeEntry:
    """A single knowledge document in the agricultural knowledge base."""
    doc_id: str
    category: str
    title: str
    content: str
    keywords: List[str] = field(default_factory=list)
    source_label: str = "AgriSustain Knowledge Base"


@dataclass
class RetrievalResult:
    """A retrieved knowledge entry with a relevance score."""
    entry: KnowledgeEntry
    score: float
    matched_keywords: List[str]


# ──────────────────────────────────────────────────────────────────────────────
# KNOWLEDGE DOCUMENTS
# ──────────────────────────────────────────────────────────────────────────────

KNOWLEDGE_DOCUMENTS: List[KnowledgeEntry] = [

    # ── CROP MANAGEMENT ─────────────────────────────────────────────────────

    KnowledgeEntry(
        doc_id="CM-001",
        category="Crop Management",
        title="Groundnut Crop Management — General Principles",
        content=(
            "Groundnut (Arachis hypogaea) is a warm-season legume well suited to "
            "sandy loam or red loam soils with good drainage. It requires a warm "
            "climate with temperatures between 25–35°C during the growing season. "
            "Sowing should be done when soil temperature is consistently above 18°C. "
            "Spacing is typically 30 cm between rows and 10 cm between plants. "
            "Groundnut fixes atmospheric nitrogen through root nodules, reducing "
            "fertilizer nitrogen needs. It is moderately drought-tolerant after "
            "establishment but requires adequate moisture at flowering and pod formation. "
            "Harvest should be done before excessive rains to prevent aflatoxin risk."
        ),
        keywords=["groundnut", "arachis hypogaea", "peanut", "legume", "sandy loam",
                  "red soil", "nitrogen fixation", "pod", "aflatoxin"],
    ),

    KnowledgeEntry(
        doc_id="CM-002",
        category="Crop Management",
        title="Rice Crop Management — General Principles",
        content=(
            "Rice (Oryza sativa) is the most widely grown cereal crop in Asia. "
            "It is primarily grown in flooded (paddy) conditions, though aerobic "
            "and direct-seeded rice systems are used where water is limited. "
            "Transplanting is the traditional method; direct seeding reduces water "
            "and labor use. Optimal growing temperature is 20–35°C. "
            "Heavy soils with low permeability are suitable for flooded rice. "
            "Key growth stages are tillering, panicle initiation, flowering, "
            "and grain filling. Waterlogging during the ripening stage can reduce "
            "yield and grain quality. Straw should be incorporated or composted "
            "rather than burned to protect soil health."
        ),
        keywords=["rice", "paddy", "oryza sativa", "transplanting", "direct seeding",
                  "flooded", "grain filling", "tillering", "straw"],
    ),

    KnowledgeEntry(
        doc_id="CM-003",
        category="Crop Management",
        title="Wheat Crop Management — General Principles",
        content=(
            "Wheat (Triticum aestivum) is a cool-season cereal grown during the "
            "winter or rabi season in tropical and subtropical regions. "
            "It requires cool temperatures (15–22°C) during vegetative growth and "
            "warm, dry conditions for grain filling and harvest. "
            "Wheat is sensitive to frost at flowering and to waterlogging at any stage. "
            "Sowing depth is typically 5–7 cm. Row spacing is 20–25 cm. "
            "Timely sowing (matching the local recommended window) is critical for "
            "yield. Late sowing reduces both grain weight and number. "
            "Wheat performs best in well-drained loamy soils with neutral to mildly "
            "alkaline pH (6.5–7.5)."
        ),
        keywords=["wheat", "triticum", "rabi", "winter crop", "cool season", "grain",
                  "loamy", "frost", "sowing depth"],
    ),

    KnowledgeEntry(
        doc_id="CM-004",
        category="Crop Management",
        title="Cotton Crop Management — General Principles",
        content=(
            "Cotton (Gossypium hirsutum) is a warm-season cash crop requiring a "
            "long frost-free growing period of 150–180 days. "
            "It grows best in deep, well-drained sandy loam to clay loam soils. "
            "Optimal temperature during boll development is 25–35°C. "
            "Cotton is moderately drought-tolerant but requires adequate moisture "
            "during flowering and boll filling. Excessive moisture causes boll rot. "
            "Integrated pest management is essential as cotton is highly susceptible "
            "to bollworm, aphid, whitefly, and thrips damage. "
            "Bt cotton varieties reduce bollworm pressure but require standard scouting."
        ),
        keywords=["cotton", "gossypium", "boll", "bollworm", "bt cotton", "cash crop",
                  "clay loam", "frost free", "whitefly", "aphid"],
    ),

    KnowledgeEntry(
        doc_id="CM-005",
        category="Crop Management",
        title="Maize Crop Management — General Principles",
        content=(
            "Maize (Zea mays) is a warm-season cereal requiring temperatures of "
            "18–35°C. It is grown as a kharif (monsoon) crop in South Asia. "
            "Maize is very sensitive to waterlogging, especially in the first "
            "4 weeks after sowing. Well-drained loamy soils are ideal. "
            "Sowing depth is 3–5 cm; row spacing 60–75 cm; plant spacing 20–25 cm. "
            "Maize has a high water requirement but is efficient when irrigation is "
            "timed to critical growth stages: germination, knee-high stage, "
            "tasseling, and grain filling. "
            "Crop rotation with legumes improves soil nitrogen for subsequent maize crops."
        ),
        keywords=["maize", "corn", "zea mays", "kharif", "monsoon", "waterlogging",
                  "tasseling", "grain filling", "row spacing", "rotation"],
    ),

    # ── WATER MANAGEMENT ────────────────────────────────────────────────────

    KnowledgeEntry(
        doc_id="WM-001",
        category="Water Management",
        title="Drip Irrigation for Water Efficiency",
        content=(
            "Drip irrigation delivers water directly to the root zone of plants "
            "through a network of pipes, tubes, and emitters. "
            "It reduces water use by 30–50% compared to flood irrigation while "
            "maintaining or improving crop yields. "
            "Drip systems reduce foliar wetness, lowering fungal disease risk. "
            "They are suitable for row crops, orchards, vegetables, and cotton. "
            "Regular maintenance — flushing laterals, checking emitters — prevents "
            "clogging. Fertigation (applying fertilizer through drip) improves "
            "nutrient efficiency. Drip irrigation is most beneficial under low "
            "to medium water availability."
        ),
        keywords=["drip irrigation", "micro irrigation", "emitter", "fertigation",
                  "water efficiency", "root zone", "clogging", "flush"],
    ),

    KnowledgeEntry(
        doc_id="WM-002",
        category="Water Management",
        title="Rainwater Harvesting for Agriculture",
        content=(
            "Rainwater harvesting collects and stores rainfall for agricultural use. "
            "Methods include farm ponds, check dams, percolation tanks, and "
            "contour bunds. Farm ponds can store runoff from surrounding fields "
            "and be used for supplemental irrigation during dry spells. "
            "Even small farm ponds of 0.1–0.5 hectares can provide critical "
            "irrigation water at flowering or grain-fill stages. "
            "Location and design should follow local topography and soil permeability. "
            "Harvested water should be covered or treated if used for drinking. "
            "Rainwater harvesting is particularly valuable in low-rainfall regions "
            "and supports SDG 6 (Clean Water and Sanitation)."
        ),
        keywords=["rainwater harvesting", "farm pond", "check dam", "contour bund",
                  "runoff", "percolation", "supplemental irrigation", "dry spell"],
    ),

    KnowledgeEntry(
        doc_id="WM-003",
        category="Water Management",
        title="Mulching to Reduce Water Loss",
        content=(
            "Mulching is the practice of covering soil with organic or inorganic "
            "material to reduce evaporation, moderate soil temperature, and suppress "
            "weeds. Organic mulches include straw, crop residue, leaves, and compost. "
            "Plastic mulch (polyethylene film) is used for vegetables and fruit crops. "
            "Mulching can reduce evapotranspiration losses by 20–40% in hot, dry "
            "conditions. It also improves soil moisture retention and can reduce "
            "irrigation frequency. Organic mulches improve soil organic matter as "
            "they decompose. Mulch should be applied at a depth of 5–10 cm for "
            "effective moisture conservation."
        ),
        keywords=["mulch", "mulching", "evaporation", "soil moisture", "straw mulch",
                  "plastic mulch", "polyethylene", "evapotranspiration", "weed"],
    ),

    KnowledgeEntry(
        doc_id="WM-004",
        category="Water Management",
        title="Irrigation Scheduling by Crop Stage",
        content=(
            "Irrigation should be timed to match critical crop growth stages when "
            "water stress has the greatest impact on yield. "
            "For most crops, critical stages are: germination and emergence, "
            "vegetative establishment, flowering and pollination, and grain/fruit filling. "
            "Over-irrigation at non-critical stages wastes water and can cause "
            "waterlogging and nutrient leaching. "
            "A simple soil moisture check (finger test: 5 cm depth) can guide "
            "irrigation timing without specialized equipment. "
            "Soil feels dry and crumbles when irrigation is needed; moist and "
            "cool when water is adequate."
        ),
        keywords=["irrigation scheduling", "irrigate", "irrigation timing", "critical stage",
                  "germination", "flowering", "grain filling", "finger test",
                  "waterlogging", "nutrient leaching", "save water", "water saving"],
    ),

    KnowledgeEntry(
        doc_id="WM-005",
        category="Water Management",
        title="Deficit Irrigation for Water-Scarce Conditions",
        content=(
            "Deficit irrigation intentionally applies less water than full "
            "evapotranspiration demand, accepting some yield reduction to save "
            "significant amounts of water. "
            "This strategy is used when water supply is limited. "
            "The principle is to ensure adequate water at the most sensitive "
            "growth stages (flowering, grain fill) while accepting slight stress "
            "at other stages. "
            "Drought-tolerant varieties perform better under deficit irrigation. "
            "Deficit irrigation can achieve 60–70% of full yield with 40–50% "
            "less water in many crops. It must be paired with improved soil "
            "organic matter to buffer the reduced water supply."
        ),
        keywords=["deficit irrigation", "water scarce", "drought tolerance", "yield reduction",
                  "evapotranspiration", "sensitive stage", "water saving"],
    ),

    # ── SUSTAINABLE FARMING ──────────────────────────────────────────────────

    KnowledgeEntry(
        doc_id="SF-001",
        category="Sustainable Farming",
        title="Crop Rotation for Soil Health and Pest Management",
        content=(
            "Crop rotation is the practice of growing different crops sequentially "
            "on the same land. Rotating cereals with legumes restores soil nitrogen "
            "naturally, reducing the need for synthetic fertilizers. "
            "Rotation breaks pest and disease cycles specific to individual crops. "
            "A three-crop rotation (e.g., rice–wheat–legume or maize–soybean–wheat) "
            "improves both soil biology and farm sustainability. "
            "Monoculture (continuous single-crop farming) depletes specific nutrients "
            "and increases soil-borne disease pressure over time. "
            "Rotation should be planned based on local climate, soil type, and market."
        ),
        keywords=["crop rotation", "legume", "cereal", "monoculture", "nitrogen",
                  "soil biology", "disease cycle", "rotation planning"],
    ),

    KnowledgeEntry(
        doc_id="SF-002",
        category="Sustainable Farming",
        title="Composting Agricultural Waste",
        content=(
            "Composting converts crop residues, animal manure, and food waste into "
            "nutrient-rich organic matter that improves soil structure and fertility. "
            "A basic compost heap requires carbon-rich materials (straw, dry leaves), "
            "nitrogen-rich materials (fresh manure, green vegetation), moisture, "
            "and aeration through turning. "
            "Compost matures in 6–12 weeks depending on conditions. "
            "Applied at 2–5 tonnes per hectare, compost improves water retention, "
            "soil biology, and reduces the need for synthetic fertilizers. "
            "Burning crop residues should be avoided as it destroys organic matter, "
            "reduces soil carbon, and contributes to air pollution."
        ),
        keywords=["compost", "composting", "organic matter", "crop residue", "manure",
                  "soil fertility", "carbon", "nitrogen", "burning residue"],
    ),

    KnowledgeEntry(
        doc_id="SF-003",
        category="Sustainable Farming",
        title="Reduced Tillage and Conservation Agriculture",
        content=(
            "Conservation agriculture is based on three principles: minimal soil "
            "disturbance (zero or minimum tillage), permanent soil cover (mulch, "
            "cover crops, crop residues), and crop diversification through rotation. "
            "Minimum tillage reduces soil erosion, preserves soil structure, "
            "lowers fuel and labour costs, and improves water infiltration. "
            "It is especially beneficial on slopes prone to erosion. "
            "Cover crops protect soil between main crop seasons. "
            "Transition to conservation agriculture may take 2–3 seasons "
            "before full soil health benefits are realized."
        ),
        keywords=["conservation agriculture", "minimum tillage", "zero tillage",
                  "cover crop", "soil erosion", "infiltration", "soil disturbance"],
    ),

    KnowledgeEntry(
        doc_id="SF-004",
        category="Sustainable Farming",
        title="Responsible Fertilizer Use",
        content=(
            "Over-application of synthetic nitrogen fertilizers leads to soil "
            "acidification, nitrate leaching into groundwater, and greenhouse gas "
            "emissions (nitrous oxide). "
            "Fertilizer should be applied based on soil test results where possible. "
            "Split application — dividing the total dose into two or three applications "
            "during the growing season — improves nutrient use efficiency and "
            "reduces loss. Incorporating organic matter before chemical fertilizers "
            "reduces the total quantity needed. "
            "Farmers should follow the 4R principle: Right Source, Right Rate, "
            "Right Time, Right Place of application."
        ),
        keywords=["fertilizer", "nitrogen", "split application", "soil test", "4R",
                  "nitrate leaching", "acidification", "nutrient efficiency"],
    ),

    # ── CROP HEALTH ─────────────────────────────────────────────────────────

    KnowledgeEntry(
        doc_id="CH-001",
        category="Crop Health",
        title="Leaf Yellowing: Common Causes and Initial Assessment",
        content=(
            "Leaf yellowing (chlorosis) in crops can result from multiple causes: "
            "nitrogen deficiency (older leaves yellow first, starting from leaf tip), "
            "iron deficiency (young leaves yellow while veins stay green — interveinal "
            "chlorosis), magnesium deficiency (older leaves yellow between veins), "
            "waterlogging (roots deprived of oxygen, leaves yellowing progressively), "
            "or early viral/fungal infection. "
            "Assessment should consider: which leaves are affected first (old or young), "
            "the pattern of yellowing (uniform, interveinal, tip, or whole leaf), "
            "soil conditions (waterlogged or dry), and recent management. "
            "Symptoms alone cannot provide a definitive diagnosis — field inspection "
            "and if necessary a soil test or laboratory analysis is recommended."
        ),
        keywords=["yellowing", "chlorosis", "nitrogen deficiency", "iron deficiency",
                  "magnesium", "interveinal", "waterlogging", "leaf", "diagnostic"],
    ),

    KnowledgeEntry(
        doc_id="CH-002",
        category="Crop Health",
        title="Fungal Diseases: Recognition and Precautionary Management",
        content=(
            "Common fungal diseases include powdery mildew (white powdery coating on "
            "leaves), downy mildew (grey/purple growth on leaf undersides), rust "
            "(orange-brown pustules on leaves), late blight (dark water-soaked lesions "
            "on leaves, white sporulation at lesion edge in humid conditions), and "
            "leaf spot diseases (brown or black spots with or without yellow halos). "
            "Favourable conditions for most fungal diseases: high humidity (>80%), "
            "warm temperatures (15–28°C), and dense canopy with poor airflow. "
            "Precautionary practices include: selecting resistant varieties, ensuring "
            "good plant spacing, avoiding overhead irrigation, removing infected plant "
            "material, and practicing crop rotation. "
            "Fungicide use should be based on confirmed identification and follow "
            "product label instructions. Avoid blanket preventive sprays."
        ),
        keywords=["fungal disease", "powdery mildew", "downy mildew", "rust", "late blight",
                  "leaf spot", "humidity", "sporulation", "lesion", "fungicide"],
    ),

    KnowledgeEntry(
        doc_id="CH-003",
        category="Crop Health",
        title="Wilting: Water Stress vs. Soil-borne Disease",
        content=(
            "Plant wilting can result from two very different causes that require "
            "different responses. Water stress wilting occurs when soil moisture is "
            "insufficient; leaves wilt during the hottest part of the day and "
            "recover at night when temperatures drop. Irrigating will resolve this. "
            "Fusarium or Verticillium wilt is a soil-borne fungal disease that "
            "blocks water-conducting vessels. Affected plants wilt progressively "
            "and do not recover with irrigation. Cross-sectioning the stem may "
            "reveal brown discolouration of vascular tissue. "
            "Bacterial wilt (common in solanaceous crops) also causes rapid, "
            "permanent wilting. A simple field test: cut the stem and immerse "
            "in water; bacterial ooze indicates bacterial wilt. "
            "Soil-borne wilt diseases have no curative chemical treatment; "
            "crop rotation and resistant varieties are the primary management tools."
        ),
        keywords=["wilting", "water stress", "fusarium wilt", "verticillium", "bacterial wilt",
                  "vascular", "stem", "soil-borne", "ooze", "resistant variety"],
    ),

    KnowledgeEntry(
        doc_id="CH-004",
        category="Crop Health",
        title="Insect Pest Damage: Visual Recognition",
        content=(
            "Common patterns of insect damage: "
            "Holes in leaves with ragged edges — caterpillars or beetles. "
            "Tiny stippling or silver streaks on leaves — thrips or mites. "
            "Curled, distorted leaves and sticky honeydew — aphids or whiteflies. "
            "Stem borers tunnel into stems; affected stems may break or show dead hearts. "
            "Leaf miners create winding tunnels inside leaves. "
            "Scouting (regular field inspection) is essential for early detection. "
            "Economic threshold — the pest population level at which damage is likely "
            "to exceed the cost of control — should guide the decision to treat. "
            "Not all insect presence requires immediate pesticide application."
        ),
        keywords=["insect damage", "caterpillar", "beetle", "thrips", "mite", "aphid",
                  "whitefly", "stem borer", "leaf miner", "scouting", "economic threshold"],
    ),

    # ── CLIMATE RISK ─────────────────────────────────────────────────────────

    KnowledgeEntry(
        doc_id="CR-001",
        category="Climate Risk",
        title="Drought Risk Management in Agriculture",
        content=(
            "Drought is one of the most significant climate risks for agriculture. "
            "Short-term drought (1–4 weeks) at critical stages (flowering, grain fill) "
            "can cause significant yield loss. Long-term drought may cause total crop failure. "
            "Strategies to reduce drought risk include: selecting drought-tolerant "
            "varieties, improving soil organic matter to increase water-holding capacity, "
            "mulching to reduce evaporation, using deficit irrigation strategically "
            "at critical growth stages, and growing shorter-duration varieties that "
            "complete their life cycle before the dry season intensifies. "
            "Rainwater harvesting and farm ponds can buffer against short dry spells. "
            "Diversifying crops across the season reduces overall farm risk from drought."
        ),
        keywords=["drought", "water stress", "drought tolerant", "yield loss", "dry season",
                  "water holding capacity", "short duration variety", "diversify"],
    ),

    KnowledgeEntry(
        doc_id="CR-002",
        category="Climate Risk",
        title="Flood and Waterlogging Risk in Crops",
        content=(
            "Flooding or waterlogging deprives plant roots of oxygen, causing rapid "
            "wilting, yellowing, and death if prolonged. Most upland crops can tolerate "
            "only 24–72 hours of waterlogging before suffering serious damage. "
            "Rice is the main exception as it is adapted to flooded conditions. "
            "Risk management includes: maintaining good field drainage, creating "
            "raised beds for sensitive crops, ensuring field bunds do not trap excess "
            "water, and planting flood-tolerant varieties where flooding is expected. "
            "After a flood event, assess root damage, apply a light nitrogen "
            "fertilizer to support recovery, and watch for fungal diseases "
            "encouraged by wet conditions."
        ),
        keywords=["flood", "flooded", "flooding", "waterlogging", "drainage", "raised bed",
                  "field bund", "oxygen", "submergence", "recovery", "root damage"],
    ),

    KnowledgeEntry(
        doc_id="CR-003",
        category="Climate Risk",
        title="Heat Stress in Crops",
        content=(
            "Heat stress occurs when temperatures exceed a crop's optimal range, "
            "typically above 35–38°C for most crops. At flowering, high temperatures "
            "can cause pollen sterility, reducing grain set. "
            "Heat-stressed crops show symptoms such as leaf curling (to reduce "
            "surface area), early leaf senescence, and poor grain/fruit set. "
            "Risk management includes: sowing at the recommended time to avoid "
            "heat at critical stages, using varieties with heat tolerance, "
            "maintaining adequate soil moisture (drought + heat combined causes "
            "the most damage), and applying light irrigation during the hottest "
            "part of the day in severe cases."
        ),
        keywords=["heat stress", "high temperature", "pollen sterility", "grain set",
                  "leaf curling", "senescence", "heat tolerance", "flowering"],
    ),

    # ── SOIL HEALTH ──────────────────────────────────────────────────────────

    KnowledgeEntry(
        doc_id="SH-001",
        category="Soil Health",
        title="Soil Organic Matter and Its Importance",
        content=(
            "Soil organic matter (SOM) is the fraction of soil that consists of "
            "decomposed plant and animal material. It improves soil structure, "
            "water-holding capacity, nutrient supply, and biological activity. "
            "SOM levels are typically 1–5% in productive agricultural soils. "
            "Practices that build SOM: incorporating crop residues, adding compost "
            "or manure, using cover crops, and reducing tillage. "
            "Burning crop residues and intensive tillage both reduce SOM. "
            "Each 1% increase in SOM increases the soil's water-holding capacity "
            "by approximately 20,000 litres per hectare — a significant drought buffer."
        ),
        keywords=["soil organic matter", "SOM", "humus", "water holding capacity",
                  "compost", "crop residue", "soil structure", "tillage", "cover crop"],
    ),

    KnowledgeEntry(
        doc_id="SH-002",
        category="Soil Health",
        title="Soil pH and Nutrient Availability",
        content=(
            "Soil pH measures the acidity or alkalinity of the soil on a scale of "
            "0–14. Most crops prefer a slightly acidic to neutral pH of 6.0–7.0. "
            "At pH below 5.5, aluminium and manganese become soluble and toxic "
            "to most crops. At pH above 7.5, iron, manganese, zinc, and boron "
            "become less available. Soil pH can be raised (limed) with agricultural "
            "lime (calcium carbonate) and lowered with sulphur or acidic organic "
            "matter. Soil testing is the only reliable way to determine pH and "
            "nutrient status before applying amendments."
        ),
        keywords=["soil pH", "acidity", "alkalinity", "lime", "acidic", "aluminium toxicity",
                  "nutrient availability", "soil test", "zinc", "iron"],
    ),

    # ── INTEGRATED PEST MANAGEMENT ───────────────────────────────────────────

    KnowledgeEntry(
        doc_id="IPM-001",
        category="Integrated Pest Management",
        title="IPM Principles for Sustainable Crop Protection",
        content=(
            "Integrated Pest Management (IPM) is an ecosystem-based approach that "
            "combines multiple pest management strategies to reduce pesticide use "
            "while maintaining effective crop protection. "
            "IPM hierarchy: "
            "1. Prevention — use resistant varieties, crop rotation, clean seed. "
            "2. Monitoring — regular field scouting to detect pests early. "
            "3. Action threshold — treat only when pest levels exceed the economic threshold. "
            "4. Biological control — encourage natural enemies (parasitic wasps, "
            "   ladybirds, predatory beetles). "
            "5. Cultural controls — adjust planting dates, spacing, irrigation "
            "   to reduce pest-favourable conditions. "
            "6. Chemical control — as a last resort, using the least toxic, "
            "   most selective product available. "
            "IPM reduces chemical residues in food, protects beneficial insects, "
            "and lowers long-term resistance development in pests."
        ),
        keywords=["IPM", "integrated pest management", "scouting", "biological control",
                  "economic threshold", "resistant variety", "natural enemy", "pesticide"],
    ),

    KnowledgeEntry(
        doc_id="IPM-002",
        category="Integrated Pest Management",
        title="Pesticide Safety and Responsible Use",
        content=(
            "Pesticides must be used responsibly and only when necessary. "
            "Always read and follow the product label — the label is the law. "
            "Key safety principles: "
            "Use the correct dose — under-dosing promotes resistance; over-dosing "
            "increases residue and environmental harm. "
            "Apply at the correct time — early morning or late evening to protect "
            "pollinators. "
            "Use personal protective equipment (PPE): gloves, mask, goggles, and "
            "coveralls. "
            "Observe the pre-harvest interval (PHI) — the minimum number of days "
            "between the last pesticide application and harvest. "
            "Never apply pesticides near water bodies, during strong wind, or "
            "at flowering when pollinators are active. "
            "Do not invent or follow unverified dosage rates. Consult the product "
            "label and local agricultural extension service."
        ),
        keywords=["pesticide", "safety", "label", "dose", "PHI", "pre-harvest interval",
                  "PPE", "resistance", "pollinator", "extension"],
    ),
]


# ──────────────────────────────────────────────────────────────────────────────
# RETRIEVAL ENGINE
# ──────────────────────────────────────────────────────────────────────────────
 
# Generic English words that appear in KB content but carry no agricultural signal.
# Queries that match ONLY these words should not trigger retrieval.
_STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "i", "my", "me", "we", "you", "he", "she", "it", "they", "them",
    "what", "when", "where", "which", "who", "how", "why",
    "can", "could", "will", "would", "should", "may", "might", "do", "does",
    "this", "that", "these", "those", "with", "from", "for", "and", "or",
    "not", "no", "yes", "to", "of", "in", "on", "at", "by", "up",
    "tell", "give", "show", "help", "please", "want", "need", "know",
    "today", "yesterday", "current", "now", "exact", "definitely", "certainly",
    "access", "your", "our", "their", "its", "has", "have", "had",
    "password", "price", "cost", "fee", "pay", "bank", "money",
    "image", "photo", "picture", "analyze", "analysis", "video",
    "weather", "temperature", "forecast",  # weather-only terms (no agri KB docs)
}


def _tokenize(text: str) -> List[str]:
    """Lower-case, strip punctuation, split into tokens. Excludes stop words."""
    return [t for t in re.findall(r"[a-z]+", text.lower()) if t not in _STOP_WORDS]


def retrieve(query: str, top_k: int = 3, min_score: float = 2.0) -> List[RetrievalResult]:
    """
    Keyword-overlap retrieval over the knowledge base.
    Scores each document by the number of query tokens that match its keywords
    or appear in its content. Stop words are excluded from scoring.

    A minimum score of 2 requires at least one keyword-level match (2 pts)
    or two content-level matches (1 pt each), preventing retrieval on
    generic queries like "what is today's weather?" or "what is the price of rice?".

    Args:
        query: The user's question or topic.
        top_k: Maximum number of documents to return.
        min_score: Minimum relevance score to include a result (default 2).

    Returns:
        A ranked list of RetrievalResult objects, highest score first.
        Returns an empty list if no document meets the minimum score.
    """
    query_tokens = set(_tokenize(query))

    # If no meaningful tokens remain after stop-word removal, skip retrieval
    if not query_tokens:
        return []

    results: List[RetrievalResult] = []

    for entry in KNOWLEDGE_DOCUMENTS:
        # Build searchable token set for this entry
        kw_tokens = set()
        for kw in entry.keywords:
            kw_tokens.update(_tokenize(kw))
        content_tokens = set(_tokenize(entry.content))
        combined = kw_tokens | content_tokens

        matched = query_tokens & combined
        matched_kw_only = query_tokens & kw_tokens

        # Keyword matches are worth 2 points; content-only matches worth 1
        score = len(matched_kw_only) * 2 + len(matched - kw_tokens)

        if score >= min_score:
            results.append(
                RetrievalResult(
                    entry=entry,
                    score=score,
                    matched_keywords=sorted(matched_kw_only),
                )
            )

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:top_k]


def format_retrieved_context(results: List[RetrievalResult]) -> str:
    """
    Format retrieved documents into a text block suitable for injection into
    the Granite prompt as grounded context.
    """
    if not results:
        return ""

    lines = ["--- RETRIEVED AGRICULTURAL KNOWLEDGE ---"]
    for i, r in enumerate(results, 1):
        lines.append(
            f"\n[Source {i}: {r.entry.doc_id} | {r.entry.category} | "
            f"{r.entry.title}]\n{r.entry.content}"
        )
    lines.append("\n--- END OF RETRIEVED KNOWLEDGE ---")
    return "\n".join(lines)


def get_source_citations(results: List[RetrievalResult]) -> List[str]:
    """Return a list of human-readable source citation strings."""
    return [
        f"{r.entry.doc_id} — {r.entry.title} ({r.entry.category})"
        for r in results
    ]
