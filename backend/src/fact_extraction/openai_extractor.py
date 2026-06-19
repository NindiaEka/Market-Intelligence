import json

from openai import OpenAI

from .extractor import FactExtractor
from .models import CompanyFacts

class OpenAIFactExtractor(FactExtractor):

    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key
        )

    def extract(
        self,
        markdown: str
    ) -> CompanyFacts:

        prompt = f"""
Extract factual company information from the markdown.

Rules:
- Only extract information explicitly stated.
- Do not infer.
- Do not invent.
- Do not use prior knowledge.
- For string fields, return null if unavailable.
- For list fields, return [] if unavailable.
- Remove duplicate values from lists.
- Return JSON only.

Description Rules:
- Extract a concise company overview.
- Prefer content from About Us, Company Profile,
  Company Overview, Tentang Perusahaan,
  atau Profil Perusahaan sections.
- Do not use slogans, taglines,
  marketing messages, or advertisements.

Products & Services Rules:
- Include only recurring commercial
  products and services offered by the company.
- Exclude:
  - promotions
  - campaigns
  - events
  - scholarships
  - CSR programs
  - contests
  - news
  - press releases
  - temporary programs

Available Documents Rules:
- Include only formal corporate documents.
- Examples:
  - Annual Report
  - Sustainability Report
  - Financial Report
  - Corporate Presentation
  - Investor Presentation
  - Governance Report
  - Company Profile
- Exclude:
  - news
  - press releases
  - announcements
  - articles
  - cookie notices
  - privacy policies
  - website pages

Extract ALL subsidiaries explicitly mentioned.
Extract ALL partnerships explicitly mentioned.

JSON Schema:

{{
    "company_name": "",
    "industry": [],
    "description": null,
    "headquarters": null,
    "products_services": [],
    "subsidiaries": [],
    "partnerships": [],
    "available_documents": [],
    "investor_relations": false
}}

Markdown:

{markdown[:30000]}
"""

        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        raw_text = (
            response.choices[0].message
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            data = json.loads(raw_text)

        except json.JSONDecodeError:
            print(raw_text)
            raise

        return CompanyFacts(**data)