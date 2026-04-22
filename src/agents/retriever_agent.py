import requests
import time

class RetrieverAgent:
    def __init__(self):
        self.name = "Retriever"
        self.api_url = "https://api.semanticscholar.org/graph/v1/paper/search"

    def retrieve_chunks(self, query, limit=2):
        print(f"[{self.name}]: Connecting to Semantic Scholar API for query: '{query}'")
        
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,abstract,externalIds,year"
        }
        
        # Adding a User-Agent to bypass strict 429 blocks. We tell the API we are an academic project.
        headers = {
            "User-Agent": "VeriCite/1.0 (Academic Research Project; student@university.edu)"
        }
        
        try:
            response = requests.get(self.api_url, params=params, headers=headers)
            
            # Retry mechanism: If we get a 429 Rate Limit, wait 5 seconds and try once more.
            if response.status_code == 429:
                print(f"[{self.name}]: API rate limit hit. Waiting 5 seconds to retry...")
                time.sleep(5)
                response = requests.get(self.api_url, params=params, headers=headers)
                
            response.raise_for_status()
            data = response.json()
            
            valid_chunks = []
            for paper in data.get('data', []):
                # We only accept papers that have an abstract and a DOI to prevent hallucination
                if paper.get('abstract') and paper.get('externalIds', {}).get('DOI'):
                    chunk = {
                        "title": paper['title'],
                        "abstract": paper['abstract'],
                        "doi": paper['externalIds']['DOI'],
                        "year": paper.get('year', 'N/A')
                    }
                    valid_chunks.append(chunk)
            
            print(f"[{self.name}]: Successfully retrieved {len(valid_chunks)} verified academic papers with DOIs.")
            return valid_chunks
            
        except Exception as e:
            print(f"[{self.name}]: API Error - {str(e)}")
            return []