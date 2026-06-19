from .templates import (
    COMPANY_BRIEF_TEMPLATE
)

from src.fact_extraction.models import (
    CompanyFacts
)


class CompanyBriefGenerator:

    def markdown_list(
        self,
        items
    ):

        return "\n".join(
            f"- {item}"
            for item in items
        )

    def markdown_capabilities(
        self,
        capabilities
    ):

        return "\n\n".join(
            (
                f"### {item.name}\n\n"
                f"{item.reason}"
            )
            for item in capabilities
        )

    def markdown_technology_needs(
        self,
        technology_needs
    ):

        return "\n\n".join(
            (
                f"### {item.category}\n\n"
                f"{item.reason}"
            )
            for item in technology_needs
        )

    def format_currency(
        self,
        value
    ):

        if value is None:
            return "N/A"

        if value >= 1_000_000:
            return (
                f"Rp {value / 1_000_000:.2f} "
                "Triliun"
            )

        if value >= 1_000:
            return (
                f"Rp {value / 1_000:.2f} "
                "Miliar"
            )

        return f"Rp {value:,.0f}"

    def generate(
        self,
        facts: CompanyFacts
    ) -> str:

        industry = (
            self.markdown_list(
                facts.industry
            )
        )

        products_services = (
            self.markdown_list(
                facts.products_services
            )
        )

        partnerships = (
            self.markdown_list(
                facts.partnerships
            )
        )

        available_documents = (
            self.markdown_list(
                facts.available_documents
            )
        )

        business_capabilities = (
            self.markdown_capabilities(
                facts.business_capabilities
            )
        )

        technology_needs = (
            self.markdown_technology_needs(
                facts.technology_needs
            )
        )

        investor_relations = (
            "Available"
            if facts.investor_relations
            else "Not Available"
        )

        return COMPANY_BRIEF_TEMPLATE.format(
            company_name=facts.company_name,

            description=facts.description or "N/A",

            ticker=facts.ticker or "N/A",

            sector=facts.sector or "N/A",

            sub_sector=facts.sub_sector or "N/A",

            listing_board=facts.listing_board or "N/A",

            latest_financial_period=(
                facts.latest_financial_period
                or "N/A"
            ),

            revenue=self.format_currency(
                facts.revenue
            ),

            net_income=self.format_currency(
                facts.net_income
            ),

            total_assets=self.format_currency(
                facts.total_assets
            ),

            total_liabilities=self.format_currency(
                facts.total_liabilities
            ),

            total_equity=self.format_currency(
                facts.total_equity
            ),

            industry=industry or "N/A",

            headquarters=(
                facts.headquarters
                or "N/A"
            ),

            products_services=(
                products_services
                or "N/A"
            ),

            business_capabilities=(
                business_capabilities
                or "N/A"
            ),

            technology_needs=(
                technology_needs
                or "N/A"
            ),

            partnerships=(
                partnerships
                or "N/A"
            ),

            investor_relations=(
                investor_relations
            ),

            available_documents=(
                available_documents
                or "N/A"
            ),
        )