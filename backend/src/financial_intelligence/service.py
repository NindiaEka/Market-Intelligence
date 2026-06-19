from financial_intelligence.idx_client import (
    IDXClient
)

from financial_intelligence.idx_resolver import (
    IDXResolver
)

from financial_intelligence.financial_parser import (
    FinancialParser
)

from financial_intelligence.models import (
    FinancialIntelligenceResult
)


class FinancialIntelligenceService:

    def __init__(self):

        self.client = IDXClient()
        self.resolver = IDXResolver()
        self.parser = FinancialParser()

    def get_company_data(
        self,
        company_name: str,
        year: int = 2026,
        period: str = "TW1",
    ):

        company = self.resolver.resolve(
            company_name
        )

        if company is None:

            return FinancialIntelligenceResult(
                company=None,
                profile=None,
                financial_report=None,
                financial_highlights=None,
            )

        profile = self.client.get_company_profile(
            company.ticker
        )

        report = self.client.get_financial_report(
            ticker=company.ticker,
            year=year,
            period=period,
        )

        highlights = None

        if report:

            xlsx_file = next(
                (
                    attachment
                    for attachment in report.attachments
                    if attachment.file_type == ".xlsx"
                ),
                None
            )

            if xlsx_file:

                file_path = (
                    self.client.download_attachment(
                        xlsx_file
                    )
                )

                highlights = (
                    self.parser.extract_highlights(
                        file_path
                    )
                )

        return FinancialIntelligenceResult(
            company=company,
            profile=profile,
            financial_report=report,
            financial_highlights=highlights,
        )