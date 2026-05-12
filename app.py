import streamlit as st
import time
from src.agents.retriever_agent import RetrieverAgent
from src.agents.synthesiser_agent import SynthesiserAgent
from src.agents.nli_verifier_agent import NLIVerifierAgent
from src.utils.formal_arbiter import FormalArbiter
from src.agents.refinement_agent import RefinementAgent

# Sayfa Ayarları
st.set_page_config(page_title="VeriCite AI", page_icon="🎓", layout="wide")

# Başlık ve Açıklama
st.title("🎓 VeriCite: NLI-Verified Academic Synthesis")
st.markdown("""
Welcome to the VeriCite Multi-Agent System. This AI uses a strict **Formal Arbiter** and **NLI Verification** to ensure zero-hallucination academic research. Enter your topic below to begin.
""")
st.divider()

# Kullanıcı Girişi
user_query = st.text_input("🔍 Enter your academic research topic:", placeholder="e.g., AI hallucination multi-agent")

# Çalıştır Butonu
if st.button("🚀 Run VeriCite Pipeline", type="primary"):
    if not user_query:
        st.warning("Please enter a research topic first.")
    else:
        # Ajanları Başlat
        retriever = RetrieverAgent()
        synthesiser = SynthesiserAgent()
        nli_verifier = NLIVerifierAgent()
        arbiter = FormalArbiter(threshold=0.20)
        refiner = RefinementAgent()

        final_approved_claims = []
        
        # 1. Aşama: Makale Çekme
        with st.status("📚 Retrieving papers from arXiv API...", expanded=True) as status:
            chunks = retriever.retrieve_chunks(user_query, limit=2)
            if not chunks:
                status.update(label="No sources found.", state="error")
                st.stop()
            st.write(f"✅ Successfully retrieved {len(chunks)} papers.")
            status.update(label="Papers Retrieved!", state="complete", expanded=False)

        # 2. Aşama: Taslak Cümleler Üretme
        with st.status("🧠 Synthesising initial draft claims...", expanded=True) as status:
            draft_claims = synthesiser.generate_draft(chunks, user_query)
            st.write(f"✅ Generated {len(draft_claims)} draft claims.")
            status.update(label="Drafting Complete!", state="complete", expanded=False)

        # 3. Aşama: NLI Hakem Kontrolü ve Düzeltme
        st.subheader("⚖️ Verification & Refinement Process")
        
        for claim in draft_claims:
            claim_expander = st.expander(f"Processing {claim['claim_id']}: {claim['claim'][:50]}...", expanded=True)
            
            with claim_expander:
                iteration = 0
                passed = False
                max_iterations = 3
                
                while iteration < max_iterations and not passed:
                    st.write(f"**Attempt {iteration + 1}/{max_iterations}**")
                    
                    # Hakem Kontrolü
                    nli_result = nli_verifier.check_entailment(claim)
                    st.caption(f"NLI Score: {nli_result['score']:.2f} (Threshold: 0.20)")
                    
                    passed = arbiter.evaluate(claim, nli_result)
                    
                    if passed:
                        st.success(f"✅ PASSED. Claim verified by Formal Arbiter.")
                        final_approved_claims.append(claim)
                    else:
                        iteration += 1
                        if iteration < max_iterations:
                            st.warning("⚠️ FAILED. Claim rejected. Routing to Refinement Agent...")
                            # Düzeltmen Devrede
                            with st.spinner("Refining claim..."):
                                claim = refiner.refine_claim(claim, nli_result)
                                st.info(f"🔄 Refined Claim: {claim['claim']}")
                        else:
                            st.error(f"❌ FATAL. Claim failed {max_iterations} times. Dropped to prevent hallucination!")
                            
        st.divider()
        
 # 4. Aşama: FİNAL EKRANI
        st.subheader("🏆 FINAL ACADEMIC SYNTHESIS (100% VERIFIED)")
        if final_approved_claims:
            for c in final_approved_claims:
                doi_raw = c['source_chunk']['doi']
                
                # DOI formatına göre otomatik tıklanabilir link oluşturma
                if doi_raw.startswith("10."):
                    url = f"https://doi.org/{doi_raw}"
                elif doi_raw.startswith("arXiv:"):
                    arxiv_id = doi_raw.replace("arXiv:", "")
                    url = f"https://arxiv.org/abs/{arxiv_id}"
                else:
                    # Ne olur ne olmaz, bilinmeyen bir format gelirse Google'da arat
                    url = f"https://www.google.com/search?q={doi_raw}"
                
                # Streamlit Markdown ile tıklanabilir link basıyoruz
                st.info(f"**{c['claim']}** \n\n🔗 **Source:** [{doi_raw}]({url})")
                
            st.balloons() # Başarı animasyonu!
        else:
            st.error("No claims survived the strict verification process. Please try a different query.")