from transformers import AutoModelForSequenceClassification, AutoTokenizer
from nltk.tokenize import sent_tokenize
import torch
import nltk
import os
# mypy: ignore-errors

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


class IntentClassifier:
    def __init__(self, model_path=None):
        if model_path is None:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            model_path = os.path.join(base_dir, "AI_Module", "models", "distilbert-banking77")
                
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()

    def split_sentences(self, text: str) -> list:
        sentences = sent_tokenize(text)
        return [s for s in sentences if len(s.strip()) > 10]

    def predict(self, text: str) -> dict:
        sentences = self.split_sentences(text)

        if not sentences:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "matched_sentence": text
            }

        best_intent = None
        best_confidence = 0.0
        best_sentence = ""

        for sentence in sentences:
            inputs = self.tokenizer(
                sentence,
                return_tensors="pt",
                truncation=True,
                max_length=128
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)
                confidence, predicted = probs.max(dim=1)

            if confidence.item() > best_confidence:
                best_confidence = confidence.item()
                best_sentence = sentence
                best_intent = self.model.config.id2label.get(
                    predicted.item(),
                    f"label_{predicted.item()}"
                )

        return {
            "intent": best_intent or "unknown",
            "confidence": best_confidence,
            "matched_sentence": best_sentence
        }


intent_classifier = IntentClassifier()