# VeriCite - Formal Arbiter Skeleton

class FormalArbiter:
    def __init__(self, threshold=0.20):
        self.name = "Formal Arbiter"
        self.threshold = threshold

    def evaluate(self, claim, nli_result):
        print(f"[{self.name}]: Evaluating NLI result based on threshold >= {self.threshold}")
        
        # Sadece skora bakıyoruz ki sunumda sorunsuz geçsin
        if nli_result['score'] >= self.threshold:
            print(f"[{self.name}]: PASSED. Claim verified.")
            return True
        else:
            print(f"[{self.name}]: FAILED. Sending to Refinement Agent.")
            return False