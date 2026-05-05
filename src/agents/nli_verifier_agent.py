from sentence_transformers import CrossEncoder
import numpy as np

class NLIVerifierAgent:
    def __init__(self):
        self.name = "NLI Verifier"
        # Hakem modelimiz zaten indirildi, direkt hafızaya alıyor
        self.model = CrossEncoder('cross-encoder/nli-MiniLM2-L6-H768')

    def check_entailment(self, claim_data):
        print(f"[{self.name}]: Checking claim mathematically against original abstract...")
        
        # İŞTE DÜZELTTİĞİMİZ YER: Doğru etiketleri okuyoruz
        premise = claim_data['source_chunk']['abstract']  # Orijinal Makale (Kaynak)
        hypothesis = claim_data['claim']                  # Yapay Zekanın Yazdığı Cümle
        
        # Matematiksel tahmin yapılıyor
        scores = self.model.predict([(premise, hypothesis)])
        
        # Çıkan ham skorları yüzdelik oranlara (probabilities) çeviriyoruz
        probabilities = np.exp(scores) / np.sum(np.exp(scores), axis=1, keepdims=True)
        
        # cross-encoder/nli-MiniLM2-L6-H768 modeli için etiketler:
        # 0: Çelişki (Contradiction), 1: Uyumlu (Entailment), 2: Nötr (Neutral)
        contradiction_score = probabilities[0][0]
        entailment_score = probabilities[0][1]
        neutral_score = probabilities[0][2]
        
        # En yüksek skora göre son kararı veriyoruz
        label = "entailment"
        if contradiction_score > entailment_score and contradiction_score > neutral_score:
            label = "contradiction"
        elif neutral_score > entailment_score:
            label = "neutral"
            
        result = {
            "score": float(entailment_score),
            "label": label,
            "details": f"Entailment: {entailment_score:.2f}, Contradiction: {contradiction_score:.2f}, Neutral: {neutral_score:.2f}"
        }
        
        return result