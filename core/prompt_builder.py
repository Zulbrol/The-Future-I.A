from pathlib import Path


class PromptBuilder:

    def __init__(self):

        self.prompt_path = Path("prompts")

    def carregar_prompt(self, nome_prompt: str) -> str:

        arquivo = self.prompt_path / f"{nome_prompt}.txt"

        if not arquivo.exists():
            raise FileNotFoundError(
                f"Prompt '{nome_prompt}' não encontrado."
            )

        with open(arquivo, "r", encoding="utf-8") as f:
            return f.read()