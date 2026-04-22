import torch
from sentence_transformers import CrossEncoder

class NLIVerifierAgent:
    def __init__(self):
        self.name = "NLI Verifier"
        print(f"[{self.name}]: Loading local HuggingFace NLI model (This might take a moment the first time)...")
        # We use a lightweight cross-encoder specifically trained for Natural Language Inference (NLI)
        self.model = CrossEncoder('cross-encoder/nli-MiniLM2-L6-H768', max_length=512)

    def check_entailment(self, claim):
        print(f"[{self.name}]: Checking claim mathematically against original abstract...")
        
        # The model takes pairs of [Premise, Hypothesis]
        # Premise = Original Abstract, Hypothesis = Generated Claim
        scores = self.model.predict([(claim['source_abstract'], claim['text'])])
        
        # For this specific model, the output scores are mapped as:
        # 0: Contradiction, 1: Entailment, 2: Neutral
        score_idx = scores[0].argmax()
        
        labels = ["contradiction", "entailment", "neutral"]
        predicted_label = labels[score_idx]
        
        # We normalize the raw logits to get a confidence percentage
        confidence = torch.softmax(torch.tensor(scores[0]), dim=0)[score_idx].item()
        
        print(f"[{self.name}]: Result -> Label: {predicted_label.upper()}, Confidence: {confidence:.2f}")
        
        return {
            "score": confidence,
            "label": predicted_label
        }