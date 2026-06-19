from .crawl4ai_crawler import Crawl4AICrawler
from .models import (
    PageLink,
    CombinedCrawlResult
)


class MultiPageCrawler:

    def __init__(self):
        self.crawler = Crawl4AICrawler()

    def crawl(
        self,
        links: list[PageLink]
    ) -> CombinedCrawlResult:

        markdown_parts = []
        crawled_urls = []

        for link in links:

            print(
                f"Crawling: {link.title}"
            )

            result = self.crawler.crawl(
                link.url
            )

            markdown_parts.append(
                f"\n\n# {link.title}\n\n"
            )

            markdown_parts.append(
                result.markdown
            )

            crawled_urls.append(
                link.url
            )

        return CombinedCrawlResult(
            markdown="\n".join(
                markdown_parts
            ),
            crawled_urls=crawled_urls
        )