import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class RefinementAgent:
    def __init__(self):
        self.name = "Refinement"
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.1
        )

    # İŞTE BURAYI DÜZELTTİK: Artık nli_result (Hakem raporu) parametresini de kabul ediyor
    def refine_claim(self, claim_data, nli_result):
        print(f"[{self.name}]: Refining claim to better match source evidence... (Previous NLI Score: {nli_result['score']:.2f})")
        
        prompt = PromptTemplate(
            input_variables=["claim", "abstract", "details"],
            template="""You are an academic editor. 
The following claim failed verification because it hallucinated or mismatched the source.
Reason for failure: {details}

Original Claim: {claim}
Source Abstract: {abstract}

Rewrite the claim as exactly ONE single academic sentence so it is 100% grounded in the source. Do not add conversational text."""
        )
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "claim": claim_data['claim'],
                "abstract": claim_data['source_chunk']['abstract'],
                "details": nli_result['details']
            })
            refined_sentence = response.content.replace('\n', ' ').strip()
            
            updated_claim_data = claim_data.copy()
            updated_claim_data['claim'] = refined_sentence
            return updated_claim_data
            
        except Exception as e:
            print(f"[{self.name}]: Error refining claim - {e}")
            return claim_data