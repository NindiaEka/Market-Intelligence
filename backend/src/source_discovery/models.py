from pydantic import BaseModel
from typing import Optional

class CompanySources(BaseModel):
    company_name: str
    candidate_websites: list[str] = []
    linkedin_url: Optional[str] = None
    news_urls: list[str] = []