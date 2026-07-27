import json
from pathlib import Path
from datetime import datetime


class TaskManager:

    def __init__(self):

        self.tasks_path = Path("memory/tasks")
        self.tasks_path.mkdir(parents=True, exist_ok=True)

    def criar_task(self, titulo, agente="Architect"):

        tarefas = list(self.tasks_path.glob("task_*.json"))

        novo_id = len(tarefas) + 1

        task = {

            "id": f"task_{novo_id:03}",

            "titulo": titulo,

            "status": "Pendente",

            "agente": agente,

            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),

            "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        }

        arquivo = self.tasks_path / f"{task['id']}.json"

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(task, f, indent=4, ensure_ascii=False)

        return task

    def listar_tasks(self):

        tarefas = []

        for arquivo in self.tasks_path.glob("task_*.json"):

            with open(arquivo, "r", encoding="utf-8") as f:

                tarefas.append(json.load(f))

        return tarefas

    def carregar_task(self, task_id):

        arquivo = self.tasks_path / f"{task_id}.json"

        if not arquivo.exists():
            return None

        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)

    def atualizar_status(self, task_id, novo_status):

        task = self.carregar_task(task_id)

        if task is None:
            return False

        task["status"] = novo_status

        task["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        arquivo = self.tasks_path / f"{task_id}.json"

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(task, f, indent=4, ensure_ascii=False)

        return True