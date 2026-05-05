import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class SynthesiserAgent:
    def __init__(self):
        self.name = "Synthesiser"
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.0 # SIFIR YARATICILIK! Sadece gerçekler.
        )

    def generate_draft(self, chunks, query):
        print(f"[{self.name}]: Generating academic draft using retrieved chunks...")
        
        prompt = PromptTemplate(
            input_variables=["query", "abstract"],
            template="""You are a strict academic extractor. 
Source Abstract: '{abstract}'

Extract exactly ONE factual sentence from the abstract that is relevant to '{query}'. 
Do NOT invent anything. Do NOT rephrase heavily. Keep it almost identical to the source to pass a strict mathematical logic check."""
        )
        
        chain = prompt | self.llm
        
        draft_claims = []
        for i, chunk in enumerate(chunks):
            try:
                response = chain.invoke({"query": query, "abstract": chunk['abstract']})
                sentence = response.content.replace('\n', ' ').strip()
                
                draft_claims.append({
                    "claim_id": f"C{i+1}",
                    "claim": sentence,
                    "source_chunk": chunk
                })
            except Exception as e:
                print(f"[{self.name}]: Error generating claim - {e}")
                
        print(f"[{self.name}]: Generated {len(draft_claims)} draft claims.")
        return draft_claims