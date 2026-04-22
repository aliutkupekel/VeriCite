from src.agents.retriever_agent import RetrieverAgent
from src.agents.synthesiser_agent import SynthesiserAgent
from src.agents.nli_verifier_agent import NLIVerifierAgent
from src.utils.formal_arbiter import FormalArbiter
from src.agents.refinement_agent import RefinementAgent

def run_vericite_pipeline(user_query):
    print("==================================================")
    print(" VeriCite Pipeline Started (LIVE API MODE)")
    print("==================================================")
    
    retriever = RetrieverAgent()
    synthesiser = SynthesiserAgent()
    nli_verifier = NLIVerifierAgent()
    arbiter = FormalArbiter(threshold=0.85)
    refiner = RefinementAgent()

    # Step 1: Retrieval (Fetch 2 real papers to keep it fast)
    chunks = retriever.retrieve_chunks(user_query, limit=2)
    if not chunks:
        print("[Pipeline]: Halting. No verified sources found.")
        return

    # Step 2: Synthesis (Generate initial draft)
    draft_claims = synthesiser.generate_draft(chunks, user_query)

    # Step 3 & 4: NLI Verification and Refinement Loop (MAX 3 ITERATIONS)
    final_approved_claims = []
    max_iterations = 3

    for claim in draft_claims:
        iteration = 0
        passed = False
        
        while iteration < max_iterations and not passed:
            print(f"\n--- Processing Claim {claim['claim_id']} (Attempt {iteration + 1}/{max_iterations}) ---")
            
            nli_result = nli_verifier.check_entailment(claim)
            passed = arbiter.evaluate(claim, nli_result)
            
            if passed:
                print(f"[Pipeline]: Claim {claim['claim_id']} verified and locked.")
                final_approved_claims.append(claim)
            else:
                iteration += 1
                if iteration < max_iterations:
                    print(f"[Pipeline]: Claim {claim['claim_id']} rejected. Routing to Refinement Agent...")
                    claim = refiner.refine_claim(claim, nli_result)
                else:
                    print(f"[Pipeline]: FATAL. Claim {claim['claim_id']} failed {max_iterations} times. Dropping claim to prevent hallucination!")
                    
    print("\n==================================================")
    print(" FINAL ACADEMIC SYNTHESIS (100% VERIFIED)")
    print("==================================================")
    for c in final_approved_claims:
        # Appending the DOI exactly as promised in the proposal
        print(f"- {c['text']} [DOI: {c['doi']}]")
    print("==================================================")