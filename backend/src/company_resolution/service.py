from .models import CompanyCandidate


class MockCompanyResolver:

    def resolve(self, company_name: str):

        if company_name.lower() == "pertamina":
            return [
                CompanyCandidate(name="PT Pertamina (Persero)"),
                CompanyCandidate(name="Pertamina Hulu Energi"),
                CompanyCandidate(name="Pertamina EP")
            ]

        return [CompanyCandidate(name=company_name)]