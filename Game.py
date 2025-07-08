import gradio as gr

from Llms.OpenAI.OpenAIClient import OpenAIClient
from Llms.Claude.ClaudeClient import ClaudeClient

open_ai_client = OpenAIClient()
claude_client = ClaudeClient()
#gr.ChatInterface(fn=open_ai_client.chat, type="messages").launch()



# print ("OpenAI: " + "Hola, ¿quieres jugar a adivinar una película? Dime 'sí' o 'no'.")
# for i in range(5):
#     messages.append(claude_client.chat_player(messages))
#     messages.append(open_ai_client.chat_host(messages))

def start_simulation(max_turns):
    messages = [{"role": "assistant", "content": "Hola, ¿quieres jugar a adivinar una película?"}]

    yield messages

    for i in range(max_turns):
        messages.append(claude_client.chat_player(messages))

        yield messages
        messages.append(open_ai_client.chat_host(messages))

        yield messages



with gr.Blocks() as demo:
    gr.Markdown("# Adivina la Película")
    gr.Markdown("Presiona 'Iniciar Conversación' para ver a las IAs interactuar.")

    chatbot = gr.Chatbot(label="Diálogo entre IAs", height=500, type="messages")

    max_turns_slider = gr.Slider(minimum=1, maximum=6, value=2, step=1, label="Número Máximo de Turnos")

    start_button = gr.Button("Iniciar Conversación")

    start_button.click(
        fn=start_simulation,
        inputs=[max_turns_slider],
        outputs=[chatbot]
    )
demo.launch()