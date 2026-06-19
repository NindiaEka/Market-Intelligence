from tavily import TavilyClient

from .resolver import CompanyResolver
from .models import CompanyCandidate


class TavilyCompanyResolver(CompanyResolver):

    def __init__(self, api_key: str):
        self.client = TavilyClient(api_key=api_key)

    def resolve(self, company_name: str) -> list[CompanyCandidate]:

        response = self.client.search(query=f"{company_name} company", max_results=10)

        candidates = []

        for result in response["results"]:

            candidates.append(
                CompanyCandidate(
                    name=result.get("title", ""),
                    website=result.get("url"),
                    description=result.get("content")
                )
            )

        return candidates