import html
import json
import os

import gradio as gr
from huggingface_hub import InferenceClient

DEFAULT_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct")


def generate_flashcards(topic, count, model):
    token = os.getenv("HF_TOKEN")
    if not token:
        return "<p>Set the HF_TOKEN environment variable, then restart the app.</p>"
    if not topic or not topic.strip():
        return "<p>Enter a topic to generate flashcards.</p>"

    prompt = (
        f"Create exactly {int(count)} concise study flashcards about: {topic.strip()}\n"
        'Return only a JSON object in this format: '
        '{"flashcards":[{"question":"...","answer":"..."}]} '
        "Use accurate, self-contained questions and clear answers."
    )

    try:
        client = InferenceClient(model=model.strip() or DEFAULT_MODEL, token=token)
        result = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1200,
            response_format={"type": "json_object"},
        )
        payload = json.loads(result.choices[0].message.content)
        cards = payload.get("flashcards", [])
        if not isinstance(cards, list) or not cards:
            raise ValueError("The model returned no flashcards.")

        return "".join(
            '<details class="card"><summary>'
            f"{html.escape(str(card.get('question', 'Question')))}"
            "</summary><p>"
            f"{html.escape(str(card.get('answer', 'No answer provided.')))}"
            "</p></details>"
            for card in cards[: int(count)]
        )
    except Exception as error:
        return f"<p>Could not generate flashcards: {html.escape(str(error))}</p>"


with gr.Blocks(title="Flashcard Generator") as demo:
    gr.Markdown("# Flashcard Generator\nTurn a topic into study cards with a Hugging Face model.")
    with gr.Row():
        topic = gr.Textbox(label="Topic", placeholder="e.g. Photosynthesis", scale=3)
        count = gr.Slider(1, 12, value=5, step=1, label="Number of cards", scale=1)
    model = gr.Textbox(label="Hugging Face model", value=DEFAULT_MODEL)
    generate = gr.Button("Generate flashcards", variant="primary")
    cards = gr.HTML(label="Flashcards")
    generate.click(generate_flashcards, inputs=[topic, count, model], outputs=cards)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", inbrowser=False)

