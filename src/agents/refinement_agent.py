import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

class RefinementAgent:
    def __init__(self):
        self.name = "Refinement Agent"
        # We use a lower temperature here (0.1) because we want strict correction, not creativity
        self.llm = ChatGroq(
            temperature=0.1, 
            model_name="llama3-8b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def refine_claim(self, claim, nli_result):
        print(f"[{self.name}]: Fixing rejected claim {claim['claim_id']}...")
        
        prompt = PromptTemplate.from_template(
            "You are a strict academic corrector. A previous AI generated a claim that FAILED a Natural Language Inference (NLI) check against the source abstract.\n"
            "Reason for failure: The relationship was evaluated as '{nli_label}' with a confidence score of {nli_score}.\n\n"
            "Source Abstract: {abstract}\n"
            "Rejected Claim: {claim_text}\n\n"
            "Task: Rewrite the claim into a single, highly accurate sentence that is STRICTLY supported by the abstract. Do NOT invent information.\n"
            "Revised Claim:"
        )
        
        chain = prompt | self.llm
        response = chain.invoke({
            "nli_label": nli_result['label'],
            "nli_score": nli_result['score'],
            "abstract": claim['source_abstract'],
            "claim_text": claim['text']
        })
        
        # Update the claim with the newly corrected text
        claim['text'] = response.content.strip()
        print(f"[{self.name}]: Claim {claim['claim_id']} rewritten successfully.")
        
        return claim