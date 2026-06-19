from crawl4ai import AsyncWebCrawler

from .crawler import Crawler
from .models import CrawlResult

import asyncio


class Crawl4AICrawler(Crawler):

    async def _crawl_async(
        self,
        url: str
    ) -> CrawlResult:

        try:

            async with AsyncWebCrawler() as crawler:

                result = await crawler.arun(
                    url=url
                )

                return CrawlResult(
                    url=result.url or url,
                    markdown=result.markdown or ""
                )

        except Exception as e:

            print(
                f"Crawl failed: {url}"
            )

            print(e)

            return CrawlResult(
                url=url,
                markdown=""
            )

    def crawl(
        self,
        url: str
    ) -> CrawlResult:

        return asyncio.run(
            self._crawl_async(url)
        )