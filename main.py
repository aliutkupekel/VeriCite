import sys
import os

# Add src to Python path so we can import modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.pipeline import run_vericite_pipeline

if __name__ == "__main__":
    # Simulate a user asking a question
    sample_query = "How do multi-agent systems stop AI from hallucinating?"
    run_vericite_pipeline(sample_query)