try:
    import ollama
except ModuleNotFoundError:
    ollama = None


class ProjectSummaryClient:
    """Reusable client for generating AI summaries of project data."""

    def __init__(self, model_name="llama3.2"):
        self.model_name = model_name

    def summarize(self, prompt):
        """Send a prompt to the AI model and return a readable summary.
        Returns a clear fallback message instead of crashing if the
        service is unavailable or the request fails."""
        if ollama is None:
            return "AI summary unavailable: the 'ollama' package is not installed."

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            message = response.get("message") if isinstance(response, dict) else getattr(response, "message", None)
            content = message.get("content") if isinstance(message, dict) else getattr(message, "content", None)

            if not content or not content.strip():
                return "AI summary unavailable: the service returned an empty response."

            return content.strip()
        except Exception as error:
            return f"AI summary unavailable: {error}"