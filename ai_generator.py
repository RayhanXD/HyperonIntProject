import os
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.affiliate_links = {
            "AFF_LINK_1": "https://amazon.com/affiliate/smart-home-hub",
            "AFF_LINK_2": "https://bestbuy.com/affiliate/smart-lights",
            "AFF_LINK_3": "https://walmart.com/affiliate/smart-thermostat"
        }

    def generate_blog_post(self, keyword: str, seo_data: Dict) -> str:
        """
        Generate a blog post using OpenAI's API based on the keyword and SEO data.
        """
        prompt = f"""Write a comprehensive blog post about {keyword}. 
        Include the following information:
        - Search Volume: {seo_data['search_volume']}
        - Keyword Difficulty: {seo_data['keyword_difficulty']}
        - Average CPC: ${seo_data['avg_cpc']}

        The post should:
        1. Be well-structured with H1, H2, and H3 headings
        2. Include an introduction, main sections, and conclusion
        3. Be informative and engaging
        4. Include 3 affiliate link placeholders using {{AFF_LINK_1}}, {{AFF_LINK_2}}, and {{AFF_LINK_3}}
        5. Be at least 1000 words long
        6. Include a meta description
        7. Be written in HTML format

        Format the response in HTML with proper tags."""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional SEO content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content = response.choices[0].message.content

        for placeholder, link in self.affiliate_links.items():
            content = content.replace(f"{{{placeholder}}}", link)

        return content 