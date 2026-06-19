import json
from google import genai
from .models import CandidateExtractionResult


def _result_title(result):
    if isinstance(result, dict):
        return result.get("title", "") or result.get("name", "")

    if hasattr(result, "dict"):
        data = result.dict()
        return data.get("title", "") or data.get("name", "")

    return getattr(result, "name", "") or ""


class CandidateExtractor:

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def extract(self, search_results: list[dict]) -> CandidateExtractionResult:

        titles = [_result_title(result)
            for result in search_results]

        prompt = f"""
You are a company entity extractor.

Extract company entities from the search results.

Rules:
- Only extract companies.
- Ignore Wikipedia, LinkedIn, Bloomberg, directories, and news websites.
- Do not invent company names.
- Remove duplicates.

Search Results:

{titles}

Return JSON only using this schema:

{{
  "companies": [
    "Company Name"
  ]
}}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_text = response.text

        raw_text = (
            raw_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(raw_text)

        return CandidateExtractionResult(candidates=data.get("companies", []))