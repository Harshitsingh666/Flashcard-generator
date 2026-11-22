# Flashcard Generator with Hugging Face

A small Gradio app that turns a study topic into interactive question-and-answer cards using Hugging Face Inference Providers.

## Requirements

- Python 3.10 or later
- A Hugging Face user access token with Inference Providers permission

## Run locally

```bash
python -m venv .venv
```

Activate the environment, then install the dependencies:

```bash
# PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Set your token as an environment variable. Do not paste it into `app.py` or commit it to Git.

PowerShell:

```powershell
$env:HF_TOKEN = "hf_your_token"
python app.py
```

macOS/Linux:

```bash
export HF_TOKEN="hf_your_token"
python app.py
```

Open the local URL printed by Gradio. Enter a topic, choose the number of cards, and click **Generate flashcards**. Click each question to reveal its answer.

## Tests

Run the offline tests with:

```bash
python -m unittest discover -s tests
```

## Configuration

- `HF_TOKEN` — required Hugging Face token
- `HF_MODEL` — optional default model ID; defaults to `Qwen/Qwen2.5-7B-Instruct`

The model field in the app can also be changed for a single generation session. Inference availability and pricing depend on the selected model and provider.

