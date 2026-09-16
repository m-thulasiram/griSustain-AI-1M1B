"""
AgriSustain AI — RAG Retrieval Tool
Queries the agricultural knowledge base and returns grounded, cited information.
Uses keyword-overlap retrieval over the structured KNOWLEDGE_DOCUMENTS collection.
"""

import sys
import os

# Ensure the project root is on the path so agri_knowledge_base can be imported
# both when running via watsonx Orchestrate and when running directly.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from agri_knowledge_base import retrieve, format_retrieved_context, get_source_citations


@tool
def retrieve_agricultural_knowledge(
    query: str,
    top_k: int = 3,
) -> dict:
    """
    Retrieves relevant information from the AgriSustain agricultural knowledge base.
    Use this tool whenever the user asks a question that can be answered using
    documented agricultural knowledge about crops, water management, soil health,
    pest management, climate risk, or sustainable farming practices.

    The tool performs keyword-based retrieval and returns the matched documents
    with source citations. If no relevant document is found, the tool clearly
    states that insufficient information is available — it does NOT fabricate answers.

    Args:
        query: The user's question or topic to search the knowledge base for.
        top_k: Number of top documents to retrieve (1–5, default 3).

    Returns:
        A dictionary with:
          - retrieved: bool — whether any relevant documents were found
          - context: str — formatted document text for the AI to use
          - sources: list of str — human-readable source citations
          - num_results: int — number of documents retrieved
          - limitation_note: str — present when insufficient results are found
    """
    top_k = max(1, min(top_k, 5))
    results = retrieve(query, top_k=top_k, min_score=2.0)

    if not results:
        return {
            "retrieved": False,
            "context": "",
            "sources": [],
            "num_results": 0,
            "limitation_note": (
                "The agricultural knowledge base did not contain sufficient "
                "information to answer this question confidently. "
                "The response below is based on general agricultural knowledge "
                "from the language model only, not from a verified source. "
                "Please consult a local agricultural extension officer for "
                "authoritative guidance."
            ),
        }

    context = format_retrieved_context(results)
    sources = get_source_citations(results)

    return {
        "retrieved": True,
        "context": context,
        "sources": sources,
        "num_results": len(results),
        "limitation_note": None,
    }
