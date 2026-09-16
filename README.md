# 🌱 AgriSustain AI

**AI-Powered Sustainable Agriculture Decision-Support System**
IBM 1M1B Internship Project · Powered by IBM Granite 4 H Small · watsonx.ai

---

## Overview

> AgriSustain AI is an AI-powered decision-support system that uses IBM Granite, RAG, and agentic AI workflows through watsonx Orchestrate to provide accessible, evidence-based information about crop planning, water sustainability, crop health, climate risks, and sustainable farming practices.

AgriSustain AI supports human decision-making. It does not replace farmers, agricultural officers, agronomists, or other qualified professionals.

### SDG Alignment

| SDG | Focus |
|-----|-------|
| 🍽️ SDG 2 — Zero Hunger | Sustainable crop production and food security |
| 💧 SDG 6 — Clean Water and Sanitation | Responsible and efficient water use |
| ♻️ SDG 12 — Responsible Consumption | Resource-efficient farming practices |
| 🌍 SDG 13 — Climate Action | Climate-resilient agriculture |

---

## Architecture

```
User
  ↓
Streamlit Frontend (app.py)
  ↓
RAG Retrieval (agri_knowledge_base.py)
  ↓
IBM Granite 4 H Small (watsonx.ai)
  ↓
Responsible AI Validation (responsible_ai.py)
  ↓
Explainable Response with Source Citations
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Primary LLM | **IBM Granite 4 H Small** (`ibm/granite-4-h-small`) — validated in IBM watsonx Prompt Lab |
| LLM Platform | IBM watsonx.ai (us-south) |
| Agentic Workflow | watsonx Orchestrate (agent YAML spec) |
| RAG | In-process keyword retrieval — 20 documents, 7 categories |
| Frontend | Streamlit |
| Backend Tools | Python (5 domain tools + 1 RAG tool) |
| Responsible AI | Pattern-based validation layer (5 dimensions) |

---

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| 🌾 Crop Planning | ✅ Working | Location, soil, season, water-aware guidance |
| 💧 Water Sustainability | ✅ Working | Irrigation and water conservation guidance |
| 🌦️ Climate Risk | ✅ Working | General seasonal risk awareness (no live weather) |
| 🌿 Crop Health | ✅ Working | Symptom-based preliminary assessment (text only) |
| ♻️ Sustainable Farming | ✅ Working | Soil health, IPM, resource efficiency |
| 📚 RAG Knowledge Base | ✅ Working | 20 agricultural documents, keyword retrieval |
| 🔒 Responsible AI | ✅ Working | Safety, uncertainty, transparency, privacy checks |
| 🌐 Live Weather | ❌ Not connected | Stated as unavailable — no false claims |
| 💹 Real-time Crop Prices | ❌ Not connected | Stated as unavailable — no false claims |
| 🖼️ Image Analysis | ❌ Not connected | Stated as unavailable — no false claims |

---

## Project Structure

```
AgriSustain_AI/
├── app.py                              # Streamlit frontend + full pipeline
├── agri_knowledge_base.py              # RAG: 20-document knowledge base + retrieval
├── responsible_ai.py                   # Responsible AI validation layer
├── requirements.txt                    # Python dependencies
├── workspace_config.yaml               # watsonx Orchestrate workspace config
│
├── agents/
│   └── agrisustain_ai_agent.yaml       # watsonx Orchestrate agent specification
│
├── tools/
│   ├── crop_planning_tool.py           # Crop planning info extraction
│   ├── water_sustainability_tool.py    # Water sustainability assessment
│   ├── crop_health_tool.py             # Symptom-based crop health assessment
│   ├── climate_risk_tool.py            # Climate risk (general knowledge only)
│   ├── sustainable_farming_tool.py     # Sustainable farming practices
│   └── rag_retrieval_tool.py           # RAG knowledge base retrieval tool
│
├── models/
│   └── granite-agrisustain.yaml        # IBM Granite 4 H Small model config
│
├── knowledge-bases/
│   └── agrisustain_knowledge_base.yaml # Knowledge base specification
│
├── connections/
│   └── watsonx_connection.yaml         # IBM watsonx connection spec
│
└── evaluation/
    ├── test_cases.py                   # Executable evaluation test suite
    ├── evaluation_report.md            # Evaluation report with real results
    └── results.json                    # Actual test execution results
```

---

## RAG Knowledge Base

The knowledge base contains **20 structured agricultural documents** across 7 categories:

| Category | Documents | Topics |
|----------|-----------|--------|
| Crop Management | 5 | Groundnut, rice, wheat, cotton, maize |
| Water Management | 5 | Drip irrigation, rainwater harvesting, mulching, scheduling, deficit irrigation |
| Sustainable Farming | 4 | Crop rotation, composting, conservation agriculture, fertilizer use |
| Crop Health | 4 | Leaf yellowing, fungal disease, wilting, insect damage |
| Climate Risk | 3 | Drought, flood/waterlogging, heat stress |
| Soil Health | 2 | Soil organic matter, soil pH |
| Integrated Pest Management | 2 | IPM principles, pesticide safety |

Retrieval uses keyword-overlap scoring with stop-word filtering. No fabricated citations.

---

## Responsible AI Validation

Every response passes through a 5-dimension validation layer before delivery:

| Dimension | What It Checks |
|-----------|---------------|
| **Safety** | Detects unsupported pesticide/chemical dosage instructions |
| **Uncertainty** | Prevents guaranteed-yield or guaranteed-outcome language |
| **Transparency** | Detects false claims of live weather or real-time data access |
| **Privacy** | Detects requests for passwords, bank details, or government IDs |
| **Groundedness** | Flags responses when RAG retrieval was expected but failed |

---

## Evaluation Results (Executed)

| Test Suite | Tests | Passed | Pass Rate |
|-----------|-------|--------|-----------|
| RAG Retrieval | 27 | 27 | **100%** |
| Responsible AI Patterns | 4 | 4 | **100%** |

See [`evaluation/evaluation_report.md`](evaluation/evaluation_report.md) for full details.

---

## Setup and Running

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Streamlit and python-dotenv are also needed:

```bash
pip install streamlit python-dotenv
```

### 2. Set environment variables

```bash
export IBM_API_KEY="your-ibm-cloud-api-key"
export WATSONX_PROJECT_ID="your-watsonx-project-id"
```

Or create a `.env` file (do not commit to version control):

```
IBM_API_KEY=your-ibm-cloud-api-key
WATSONX_PROJECT_ID=your-watsonx-project-id
```

### 3. Run the Streamlit app

```bash
streamlit run app.py
```

### 4. Run the evaluation tests (no API key needed)

```bash
python evaluation/test_cases.py
```

---

## Deploying to watsonx Orchestrate

### Activate your environment first

```bash
orchestrate env activate <your-environment>
```

### Import in order

```bash
# 1. Model
orchestrate models import -f models/granite-agrisustain.yaml

# 2. Tools
orchestrate tools import -k python -f tools/crop_planning_tool.py
orchestrate tools import -k python -f tools/water_sustainability_tool.py
orchestrate tools import -k python -f tools/crop_health_tool.py
orchestrate tools import -k python -f tools/climate_risk_tool.py
orchestrate tools import -k python -f tools/sustainable_farming_tool.py
orchestrate tools import -k python -f tools/rag_retrieval_tool.py

# 3. Agent
orchestrate agents import -f agents/agrisustain_ai_agent.yaml
```

---

## Responsible AI

| Principle | Implementation |
|-----------|---------------|
| **Fairness** | Recognizes regional, soil, and climatic differences |
| **Transparency** | Every response shows what was retrieved vs. AI-generated |
| **Privacy** | No unnecessary personal data collected; privacy validation active |
| **Accuracy** | No fabricated data, statistics, or citations |
| **Safety** | Chemical instruction validation; encourages product label compliance |
| **Human Oversight** | Every response recommends local expert consultation |
| **Uncertainty** | Guaranteed-outcome language detected and flagged |

> ⚠️ AgriSustain AI is a decision-support tool. It does NOT replace qualified agricultural professionals. For critical farm management decisions, always consult a local agricultural extension officer or agronomist.

---

## IBM 1M1B Internship

This project was developed as part of the IBM 1M1B Internship Programme, demonstrating responsible application of IBM AI technologies to a real-world sustainability challenge.

**Technology demonstrated:**
- IBM Granite 4 H Small (actual model used — validated in IBM watsonx Prompt Lab)
- watsonx.ai API integration
- Retrieval-Augmented Generation (RAG) — implemented and tested
- Responsible AI validation — implemented and tested
- Agentic AI workflow (watsonx Orchestrate)
- Prompt engineering
- SDG alignment (SDG 2, 6, 12, 13)
- Software-only system — no IoT or hardware
