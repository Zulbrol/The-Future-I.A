from core.agent_manager import AgentManager


manager = AgentManager()


resultado = manager.executar(
    "architect",
    "Criar uma landing page premium"
)


print(resultado)