from abc import ABC, abstractmethod

from .models import CrawlResult


class Crawler(ABC):

    @abstractmethod
    def crawl(self, url: str) -> CrawlResult:
        pass