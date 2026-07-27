from core.llm_manager import LLMManager
from core.prompt_builder import PromptBuilder
from core.task_manager import TaskManager
from core.agent_manager import AgentManager


class OrchestratorBrain:


    def __init__(self, file_manager):

        self.file_manager = file_manager
        self.llm = LLMManager()
        self.prompt_builder = PromptBuilder()
        self.task_manager = TaskManager()
        self.agent_manager = AgentManager()


    def processar_solicitacao(self, mensagem_usuario):

        prompt_sistema = self.prompt_builder.carregar_prompt("orchestrator")

        print("\n===== PROMPT DO ORCHESTRATOR =====")
        print(prompt_sistema)
        print("=================================\n")

        task = self.task_manager.criar_task(mensagem_usuario)
        resultado_agente = self.agent_manager.executar(
    task["agente"],
    mensagem_usuario
)

        resposta = self.llm.perguntar(
            prompt_sistema,
            mensagem_usuario
        )

        resposta += (
            f"\n\n📌 Task criada com sucesso!\n"
            f"ID: {task['id']}\n"
            f"Status: {task['status']}\n"
            f"Agente inicial: {task['agente']}"
        )
        resposta += (
    "\n\n🤖 Resultado do agente:\n"
    f"{resultado_agente}"
)

        return resposta