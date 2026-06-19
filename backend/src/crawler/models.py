from pydantic import BaseModel


class CrawlResult(BaseModel):
    url: str
    markdown: str

class PageLink(BaseModel):
    title: str
    url: str

class CombinedCrawlResult(BaseModel):
    markdown: str
    crawled_urls: list[str]
    