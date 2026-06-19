from .resolver import CompanyResolver
from .models import CompanyCandidate


class MockCompanyResolver(CompanyResolver):

    def resolve(
        self,
        company_name: str
    ) -> list[CompanyCandidate]:

        if company_name.lower() == "pertamina":
            return [
                CompanyCandidate(
                    name="PT Pertamina (Persero)",
                    industry="Oil & Gas",
                    website="https://www.pertamina.com"
                ),
                CompanyCandidate(
                    name="Pertamina Hulu Energi",
                    industry="Upstream Oil & Gas",
                    website="https://phe.pertamina.com"
                ),
                CompanyCandidate(
                    name="Pertamina EP",
                    industry="Exploration & Production",
                    website="https://pep.pertamina.com"
                )
            ]

        return [
            CompanyCandidate(
                name=company_name
            )
        ]