import os
from src.source_discovery.tavily_discovery import (TavilySourceDiscovery)
from src.crawler.crawl4ai_crawler import (Crawl4AICrawler)
from dotenv import load_dotenv

load_dotenv()

discovery = (
    TavilySourceDiscovery(
        api_key=os.getenv(
            "TAVILY_API_KEY"
        )
    )
)

sources = discovery.discover(
    "Telkomsel"
)

print(
    "LINKEDIN:",
    sources.linkedin_url
)

crawler = Crawl4AICrawler()

result = crawler.crawl(
    sources.linkedin_url
)

print("\nURL:")
print(result.url)

print("\nMARKDOWN:")
print(result.markdown[:3000])