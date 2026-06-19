import re

from src.fact_extraction.models import (CompanyFacts)


class LinkedInFallbackExtractor:

    def extract(self, markdown: str, company_name: str) -> CompanyFacts:

        facts = CompanyFacts(company_name=company_name)

        # Industry
        industry_match = re.search(r"##\s+([^\n]+)\n###", markdown)

        if industry_match:

            facts.industry = [industry_match.group(1).strip()]

        # Description
        description_match = re.search(r"####\s+([^\n]+)", markdown)

        if description_match:

            facts.description = (description_match.group(1).strip())

        # Headquarters
        headquarters_match = re.search(r"###\s+([^\n]+followers)", markdown)

        if headquarters_match:

            headquarters = (
                headquarters_match
                .group(1)
                .replace("followers", "")
                .strip()
            )

            facts.headquarters = (
                headquarters
            )

        # Products & Services
        specialties_match = re.search(
            r"Specialties\s+(.*?)\n##",
            markdown,
            re.DOTALL
        )

        if specialties_match:

            specialties = (
                specialties_match
                .group(1)
                .strip()
            )

            facts.products_services = [
                item.strip()
                for item in specialties.split(",")
                if item.strip()
            ]

        return facts