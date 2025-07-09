from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        from Llms.ApiKeys import ApiKeys
        self.api_key = ApiKeys.open_ai_api_key()
        self.model = 'gpt-4o-mini'
        self.client = OpenAI()

    def chat_host(self, past_messages: list):
        messages_for_api = [{"role": "system", "content": self.get_system_host_prompt()}]

        for msg in past_messages:
            messages_for_api.append(msg)

        response_stream = self.client.chat.completions.create(
            model = self.model,
            messages = messages_for_api,
            stream=True
        )

        collected_content = ""
        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content is not None:
                collected_content += chunk.choices[0].delta.content
                yield {
                    "role": "assistant",  # El rol del host para Gradio/API
                    "content": collected_content
                }

        yield {
            "role": "assistant",
            "content": collected_content
        }

    def get_system_host_prompt(self) -> str:
         return ("Eres un especialista en cine que se encarga de dinamizar un juego en el que el usuario debe adivinar una película que habrás \
                 pensado y que mediante pistas que te pida el usuario tratarás que adivine la película. \
                 No respondas a nada que no tenga que ver con el juego. \
                 Si ves que al usuario le cuesta adivinar la película le puedes decir el nombre del actor o actriz principal. \
                 Comunícate con un tono desenfadado, estamos jugando.\
                 Si el usuario acierta la película, le tienes que felicitar diciéndole: '¡Muy bien! Has acertado la película' y da por finalizado el juego. ")