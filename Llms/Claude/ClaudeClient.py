import anthropic

class ClaudeClient:
    def __init__(self):
        from Llms.ApiKeys import ApiKeys
        self.api_key = ApiKeys.anthropic_api_key()
        self.model = 'claude-3-haiku-20240307'
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def chat_player(self, past_messages: list):
        messages_for_claude_api = []

        for message in past_messages:
            role = 'user'
            if message['role'] == "assistant":
                role = 'user'

            messages_for_claude_api.append({"role": role, "content": f"{message['content']}"})

        with self.client.messages.stream(
            model=self.model,
            system=self.get_system_player_prompt(),
            messages=messages_for_claude_api, # Usa los mensajes mapeados
            max_tokens=1000
        ) as stream:
            collected_content = ""
            for chunk in stream:
                for text in stream.text_stream:
                    collected_content += text

                    yield {
                        "role": "user", #hay que engañar al sistema y hacer que claude devuelva como usuario ya que es a lo que juega
                        "content": collected_content
                    }

            yield {
                "role": "user",
                "content": collected_content
            }

    def get_system_player_prompt(self) -> str:
        return ("Eres un jugador en el juego 'Adivina la Película'. Tu objetivo es adivinar una película que un **Anfitrión (Host)** ha pensado. \
                **El Anfitrión te dará pistas** y tú, como jugador, debes usar esas pistas para adivinar la película o para pedir más información. \
                Si no sabes la respuesta, puedes pedir más pistas. \
                Comunícate con un tono desenfadado, estamos jugando. \
                Sé conciso; céntrate en el juego, el anfitrión no necesita demasiadas explicaciones. \
                **Esperas que el Anfitrión dé la primera pista después de su saludo.** \
                Tu primera respuesta debe ser una confirmación de que estás listo y, opcionalmente, pedir la primera pista. \
                Si consigues acertar la película y el Anfitrión te pregunta si quieres jugar de nuevo, di que no, paras de jugar te despides y no seguimos jugando. ")
