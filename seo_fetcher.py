import json
import random
from typing import Dict

class SEOFetcher:
    def __init__(self):
        self.mock_data = {
            "smart home hub": {
                "search_volume": 135000,
                "keyword_difficulty": 72,
                "avg_cpc": 3.80
            },
            "smart light bulbs": {
                "search_volume": 98500,
                "keyword_difficulty": 65,
                "avg_cpc": 2.90
            },
            "smart thermostat": {
                "search_volume": 89200,
                "keyword_difficulty": 68,
                "avg_cpc": 3.40
            }
        }
 
    def get_seo_data(self, keyword: str) -> Dict:
        """
        Get SEO data for a given keyword.
        If keyword exists in mock data, return it. Otherwise, generate random data.
        """
        if keyword.lower() in self.mock_data:
            return self.mock_data[keyword.lower()]
        
        return {
            "search_volume": random.randint(1000, 100000),
            "keyword_difficulty": random.randint(1, 100),
            "avg_cpc": round(random.uniform(0.5, 5.0), 2)
        }

    def save_seo_data(self, keyword: str, data: Dict):
        """Save SEO data for a keyword (for future reference)"""
        self.mock_data[keyword.lower()] = data 