import sys
import os

# Add src to Python path so we can import modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.pipeline import run_vericite_pipeline

if __name__ == "__main__":
    print("\n" + "="*50)
    print(" Welcome to VeriCite - NLI Verified Academic Synthesis")
    print(" Type 'exit' to stop the engine.")
    print("="*50 + "\n")

    while True:
        # Get dynamic input from the user
        user_query = input("\n[User] Enter your academic research topic: ")
        
        if user_query.lower() in ['exit', 'quit']:
            print("\nShutting down VeriCite. Goodbye!")
            break
            
        if not user_query.strip():
            continue
            
        # Run the pipeline with the user's custom query
        run_vericite_pipeline(user_query)