import json
import random
from typing import Dict

class SEOFetcher:
    def __init__(self):
        # Mock data for demonstration
        self.mock_data = {
            "wireless earbuds": {
                "search_volume": 110000,
                "keyword_difficulty": 65,
                "avg_cpc": 2.50
            },
            "best headphones": {
                "search_volume": 90500,
                "keyword_difficulty": 70,
                "avg_cpc": 3.20
            },
            "noise cancelling headphones": {
                "search_volume": 82300,
                "keyword_difficulty": 68,
                "avg_cpc": 2.80
            }
        }
 
    def get_seo_data(self, keyword: str) -> Dict:
        """
        Get SEO data for a given keyword.
        If keyword exists in mock data, return it. Otherwise, generate random data.
        """
        if keyword.lower() in self.mock_data:
            return self.mock_data[keyword.lower()]
        
        # Generate random data for unknown keywords
        return {
            "search_volume": random.randint(1000, 100000),
            "keyword_difficulty": random.randint(1, 100),
            "avg_cpc": round(random.uniform(0.5, 5.0), 2)
        }

    def save_seo_data(self, keyword: str, data: Dict):
        """Save SEO data for a keyword (for future reference)"""
        self.mock_data[keyword.lower()] = data 