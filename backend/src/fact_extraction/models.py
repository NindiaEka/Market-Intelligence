from pydantic import BaseModel
from typing import List, Optional
from src.capability_detection.models import (BusinessCapability)
from src.technology_needs.models import (TechnologyNeed)

class CompanyFacts(BaseModel):

    company_name: str
    industry: list[str] = []
    description: Optional[str] = None
    headquarters: Optional[str] = None
    products_services: List[str] = []
    subsidiaries: List[str] = []
    partnerships: List[str] = []
    available_documents: List[str] = []
    investor_relations: bool = False
    ticker: Optional[str] = None
    sector: Optional[str] = None
    sub_sector: Optional[str] = None
    listing_board: Optional[str] = None
    latest_financial_period: Optional[str] = None
    revenue: float | None = None
    net_income: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    total_equity: float | None = None
    business_capabilities: list[BusinessCapability] = []
    technology_needs: list[TechnologyNeed] = []