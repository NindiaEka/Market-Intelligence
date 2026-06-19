from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class IDXCompany:
    ticker: str
    company_name: str

@dataclass
class IDXCompanyProfile:

    ticker: str
    company_name: str

    sector: str
    sub_sector: str
    industry: str

    website: str
    email: str
    phone: str

    address: str

    listing_board: str
    listing_date: str

class FinancialAttachment(BaseModel):
    file_name: str
    file_path: str
    file_type: str


class FinancialReport(BaseModel):
    ticker: str
    company_name: str

    year: int
    period: str

    attachments: list[FinancialAttachment]

class FinancialHighlights(BaseModel):

    revenue: float | None = None

    net_income: float | None = None

    total_assets: float | None = None

    total_liabilities: float | None = None

    total_equity: float | None = None
    
@dataclass
class FinancialIntelligenceResult:

    company: IDXCompany | None
    profile: IDXCompanyProfile | None
    financial_report: FinancialReport | None
    financial_highlights: FinancialHighlights | None


