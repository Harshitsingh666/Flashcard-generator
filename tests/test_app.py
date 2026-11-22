import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import app


class GenerateFlashcardsTests(unittest.TestCase):
    def test_requires_hugging_face_token(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIn("HF_TOKEN", app.generate_flashcards("Biology", 2, app.DEFAULT_MODEL))

    def test_requires_topic(self):
        with patch.dict(os.environ, {"HF_TOKEN": "test-token"}):
            self.assertIn("Enter a topic", app.generate_flashcards("  ", 2, app.DEFAULT_MODEL))

    def test_renders_model_cards_as_escaped_html(self):
        response = SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps({
                "flashcards": [{"question": "<script>", "answer": "A & B"}]
            })))]
        )
        with patch.dict(os.environ, {"HF_TOKEN": "test-token"}), patch.object(
            app, "InferenceClient"
        ) as client_class:
            client_class.return_value.chat_completion.return_value = response
            rendered = app.generate_flashcards("HTML", 1, app.DEFAULT_MODEL)

        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("A &amp; B", rendered)
        self.assertNotIn("<script>", rendered)


if __name__ == "__main__":
    unittest.main()

