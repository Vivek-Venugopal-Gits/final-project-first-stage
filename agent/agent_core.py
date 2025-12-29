from agent.prompt import build_prompt
from llm.model import LLM
from rag.retriever import retrieve_context
from agent.file_tools import (
    read_file,
    write_file,
    append_file,
    FileToolError
)


class AgentCore:
    """
    Smart Django CLI Agent
    - LLM generates code + explanation
    - Code goes to file
    - Full response prints to CLI
    """

    def __init__(self):
        self.llm = LLM()

    def run(self, user_input: str) -> str:
        # STEP 1: Retrieve context
        try:
            context, sources = retrieve_context(user_input, k=4)
        except Exception:
            context, sources = None, []

        # STEP 2: Prompt LLM
        path = self._extract_path(user_input)
        prompt = build_prompt(user_input=user_input, context=context)
        raw = self.llm.generate(prompt).strip()

        # ANSWER MODE → explanation only
        if not path:
            return raw

        # ACTION MODE → extract code for file, keep full response for CLI
        code = self._extract_code_only(raw)
        if not code:
            return "❌ No code detected in LLM output.\n\n" + raw

        # STEP 3: Remove duplicate imports if file exists
        try:
            existing = read_file(path)
            code = self._remove_duplicate_imports(existing, code)
        except Exception:
            pass  # file does not exist yet

        # STEP 4: Decide safe action
        try:
            read_file(path)
            action = "append_file"
        except Exception:
            action = "write_file"

        # STEP 5: Execute action
        try:
            if action == "write_file":
                write_file(path, code)
                file_status = f"✅ File created: {path}"
            else:
                append_file(path, code)
                file_status = f"✅ Code appended to: {path}"

        except FileToolError as e:
            file_status = f"❌ [FILE ERROR] {e}"

        # STEP 6: Build CLI output (file status + full LLM response + sources)
        cli_output = [file_status, "", "=" * 60, "📝 Full Response:", "=" * 60, raw]
        
        if sources:
            cli_output.extend(["", "=" * 60, "📚 Sources:", "=" * 60])
            cli_output.extend(f"  • {s}" for s in sources)

        return "\n".join(cli_output)

    # ---------------- HELPERS ---------------- #

    def _extract_path(self, user_input: str) -> str | None:
        """Extract file path from user input"""
        for token in user_input.split():
            if token.endswith((".py", ".html")):
                return token
        return None

    def _extract_code_only(self, text: str) -> str:
        """
        Extract code from LLM output
        - Stops at first explanation or blank line after code
        """
        lines = []
        recording = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("class ", "def ", "from ", "import ")):
                recording = True

            # Stop recording if explanation begins
            if recording and (
                stripped.startswith("Explanation") or
                stripped.startswith("In order to") or
                stripped.lower().startswith("you can")
            ):
                break

            if recording:
                lines.append(line)

        return "\n".join(lines).strip()

    def _remove_duplicate_imports(self, existing: str, new_code: str) -> str:
        """
        Removes imports from new_code that are already present in existing
        Only removes exact matches and keeps the rest intact
        """
        existing_lines = existing.splitlines()
        new_lines = new_code.splitlines()
        filtered_lines = []

        for line in new_lines:
            if line.strip() and line.strip() not in existing_lines:
                filtered_lines.append(line)

        return "\n".join(filtered_lines).strip()