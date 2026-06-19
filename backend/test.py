import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

from src.source_discovery.tavily_discovery import (
    TavilySourceDiscovery
)

from src.crawler.crawl4ai_crawler import (
    Crawl4AICrawler
)

from src.crawler.link_extractor import (
    LinkExtractor
)

from src.crawler.important_link_selector import (
    ImportantLinkSelector
)

from src.crawler.multi_page_crawler import (
    MultiPageCrawler
)

from src.crawler.markdown_cleaner import (
    MarkdownCleaner
)

from src.fact_extraction.gemini_extractor import (
    GeminiFactExtractor
)

from src.report_generator.generator import (
    CompanyBriefGenerator
)
dotenv_path = (
    Path(__file__).parent
    / "src"
    / "company_resolution"
    / ".env"
)

load_dotenv(dotenv_path)

# ==========================================
# Source Discovery
# ==========================================

discovery = TavilySourceDiscovery(
    api_key=os.getenv("TAVILY_API_KEY")
)

company_name = input(
    "Enter company name: "
)

sources = discovery.discover(
    company_name
)

print("\n=== SOURCES ===")
print(sources)

# ==========================================
# Crawl Homepage
# ==========================================

crawler = Crawl4AICrawler()

crawl_result = crawler.crawl(
    sources.official_website
)

print("\n=== CRAWL SUCCESS ===")
print(crawl_result.url)

with open(
    "output.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(crawl_result.markdown)

print("\nHomepage markdown saved to output.md")

# ==========================================
# Extract Links
# ==========================================

link_extractor = LinkExtractor()

links = link_extractor.extract(
    crawl_result.markdown
)

print(f"\n=== FOUND {len(links)} LINKS ===")

# ==========================================
# Select Important Links
# ==========================================

selector = ImportantLinkSelector(
    base_domain=urlparse(
        sources.official_website
    ).netloc
)

important_links = selector.select(
    links
)

print(
    f"\n=== SELECTED {len(important_links)} IMPORTANT LINKS ===\n"
)

for link in important_links:
    print(link)

# ==========================================
# Multi Page Crawl
# ==========================================

multi_page_crawler = MultiPageCrawler()

combined_result = (
    multi_page_crawler.crawl(
        important_links
    )
)

print(
    f"\nCombined markdown length: "
    f"{len(combined_result.markdown):,} chars"
)

# ==========================================
# Markdown Cleaning
# ==========================================

cleaner = MarkdownCleaner()

cleaned_markdown = cleaner.clean(
    combined_result.markdown
)

print(
    f"Cleaned markdown length: "
    f"{len(cleaned_markdown):,} chars"
)

with open(
    "combined_cleaned.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(cleaned_markdown)

print(
    "\nCleaned markdown saved to combined_cleaned.md"
)

# print(
#     "\n=== DEBUG ==="
# )

# keywords = [
#     "Pertamina Hulu Rokan",
#     "Pertamina EP",
#     "Exploration",
#     "Operation and Production"
# ]

# for keyword in keywords:
#     print(
#         keyword,
#         keyword in cleaned_markdown
#     )

# ==========================================
# Fact Extraction
# ==========================================

fact_extractor = GeminiFactExtractor(
    api_key=os.getenv("GOOGLE_API_KEY")
)

facts = fact_extractor.extract(
    cleaned_markdown
)

print("\n=== COMPANY FACTS ===\n")

print(
    facts.model_dump_json(
        indent=4
    )
)

generator = CompanyBriefGenerator()

report = generator.generate(
    facts
)

safe_name = (
    company_name
    .lower()
    .replace(" ", "_")
    .replace(".", "")
    .replace("/", "_")
)

filename = f"{safe_name}_brief.md"

with open(
    filename,
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

print(
    f"\nCompany brief saved to {filename}"
)