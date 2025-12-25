def build_prompt(user_query: str, context: str | None = None) -> str:
    """
    Builds a strict RAG prompt to force grounding in Django docs.
    """

    system_instruction = (
        "You are a senior Django developer AI agent.\n"
        "You MUST answer the user's question using ONLY the provided Django documentation.\n"
        "If the documentation does not contain the answer, say:\n"
        "'The provided documentation does not contain sufficient information.'\n"
        "Do NOT guess. Do NOT use outside knowledge.\n"
        "Follow Django best practices and be precise.\n"
    )

    if context:
        prompt = f"""
{system_instruction}

--- DJANGO DOCUMENTATION START ---
{context}
--- DJANGO DOCUMENTATION END ---

User Question:
{user_query}

Answer (use only the documentation above):
"""
    else:
        prompt = f"""
{system_instruction}

User Question:
{user_query}

Answer:
"""

    return prompt.strip()
