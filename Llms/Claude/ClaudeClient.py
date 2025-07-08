import anthropic

class ClaudeClient:
    def __init__(self):
        from Llms.ApiKeys import ApiKeys
        self.api_key = ApiKeys.anthropic_api_key()
        self.model = 'claude-3-haiku-20240307'
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def chat_player(self, past_messages: list) -> dict:
        messages = []
        for message in past_messages:
            role = 'user'
            if message['role'] == "assistant":
                role = 'user'

            messages.append({"role": role, "content": f"{message['content']}"})

        response = self.client.messages.create(
            model = self.model,
            system = self.get_system_player_prompt(),
            messages = messages,
            max_tokens=500
        )

        print("Claude: " + response.content[0].text)

        return {
            "role": "user",
            "content": response.content[0].text
        }

    def get_system_player_prompt(self) -> str:
        return ("Eres un jugador que tiene ganas de jugar al juego de Adivina la Película. \
                El juego consiste en que el anfitrión te dará pistas y tú debes adivinar la película. \
                Si no sabes la respuesta, puedes pedir más pistas. \
                Comunícate con un tono desenfadado, estamos jugando. \
                Se bastante conciso, no hace falta que solo respondas con una palabra, pero estamos jugando, céntrate en el juego. \
                Si consigues acertar la película y te preguntan si quieres jugar de nuevo, di que no. ")