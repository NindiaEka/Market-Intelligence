from openai import OpenAI

from src.fact_extraction.models import (CompanyFacts)
from src.technology_needs.models import (TechnologyNeedsResult)

class OpenAITechnologyDetector:

    def __init__(self, api_key: str):

        self.client = OpenAI(api_key=api_key)

    def detect(self, facts: CompanyFacts) -> TechnologyNeedsResult:
        prompt = f"""
        Analyze the company profile.

        Company:
        {facts.company_name}

        Industry:
        {facts.industry}

        Products & Services:
        {facts.products_services}

        Business Capabilities:
        {facts.business_capabilities}

        Based on the information above,
        identify potential technology needs.

        ONLY CHOOSE FROM:

        - DevSecOps
        - Data Security
        - Data Management
        - PAM
        - Observability
        - Endpoint Security
        - AI & Cloud

        Do not recommend all categories.

        Only select categories that have strong business justification.

        Maximum 5 recommendations.

        IMPORTANT:
        Return category names exactly as provided above.
        Write all explanations and reasons in Indonesian.

        For each item provide:

        - category
          - reason
        """
        
        response = (
            self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        )

        return response.choices[0].message