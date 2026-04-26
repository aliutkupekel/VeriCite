# VeriCite: A Formally Constrained Multi-Agent LLM Framework
A Formally Constrained Multi-Agent LLM Framework for NLI-Verified Academic Synthesis.

## Project Overview
VeriCite is a multi-agent system designed to generate NLI-verified academic synthesis. It strictly addresses AI hallucination by enforcing a formal Natural Language Inference (NLI) gate.

## System Architecture & Modules
Based on our approved proposal, the system consists of the following baseline modules:
1. **Retriever Agent:** Hybrid dense-sparse retrieval (RAG + Chunking).
2. **Synthesiser Agent:** Draft generation based on retrieved chunks.
3. **NLI Verifier Agent:** Entailment checking using a dedicated Cross-Encoder model.
4. **Formal Arbiter:** The strict logic gate that enforces the $\tau \geq 0.85$ confidence threshold.
5. **Refinement Agent:** Targeted rewriting (Max $k=3$ iterations).

## Scope & Requirements (Finalized)
- **In-Scope:** Text-based academic claim synthesis, PDF/text document ingestion, multi-agent pipeline orchestration, NLI-based fact verification.
- **Out-of-Scope:** Image/video generation, unstructured web scraping, real-time database updates.
- **Tech Stack Baseline:** Python 3.10+, LangChain/AutoGen (for agent orchestration), SentenceTransformers (for NLI), FAISS/ChromaDB (for vector storage).

## Contributors
* Ali Utku Pekel
* Alperen Atalay