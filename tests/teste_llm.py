from core.llm_manager import LLMManager

llm = LLMManager()

print("Enviando mensagem...")

resposta = llm.perguntar("Olá! Quem é você?")

print(resposta)