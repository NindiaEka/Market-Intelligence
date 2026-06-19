import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from capability_detection.anthropic_capability_detector import AnthropicCapabilityDetector
from fact_extraction.anthropic_extractor import AnthropicFactExtractor
from src.capability_detection.fallback_detector import FallbackCapabilityDetector
from src.source_discovery.tavily_discovery import (TavilySourceDiscovery)
from src.crawler.crawl4ai_crawler import (Crawl4AICrawler)
from src.crawler.link_extractor import (LinkExtractor)
from src.crawler.important_link_selector import (ImportantLinkSelector)
from src.crawler.multi_page_crawler import (MultiPageCrawler)
from src.crawler.markdown_cleaner import (MarkdownCleaner)
from src.fact_extraction.gemini_extractor import (GeminiFactExtractor)
from src.fact_extraction.openai_extractor import (OpenAIFactExtractor)
from src.report_generator.generator import (CompanyBriefGenerator)
from src.financial_intelligence.service import (FinancialIntelligenceService)
from src.capability_detection.gemini_capability_detector import (GeminiCapabilityDetector)
from src.capability_detection.openai_capability_detector import (OpenAICapabilityDetector)
from src.technology_needs.gemini_technology_detector import (GeminiTechnologyDetector)
from src.technology_needs.openai_technology_detector import (OpenAITechnologyDetector)
from src.fact_extraction.linkedin_fallback_extractor import (LinkedInFallbackExtractor)
from src.technology_needs.fallback_detector import (FallbackTechnologyDetector)
from src.fact_extraction.fallback_detector import (FallbackExtractor)
from technology_needs.anthropic_technology_detector import AnthropicTechnologyDetector
from src.website_validation.validator import (WebsiteValidator)
from src.website_validation.website_filter import (WebsiteFilter)


class MarketIntelligencePipeline:

    def __init__(self):

        load_dotenv()

        self.discovery = (
            TavilySourceDiscovery(
                api_key=os.getenv(
                    "TAVILY_API_KEY"
                )
            )
        )

        self.crawler = (Crawl4AICrawler())

        self.link_extractor = (LinkExtractor())

        self.multi_page_crawler = (MultiPageCrawler())

        self.cleaner = (MarkdownCleaner())

        self.fallback_extractor = (
            FallbackExtractor(
                [
                    GeminiFactExtractor(
                        api_key=os.getenv(
                            "GOOGLE_API_KEY"
                        )
                    ),
                    OpenAIFactExtractor(
                        api_key=os.getenv(
                            "OPENAI_API_KEY"
                        )
                    ),
                    AnthropicFactExtractor(
                        api_key=os.getenv(
                            "ANTHROPIC_API_KEY"
                        )
                    )
                ]
            )
        )

        self.report_generator = (CompanyBriefGenerator())
        
        self.financial_service = (FinancialIntelligenceService())
        
        self.capability_detector = (
            FallbackCapabilityDetector(
                [
                    GeminiCapabilityDetector(
                        api_key=os.getenv(
                            "GOOGLE_API_KEY"
                        )
                    ),
                    OpenAICapabilityDetector(
                        api_key=os.getenv(
                            "OPENAI_API_KEY"
                        )
                    ),
                    AnthropicCapabilityDetector(
                        api_key=os.getenv(
                            "ANTHROPIC_API_KEY"
                        )
                    )
                ]
            )
        )
        
        self.technology_detector = (
            FallbackTechnologyDetector(
                [
                    GeminiTechnologyDetector(
                        api_key=os.getenv(
                            "GOOGLE_API_KEY"
                        )
                    ),
                    OpenAITechnologyDetector(
                        api_key=os.getenv(
                            "OPENAI_API_KEY"
                        )
                    ),
                    AnthropicTechnologyDetector(
                        api_key=os.getenv(
                            "ANTHROPIC_API_KEY"
                        )
                    )
                ]
            )
        )
        
        self.linkedin_fallback = (LinkedInFallbackExtractor())
        self.website_validator = (WebsiteValidator())
        self.website_filter = (WebsiteFilter())

    def is_poor_content(self, markdown: str) -> bool:
        return len(markdown.strip()) < 500

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------

    def run(self, company_name: str) -> str:
        """Run the full pipeline for a single company and return the generated brief."""

        filename = self._build_filename(company_name)
        cache_file = Path("cache") / f"{filename}.md"

        if cache_file.exists():
            print("\n⚡ Loaded from cache")
            return cache_file.read_text(encoding="utf-8")

        print(f"\nProcessing: {company_name}")

        financial_data = self.resolve_financial_data(company_name)
        website, sources = self.discover_sources(company_name, financial_data)

        facts = None
        use_linkedin_only = False
        links: list = []

        if website is None:
            facts = self._extract_via_linkedin(sources, company_name)
            if facts is None:
                raise ValueError("No website and no LinkedIn found.")
            use_linkedin_only = True

        else:
            links, is_valid = self.validate_website(website)

            if not is_valid:
                website, links, is_valid, sources = self.recover_website(company_name)

                if not is_valid:
                    fallback_name = (
                        financial_data.profile.company_name
                        if financial_data.profile
                        else company_name
                    )
                    facts = self._extract_via_linkedin(sources, fallback_name)
                    if facts is None:
                        raise ValueError("No valid website and no LinkedIn found.")
                    use_linkedin_only = True

        if not use_linkedin_only:
            facts = self.extract_company_facts(
                website=website,
                links=links,
                sources=sources,
                financial_data=financial_data,
                company_name=company_name,
                filename=filename,
            )

        facts = self._merge_financial_data(facts, financial_data)

        print("\n=== COMPANY FACTS ===\n")
        print(facts.model_dump_json(indent=4))

        facts = self.detect_capabilities(facts)
        facts = self.detect_technology_needs(facts)

        report = self.generate_report(facts, filename)

        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(report, encoding="utf-8")
        print("\n💾 Report cached")

        return report

    # ------------------------------------------------------------------
    # Pipeline steps (see diagram in PR description / docstring of run())
    # ------------------------------------------------------------------

    def resolve_financial_data(self, company_name: str):
        """Look up IDX (Indonesia Stock Exchange) data for the company, if it is listed."""

        print("\n=== IDX COMPANIES COUNT ===")
        print(len(self.financial_service.resolver.companies))

        resolved = self.financial_service.resolver.resolve(company_name)
        print("\n=== IDX RESOLVE ===")
        print(resolved)

        financial_data = self.financial_service.get_company_data(company_name)
        return financial_data

    def discover_sources(self, company_name: str, financial_data):
        """Resolve the company's website: use the IDX profile if listed, otherwise
        discover candidate sources via web search and pick the first one that
        passes the company-website filter.

        Returns (website, sources). `sources` is None for the IDX-profile path,
        since no discovery call is made in that case.
        """

        if financial_data.profile:
            website = financial_data.profile.website

            if not website.startswith(("http://", "https://")):
                website = f"https://{website}"

            print(f"\nUsing IDX Website: {website}")
            return website, None

        sources = self.discovery.discover(company_name)
        print("\n=== SOURCES ===")
        print(sources)

        website = None
        for candidate in sources.candidate_websites:
            if self.website_filter.is_company_website(candidate):
                website = candidate
                break

        return website, sources

    def validate_website(self, website: str):
        """Crawl the candidate website once and check whether its content looks
        like a genuine company site. Returns (links, is_valid).
        """

        crawl_result = self.crawler.crawl(website)
        print("\n=== CRAWL SUCCESS ===")
        print(crawl_result.url)

        links = self.link_extractor.extract(crawl_result.markdown)
        print(f"\n=== FOUND {len(links)} LINKS ===")

        is_valid = self.website_validator.is_valid(
            markdown=crawl_result.markdown,
            links_count=len(links),
        )
        print(f"Valid: {is_valid}")

        return links, is_valid

    def recover_website(self, company_name: str):
        """Called when the initial website fails validation. Re-runs discovery
        and tries each candidate until one passes validation.

        Returns (website, links, is_valid, sources). `website` and `is_valid`
        reflect whether a recovery candidate was found; `is_valid` is False
        (with website=None) if none passed.
        """

        print("\nWebsite invalid. Trying website recovery...")
        sources = self.discovery.discover(company_name)

        for candidate in sources.candidate_websites:
            print(f"\nRecovery candidate: {candidate}")

            if not self.website_filter.is_company_website(candidate):
                print(f"Rejected recovery source: {candidate}")
                continue

            print(f"\nAccepted recovery source: {candidate}")

            try:
                crawl_result = self.crawler.crawl(candidate)
                if not crawl_result.markdown:
                    print("\nEmpty crawl result.")
                    continue

            except Exception as e:
                print(f"\nCrawl failed: {e}")
                continue

            links = self.link_extractor.extract(crawl_result.markdown)
            print(f"\n=== RECOVERY FOUND {len(links)} LINKS ===")

            is_valid = self.website_validator.is_valid(
                markdown=crawl_result.markdown,
                links_count=len(links),
            )

            if is_valid:
                print(f"\nRecovered Website: {candidate}")
                return candidate, links, True, sources

        print("\nNo valid recovery website found.")
        return None, [], False, sources

    def extract_company_facts(self, website, links, sources, financial_data, company_name, filename):
        """Crawl the website's most important pages, combine + clean the markdown,
        save it to disk, and extract structured company facts from it.
        """

        selector = ImportantLinkSelector(base_domain=urlparse(website).netloc)
        important_links = selector.select(links)
        print(f"\n=== SELECTED {len(important_links)} IMPORTANT LINKS ===")

        combined_result = self.multi_page_crawler.crawl(important_links)
        combined_markdown = combined_result.markdown

        if (
            self.is_poor_content(combined_markdown)
            and not financial_data.profile
            and sources
            and sources.linkedin_url
        ):
            print("\nWebsite content insufficient.")
            print("Trying LinkedIn...")

            linkedin_result = self.crawler.crawl(sources.linkedin_url)
            combined_markdown += "\n\n" + linkedin_result.markdown

        cleaned_markdown = self.cleaner.clean(combined_markdown)

        markdown_path = f"{filename}_cleaned.md"
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(cleaned_markdown)
        print(f"\nSaved: {markdown_path}")

        try:
            facts = self.fallback_extractor.extract(cleaned_markdown)

        except Exception as e:
            print(f"\nFact extraction failed: {e}")
            print("\nTrying LinkedIn fallback extraction...")

            facts = self.linkedin_fallback.extract(
                markdown=cleaned_markdown,
                company_name=(
                    financial_data.profile.company_name
                    if financial_data.profile
                    else company_name
                ),
            )

        return facts

    def detect_capabilities(self, facts):
        """Detect business capabilities from the extracted facts, when there's
        enough signal to work with. Always sets facts.business_capabilities.
        """

        has_company_data = (
            bool(facts.description)
            or len(facts.industry) > 0
            or len(facts.products_services) > 0
        )

        if not has_company_data:
            print("\nInsufficient company data. Skipping capability detection.")
            facts.business_capabilities = []
            return facts

        try:
            capabilities = self.capability_detector.detect(facts)
            facts.business_capabilities = capabilities.capabilities
            print(f"\nDetected {len(facts.business_capabilities)} business capabilities")

        except Exception as e:
            print(f"\nCapability detection failed: {e}")
            facts.business_capabilities = []

        print("\n=== BUSINESS CAPABILITIES ===\n")
        for capability in facts.business_capabilities:
            print(capability.model_dump())

        return facts

    def detect_technology_needs(self, facts):
        """Detect technology needs from the detected business capabilities.
        Always sets facts.technology_needs.
        """

        if not facts.business_capabilities:
            print("\nNo business capabilities found. Skipping technology detection.")
            facts.technology_needs = []
            return facts

        try:
            technology_needs = self.technology_detector.detect(facts)
            facts.technology_needs = technology_needs.technology_needs
            print(f"\nDetected {len(facts.technology_needs)} technology needs")

        except Exception as e:
            print(f"\nTechnology detection failed: {e}")
            facts.technology_needs = []

        print("\n=== TECHNOLOGY NEEDS ===\n")
        for item in facts.technology_needs:
            print(item.model_dump())

        return facts

    def generate_report(self, facts, filename: str) -> str:
        """Render the final company brief and save it to disk."""

        report = self.report_generator.generate(facts)

        report_path = f"{filename}_brief.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\nCompany brief saved to {report_path}")
        return report

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_filename(self, company_name: str) -> str:
        return (
            company_name
            .lower()
            .strip()
            .replace(".", "")
            .replace(" ", "_")
        )

    def _extract_via_linkedin(self, sources, fallback_company_name: str):
        """Crawl the LinkedIn page (if any) and extract facts from it.
        Returns None if there's no LinkedIn URL to fall back to.
        """

        if not (sources and sources.linkedin_url):
            return None

        print("\nTrying LinkedIn fallback...")
        linkedin_result = self.crawler.crawl(sources.linkedin_url)

        return self.linkedin_fallback.extract(
            markdown=linkedin_result.markdown,
            company_name=fallback_company_name,
        )

    def _merge_financial_data(self, facts, financial_data):
        """Overlay IDX financial data onto the extracted facts, and fill in a
        generic description if the extractor didn't produce one.
        """

        if financial_data.company:
            facts.ticker = financial_data.company.ticker

        if financial_data.profile:
            facts.sector = financial_data.profile.sector
            facts.sub_sector = financial_data.profile.sub_sector
            facts.listing_board = financial_data.profile.listing_board

        if financial_data.financial_report:
            facts.latest_financial_period = (
                f"{financial_data.financial_report.period} "
                f"{financial_data.financial_report.year}"
            )

        if financial_data.financial_highlights:
            facts.revenue = financial_data.financial_highlights.revenue
            facts.net_income = financial_data.financial_highlights.net_income
            facts.total_assets = financial_data.financial_highlights.total_assets
            facts.total_liabilities = financial_data.financial_highlights.total_liabilities
            facts.total_equity = financial_data.financial_highlights.total_equity

        if not facts.description:
            if facts.sector and facts.sub_sector:
                facts.description = (
                    f"{facts.company_name} merupakan perusahaan pada sektor "
                    f"{facts.sector} dengan fokus pada {facts.sub_sector}."
                )
            elif facts.industry:
                facts.description = (
                    f"{facts.company_name} merupakan perusahaan yang bergerak "
                    f"di bidang {facts.industry[0]}."
                )

        return facts
