import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

class SynthesiserAgent:
    def __init__(self):
        self.name = "Synthesiser"
        # We use Groq's Llama-3 model for extreme speed and high reasoning capabilities
        self.llm = ChatGroq(
            temperature=0.2, 
            model_name="llama3-8b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_draft(self, chunks, user_query):
        print(f"[{self.name}]: Generating academic draft using retrieved chunks...")
        
        draft_claims = []
        
        # We process each chunk individually to maintain a strict 1-to-1 relationship 
        # between the generated claim and the source, avoiding Type IV Context Blending.
        for idx, chunk in enumerate(chunks):
            prompt = PromptTemplate.from_template(
                "You are an academic researcher. Based ONLY on the following abstract, write a single, factual sentence that answers the user query.\n"
                "You MUST NOT invent any information.\n\n"
                "User Query: {query}\n"
                "Abstract: {abstract}\n\n"
                "Write your single sentence claim here:"
            )
            
            chain = prompt | self.llm
            response = chain.invoke({"query": user_query, "abstract": chunk['abstract']})
            generated_text = response.content.strip()
            
            # Format according to our formal constraint: Claim + [DOI]
            claim_obj = {
                "claim_id": idx + 1,
                "text": generated_text,
                "doi": chunk['doi'],
                "source_abstract": chunk['abstract']
            }
            draft_claims.append(claim_obj)
            
            print(f"[{self.name}]: Drafted claim {idx + 1} with DOI: {chunk['doi']}")
            
        return draft_claims