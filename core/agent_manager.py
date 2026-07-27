import importlib


class AgentManager:

    def __init__(self):

        self.agents_path = "agents"


    def executar(self, nome_agente, tarefa):

        try:

            nome_agente = nome_agente.lower()


            modulo = importlib.import_module(
                f"{self.agents_path}.{nome_agente}"
            )


            classe_nome = (
                nome_agente.capitalize()
                + "Agent"
            )


            agente_class = getattr(
                modulo,
                classe_nome
            )


            agente = agente_class()


            resposta = agente.executar(
                tarefa
            )


            return resposta


        except Exception as erro:

            return (
                f"Erro ao executar agente {nome_agente}: "
                f"{erro}"
            )