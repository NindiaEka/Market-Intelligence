from tavily import TavilyClient

from .discovery import SourceDiscovery
from .models import CompanySources


class TavilySourceDiscovery(SourceDiscovery):

    def __init__(self, api_key: str):
        self.client = TavilyClient(
            api_key=api_key
        )

    def discover(
        self,
        company_name: str
    ) -> CompanySources:

        website_result = self.client.search(
            query=f"{company_name} corporate website",
            max_results=10
        )

        linkedin_result = self.client.search(
            query=f"{company_name} linkedin",
            max_results=5
        )

        BLOCKED_DOMAINS = [
            "linkedin.com",
            "instagram.com",
            "facebook.com",
            "twitter.com",
            "x.com",
        ]

        candidate_websites = []

        print("\n=== WEBSITE SEARCH RESULTS ===")

        for result in website_result["results"]:

            url = result["url"]

            print(url)

            # skip social media
            if any(
                blocked in url.lower()
                for blocked in BLOCKED_DOMAINS
            ):
                continue

            # skip duplicate
            if url in candidate_websites:
                continue

            candidate_websites.append(
                url
            )

        print(
            "\n=== CANDIDATE WEBSITES ==="
        )

        for url in candidate_websites:
            print(url)

        linkedin_url = None

        print(
            "\n=== LINKEDIN SEARCH RESULTS ==="
        )

        for result in linkedin_result["results"]:

            url = result["url"]

            print(url)

            if "linkedin.com/company" in url:

                linkedin_url = url
                break

        return CompanySources(
            company_name=company_name,
            candidate_websites=candidate_websites,
            linkedin_url=linkedin_url
        )