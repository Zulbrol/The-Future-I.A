import os
import shutil
from pathlib import Path


class FileManager:
    """
    Gerenciador de arquivos da The Future IA.
    Responsável por criar, ler, editar, mover e excluir arquivos.
    """

    def __init__(self, base_path: str = "."):
        # "." = pasta onde está o projeto The Future
        self.base_path = Path(base_path).resolve()

    # =====================================================
    # LISTAR
    # =====================================================

    def listar_arquivos(self):
        """Retorna todos os arquivos do projeto."""
        arquivos = []

        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                caminho = Path(root) / file
                arquivos.append(str(caminho.relative_to(self.base_path)))

        return arquivos

    def listar_arvore(self):
        """Retorna a árvore completa do projeto."""

        resultado = []

        for root, dirs, files in os.walk(self.base_path):

            nivel = len(Path(root).relative_to(self.base_path).parts)

            indent = "    " * nivel

            pasta = Path(root).name

            if nivel == 0:
                resultado.append(f"{self.base_path.name}/")
            else:
                resultado.append(f"{indent}{pasta}/")

            for arquivo in files:
                resultado.append(f"{indent}    {arquivo}")

        return "\n".join(resultado)

    # =====================================================
    # LEITURA
    # =====================================================

    def ler_arquivo(self, caminho_relativo: str):

        caminho = self.base_path / caminho_relativo

        if not caminho.exists():
            return f"Erro: '{caminho_relativo}' não encontrado."

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                return arquivo.read()

        except Exception as erro:
            return f"Erro ao ler arquivo: {erro}"

    # =====================================================
    # ESCRITA
    # =====================================================

    def escrever_arquivo(self, caminho_relativo: str, conteudo: str):

        caminho = self.base_path / caminho_relativo

        caminho.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo)

            return f"Arquivo '{caminho_relativo}' salvo."

        except Exception as erro:
            return f"Erro ao salvar arquivo: {erro}"

    # =====================================================
    # PASTAS
    # =====================================================

    def criar_pasta(self, nome: str):

        pasta = self.base_path / nome

        try:
            pasta.mkdir(parents=True, exist_ok=True)
            return f"Pasta '{nome}' criada."

        except Exception as erro:
            return f"Erro: {erro}"

    # =====================================================
    # EXCLUIR
    # =====================================================

    def excluir_arquivo(self, caminho_relativo: str):

        caminho = self.base_path / caminho_relativo

        if not caminho.exists():
            return "Arquivo não encontrado."

        try:
            caminho.unlink()
            return f"Arquivo '{caminho_relativo}' excluído."

        except Exception as erro:
            return f"Erro: {erro}"

    # =====================================================
    # COPIAR
    # =====================================================

    def copiar_arquivo(self, origem: str, destino: str):

        origem = self.base_path / origem
        destino = self.base_path / destino

        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(origem, destino)
            return "Arquivo copiado."

        except Exception as erro:
            return f"Erro: {erro}"

    # =====================================================
    # MOVER
    # =====================================================

    def mover_arquivo(self, origem: str, destino: str):

        origem = self.base_path / origem
        destino = self.base_path / destino

        try:
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(origem, destino)
            return "Arquivo movido."

        except Exception as erro:
            return f"Erro: {erro}"

    # =====================================================
    # EXISTE?
    # =====================================================

    def existe(self, caminho_relativo: str):

        return (self.base_path / caminho_relativo).exists()