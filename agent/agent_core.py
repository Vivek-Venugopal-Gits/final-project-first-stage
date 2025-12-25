from agent.prompt import build_prompt
from llm.model import LLM
from rag.retriever import retrieve_context


class AgentCore:
    def __init__(self):
        # Initialize the LLM once
        self.llm = LLM()

    def run(self, user_input: str) -> str:
        """
        Executes a full RAG-based reasoning cycle:
        1. Retrieve relevant Django documentation
        2. Build a context-aware prompt
        3. Generate a grounded answer using the LLM
        """

        # STEP 1: Retrieve relevant context from vector DB
        try:
            context, sources = retrieve_context(user_input, k=4)
        except Exception as e:
            context = None
            sources = []
            retrieval_error = f"[Warning] Context retrieval failed: {e}"
        else:
            retrieval_error = None

        # STEP 2: Build prompt with retrieved context
        prompt = build_prompt(
            user_query=user_input,
            context=context
        )

        # STEP 3: Generate response from LLM
        response = self.llm.generate(prompt)

        # STEP 4: Append sources for transparency (RAG best practice)
        if sources:
            response += "\n\n📚 Sources:\n"
            for src in sources:
                response += f"- {src}\n"

        # STEP 5: Append retrieval warning if needed
        if retrieval_error:
            response += f"\n\n{retrieval_error}"

        return response
