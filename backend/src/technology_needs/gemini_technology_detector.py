from google import genai

from src.fact_extraction.models import (CompanyFacts)
from src.technology_needs.models import (TechnologyNeedsResult)

class GeminiTechnologyDetector:

    def __init__(self, api_key: str):

        self.client = genai.Client(api_key=api_key)
        
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
            self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type":
                    "application/json",

                    "response_schema":
                    TechnologyNeedsResult,
                }
            )
        )

        return response.parsed