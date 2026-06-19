from google import genai

from src.fact_extraction.models import (CompanyFacts)
from src.capability_detection.models import (CapabilityDetectionResult)
from src.capability_detection.capability_library import (CAPABILITY_LIBRARY)


class GeminiCapabilityDetector:

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def detect(self, facts: CompanyFacts) -> CapabilityDetectionResult:
        capability_list = "\n".join(f"- {item}" for item in CAPABILITY_LIBRARY)

        prompt = f"""
        Analyze the company's products, services,
        and business activities.

        Company:
        {facts.company_name}

        Description:
        {facts.description}

        Industry:
        {facts.industry}

        Products & Services:
        {facts.products_services}

        Only choose capabilities from
        the following list:

        {capability_list}

        Identify the business capabilities
        required to operate the company's
        products, services, and business activities.

        Prioritize:
        1. Products & Services
        2. Business Activities
        3. Company Description

        Do not infer capabilities solely
        from industry classification.

        IMPORTANT:

        - Only choose capabilities from the provided list.
        - Return capability names exactly as provided.
        - Write all reasons in Indonesian.
        - Return only the most relevant capabilities.

        Provide:

        - name
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
                    CapabilityDetectionResult,
                }
            )
        )

        return response.parsed