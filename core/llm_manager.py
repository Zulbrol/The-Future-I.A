import json
from openai import OpenAI


class LLMManager:

    def __init__(self):

        self.client = OpenAI(
            base_url="http://127.0.0.1:8080/v1",
            api_key="the-future"
        )


        self.config = self.carregar_config()


        modelo_atual = self.config["modelo_padrao"]

        self.modelo = self.config["modelos"][modelo_atual]


    def carregar_config(self):

        with open(
            "config/models.json",
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)



    def perguntar(
     self,
     prompt_sistema,
     mensagem_usuario,
     modelo=None
    ):


        if modelo:

            configuracao = self.config["modelos"][modelo]

        else:

            configuracao = self.modelo



        resposta = self.client.chat.completions.create(

            model=configuracao["nome"],

            messages=[
                {
                    "role":"system",
                    "content": prompt_sistema
                },
                {
                    "role":"user",
                    "content": mensagem_usuario
                 }
],


            temperature=configuracao["temperature"],

            max_tokens=configuracao["tokens"]

        )


        return resposta.choices[0].message.content