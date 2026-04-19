# VeriCite - Main Pipeline Orchestration

from src.agents.retriever_agent import RetrieverAgent
from src.agents.synthesiser_agent import SynthesiserAgent
from src.agents.nli_verifier_agent import NLIVerifierAgent
from src.utils.formal_arbiter import FormalArbiter

def run_vericite_pipeline(user_query):
    print("==================================================")
    print(" VeriCite Pipeline Started")
    print("==================================================")
    
    # Initialize components
    retriever = RetrieverAgent()
    synthesiser = SynthesiserAgent()
    nli_verifier = NLIVerifierAgent()
    arbiter = FormalArbiter(threshold=0.85)

    # Step 1: Retrieval
    retriever.setup_database()
    chunks = retriever.retrieve_chunks(user_query)

    # Step 2: Synthesis
    draft_claims = synthesiser.generate_draft(chunks)

    # Step 3 & 4: NLI Verification and Formal Arbiter
    for claim in draft_claims:
        nli_result = nli_verifier.check_entailment(claim)
        passed = arbiter.evaluate(claim, nli_result)
        
        if passed:
            print("\nFinal Output: Claim verified and ready for user.")
        else:
            print("\nFinal Output: Claim rejected. (Refinement loop will be triggered here)")
            
    print("==================================================")
    print(" Pipeline Execution Finished")
    print("==================================================")