from financial_intelligence.idx_client import IDXClient
from financial_intelligence.models import IDXCompany
import re

def normalize(text: str):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9 ]",
        " ",
        text
    )

    text = " ".join(
        text.split()
    )

    return text

class IDXResolver:

    def __init__(self):
        self.client = IDXClient()
        self.companies = self._load_companies()

    def _load_companies(self):
        data = self.client.get_emiten()
        companies = []

        for item in data:
            companies.append(
                IDXCompany(
                    ticker=item["KodeEmiten"],
                    company_name=item["NamaEmiten"],
                )
            )
        return companies

    def resolve(self, query: str):

        query = normalize(query)

        for company in self.companies:

            company_name = normalize(company.company_name)

            if query == company.ticker.lower():
                return company
            if query in company_name:
                return company
        return None