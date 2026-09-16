"""
AgriSustain AI — Streamlit Frontend
IBM 1M1B Internship Project
Powered by IBM Granite 4 H Small via watsonx.ai

Architecture:
  User → Streamlit UI
       → RAG retrieval (agri_knowledge_base.py)
       → IBM Granite 4 H Small (watsonx.ai)
       → Responsible AI validation (responsible_ai.py)
       → Final response with transparency note
"""

import os
import requests
import streamlit as st

from agri_knowledge_base import retrieve, format_retrieved_context, get_source_citations
from responsible_ai import validate_response, format_validation_warnings

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
IBM_API_KEY = os.environ.get("IBM_API_KEY", "AnVdUFtNgdKL6ajSwTAxjIuJCevD2-CrIGzGim6RP7QN")
PROJECT_ID = os.environ.get("WATSONX_PROJECT_ID", "26d4153a-6c3a-40c2-895e-e3563f47cfba")
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-4-h-small"          # Validated in IBM watsonx Prompt Lab
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

# Keywords that signal the query likely benefits from RAG knowledge retrieval
_RAG_TRIGGER_WORDS = {
    "crop", "crops", "plant", "plants", "grow", "growing", "sow", "seed",
    "soil", "water", "irrigation", "drought", "flood", "rain", "weather",
    "climate", "pest", "disease", "fungal", "insect", "wilt", "yellow",
    "symptom", "leaf", "root", "fertilizer", "nitrogen", "compost",
    "rice", "wheat", "maize", "corn", "cotton", "groundnut", "peanut",
    "sustainable", "ipm", "rotation", "mulch", "harvest", "blight",
}


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are AgriSustain AI, an IBM Granite-powered sustainable agriculture
decision-support assistant. Your purpose is to help farmers, students, and agricultural
learners understand agricultural information and make more informed, resource-efficient decisions.

You are a decision-support system — NOT a replacement for qualified agricultural professionals.

SDG Alignment:
- SDG 2 (Zero Hunger): Sustainable crop planning
- SDG 6 (Clean Water): Responsible water use
- SDG 12 (Responsible Consumption): Responsible agricultural resource use
- SDG 13 (Climate Action): Climate-risk awareness

RESPONSE FORMAT — for agricultural questions, use this structure when relevant:
## 🌱 AgriSustain AI Assessment
### 1. Understanding Your Situation
### 2. Key Factors
### 3. 🌱 Crop Considerations
### 4. 💧 Water Sustainability
### 5. 🌦️ Climate / Weather Considerations
### 6. ♻️ Sustainability Suggestions
### 7. 📋 Recommended Next Steps
### 8. ⚠️ Important Limitation

CORE RULES — follow these without exception:
1. Never claim live weather data. Say: "I do not have access to live weather information in this session."
2. Never claim real-time crop prices, government data, or live databases.
3. Never perform image analysis — this system is text/symptom based only.
4. Never fabricate statistics, citations, yield predictions, dosage rates, or chemical instructions.
5. If the RETRIEVED KNOWLEDGE section is present in this prompt, base your answer on it and cite the source IDs.
6. If no retrieved knowledge is present, clearly state: "This response is based on general agricultural knowledge."
7. Never present uncertain outcomes as guaranteed. Use language like "may", "typically", "depends on".
8. If the user writes in Telugu, respond in Telugu.
9. Use simple, clear language accessible to non-technical users.
10. If important information is missing, ask only the single most important follow-up question.
"""


# ─────────────────────────────────────────────────────────────────────────────
# IBM CLOUD IAM AUTHENTICATION
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3000)
def get_iam_token(api_key: str) -> str:
    """Fetch a short-lived IAM bearer token from IBM Cloud."""
    response = requests.post(
        IAM_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


# ─────────────────────────────────────────────────────────────────────────────
# RAG RETRIEVAL
# ─────────────────────────────────────────────────────────────────────────────
def run_rag(query: str) -> tuple[str, list[str], bool]:
    """
    Run keyword-based RAG retrieval against the agricultural knowledge base.

    Returns:
        (context_block, source_list, retrieved_flag)
        context_block — formatted text to inject into the prompt (empty if nothing found)
        source_list   — list of human-readable citation strings
        retrieved_flag — True if at least one document was retrieved
    """
    # Determine whether this query is likely agricultural (worth searching the KB)
    query_tokens = set(query.lower().split())
    is_agri_query = bool(query_tokens & _RAG_TRIGGER_WORDS)

    if not is_agri_query:
        return "", [], False

    results = retrieve(query, top_k=3, min_score=2.0)
    if not results:
        return "", [], False

    context = format_retrieved_context(results)
    sources = get_source_citations(results)
    return context, sources, True


# ─────────────────────────────────────────────────────────────────────────────
# IBM GRANITE TEXT GENERATION
# ─────────────────────────────────────────────────────────────────────────────
def call_granite(prompt: str) -> str:
    """
    Call IBM Granite 4 H Small via watsonx.ai text generation API.
    Returns the generated text or an error string.
    """
    try:
        token = get_iam_token(IBM_API_KEY)
    except Exception as e:
        return f"⚠️ Authentication error: {e}. Please check your IBM API key."

    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 900,
            "min_new_tokens": 20,
            "stop_sequences": ["<|user|>", "<|system|>"],
            "repetition_penalty": 1.1,
        },
        "project_id": PROJECT_ID,
    }

    try:
        resp = requests.post(
            f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        text = resp.json()["results"][0]["generated_text"].strip()
        # Strip any trailing stop tokens
        for stop in ["<|user|>", "<|system|>", "<|assistant|>"]:
            if text.endswith(stop):
                text = text[: -len(stop)].strip()
        return text
    except requests.exceptions.HTTPError:
        return f"⚠️ API error ({resp.status_code}): {resp.text}"
    except Exception as e:
        return f"⚠️ Error generating response: {e}"


# ─────────────────────────────────────────────────────────────────────────────
# FULL PIPELINE: RAG → GRANITE → RESPONSIBLE AI
# ─────────────────────────────────────────────────────────────────────────────
def generate_response(user_message: str, chat_history: list) -> tuple[str, list[str]]:
    """
    Full AgriSustain AI pipeline:
      1. RAG retrieval from agricultural knowledge base
      2. Prompt assembly with retrieved context
      3. IBM Granite 4 H Small generation
      4. Responsible AI validation
      5. Return annotated response + source citations

    Returns:
        (final_response_text, source_citations_list)
    """
    # ── Step 1: RAG retrieval ────────────────────────────────────────────────
    rag_context, rag_sources, rag_retrieved = run_rag(user_message)

    # ── Step 2: Build prompt ─────────────────────────────────────────────────
    prompt = f"<|system|>\n{SYSTEM_PROMPT}\n"

    if rag_retrieved and rag_context:
        prompt += f"\n{rag_context}\n"

    # Include last 8 conversation turns for context
    for turn in chat_history[-8:]:
        prompt += f"<|{turn['role']}|>\n{turn['content']}\n"

    prompt += f"<|user|>\n{user_message}\n<|assistant|>\n"

    # ── Step 3: Generate with IBM Granite ────────────────────────────────────
    raw_response = call_granite(prompt)

    # If generation failed (error string), return early without validation
    if raw_response.startswith("⚠️"):
        return raw_response, []

    # ── Step 4: Responsible AI validation ────────────────────────────────────
    query_tokens = set(user_message.lower().split())
    query_requires_rag = bool(query_tokens & _RAG_TRIGGER_WORDS)

    validation = validate_response(
        response_text=raw_response,
        rag_was_used=True,
        rag_retrieved=rag_retrieved,
        query_requires_rag=query_requires_rag,
    )

    # ── Step 5: Assemble final response ──────────────────────────────────────
    final = raw_response

    # Append any Responsible AI warnings (safety, certainty, false caps, privacy)
    warnings_block = format_validation_warnings(validation)
    if warnings_block:
        final += warnings_block

    # Append transparency note (always shown)
    if validation.transparency_note:
        final += validation.transparency_note

    return final, rag_sources


# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT APP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="AgriSustain AI",
        page_icon="🌱",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/IBM_logo.svg/200px-IBM_logo.svg.png",
            width=80,
        )
        st.markdown("## 🌱 AgriSustain AI")
        st.markdown(
            "**Sustainable Agriculture Decision-Support**\n\n"
            "Powered by **IBM Granite 4 H Small** · watsonx.ai\n\n"
            "IBM 1M1B Internship Project"
        )
        st.divider()

        st.markdown("**SDG Alignment**")
        st.markdown("🍽️ SDG 2 — Zero Hunger")
        st.markdown("💧 SDG 6 — Clean Water")
        st.markdown("♻️ SDG 12 — Responsible Consumption")
        st.markdown("🌍 SDG 13 — Climate Action")
        st.divider()

        st.markdown("**Features**")
        st.markdown(
            "- 🌾 Crop Planning\n"
            "- 💧 Water Sustainability\n"
            "- 🌦️ Climate Risk (general guidance)\n"
            "- 🌿 Crop Health (symptom-based)\n"
            "- ♻️ Sustainable Practices\n"
            "- 📚 RAG Knowledge Base"
        )
        st.divider()

        st.markdown("**System Capabilities**")
        st.caption("✅ IBM Granite 4 H Small (watsonx.ai)")
        st.caption("✅ RAG agricultural knowledge base")
        st.caption("✅ Responsible AI validation")
        st.caption("❌ Live weather (not connected)")
        st.caption("❌ Real-time crop prices (not connected)")
        st.caption("❌ Image analysis (not connected)")
        st.divider()

        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

        st.caption(
            "⚠️ Decision-support tool only. "
            "Consult local agricultural experts for critical decisions."
        )

    # ── Main Area ─────────────────────────────────────────────────────────────
    st.title("🌱 AgriSustain AI")
    st.markdown(
        "**AI-powered sustainable agriculture decision-support** — crop planning, "
        "water management, crop health, climate risk awareness, and more.\n\n"
        "*Powered by IBM Granite 4 H Small via watsonx.ai*"
    )
    st.divider()

    # ── Initialize chat history ───────────────────────────────────────────────
    if "messages" not in st.session_state:
        st.session_state.messages = []
        greeting = (
            "Hello! I'm **AgriSustain AI**, your sustainable agriculture assistant.\n\n"
            "I can help you with:\n"
            "- 🌾 **Crop Planning** — varieties, soil, season, and sowing guidance\n"
            "- 💧 **Water Sustainability** — efficient irrigation and conservation\n"
            "- 🌦️ **Climate Risk** — general seasonal risk awareness\n"
            "- 🌿 **Crop Health** — understanding plant symptoms (text-based)\n"
            "- ♻️ **Sustainable Practices** — soil health, IPM, resource efficiency\n"
            "- 📚 **Agricultural Knowledge** — backed by my knowledge base\n\n"
            "To get started, tell me:\n"
            "1. What crop are you planning or growing?\n"
            "2. Your location or region\n"
            "3. Any specific challenge or question\n\n"
            "---\n"
            "⚠️ *I do not have access to live weather data, real-time crop prices, "
            "or image analysis in this session. I provide general agricultural "
            "decision-support only.*\n\n"
            "*Powered by IBM Granite 4 H Small · watsonx.ai*"
        )
        st.session_state.messages.append({"role": "assistant", "content": greeting})

    # ── Render chat history ───────────────────────────────────────────────────
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ── Chat input ────────────────────────────────────────────────────────────
    if prompt := st.chat_input("Ask about crops, water, climate, or sustainable farming..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AgriSustain AI is thinking..."):
                history = st.session_state.messages[:-1]
                final_response, sources = generate_response(prompt, history)

            st.markdown(final_response)

            # Show source citations if RAG retrieved anything
            if sources:
                with st.expander("📚 Knowledge Base Sources Used"):
                    for s in sources:
                        st.markdown(f"- {s}")

        st.session_state.messages.append({"role": "assistant", "content": final_response})


if __name__ == "__main__":
    main()
