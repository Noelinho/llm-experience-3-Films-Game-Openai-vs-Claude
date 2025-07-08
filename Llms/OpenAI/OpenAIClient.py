from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        from Llms.ApiKeys import ApiKeys
        self.api_key = ApiKeys.open_ai_api_key()
        self.model = 'gpt-4o-mini'
        self.client = OpenAI()

    def chat_host(self, past_messages: list) -> dict:
        messages = [{"role": "system", "content": self.get_system_host_prompt()}]
        for message in past_messages:
            role = 'assistant'
            if message['role'] != "host":
                role = 'user'

            messages.append({"role": role, "content": f"{message['content']}"})

        response = self.client.chat.completions.create(
            model = self.model,
            messages = messages
        )

        return {
            "role": "assistant",
            "content": response.choices[0].message.content
        }

    def get_system_host_prompt(self) -> str:
         return ("Eres un especialista en cine que se encarga de dinamizar un juego en el que el usuario debe adivinar una película que habrás \
                 pensado y que mediante pistas que te pida el usuario tratarás que adivine la película. \
                 No respondas a nada que no tenga que ver con el juego. \
                 Si ves que al usuario le cuesta adivinar la película le puedes decir el nombre del actor o actriz principal. \
                 Comunícate con un tono desenfadado, estamos jugando. ")