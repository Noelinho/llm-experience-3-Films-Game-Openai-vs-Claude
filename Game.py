import gradio as gr
import time

from Llms.OpenAI.OpenAIClient import OpenAIClient
from Llms.Claude.ClaudeClient import ClaudeClient

open_ai_client = OpenAIClient()
claude_client = ClaudeClient()

def start_simulation(max_turns):
    #conversation_history = [{"role": "assistant", "content": "Hola, ¿quieres jugar a adivinar una película? Pensaré en una y tú la adivinarás."}]
    conversation_history = []
    game_over = False

    initial_host_response_generator = open_ai_client.chat_host([])

    for partial_host_response in initial_host_response_generator:
        if conversation_history and conversation_history[-1]["role"] == "assistant":
            conversation_history[-1] = partial_host_response
        else:
            conversation_history.append(partial_host_response)

        yield conversation_history

    for i in range(max_turns):
        if game_over:
            break

        time.sleep(1)

        for partial_player_response in claude_client.chat_player(conversation_history):

            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history[-1] = partial_player_response
            else:
                conversation_history.append(partial_player_response)

            yield conversation_history

        time.sleep(1)

        for partial_host_response in open_ai_client.chat_host(conversation_history):
            if conversation_history and conversation_history[-1]["role"] == "assistant":
                conversation_history[-1] = partial_host_response
            else:
                conversation_history.append(partial_host_response)

            yield conversation_history

            final_host_response = conversation_history[-1]["content"]
            if "¡muy bien! has acertado la película" in final_host_response.lower():
                game_over = True  # El Host ha confirmado el fin del juego.
                print("DEBUG: OpenAI ha confirmado el fin del juego. Bandera game_over activada.")

        yield conversation_history

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