# test_service.py

from financial_intelligence.service import (
    FinancialIntelligenceService
)

service = FinancialIntelligenceService()

result = service.get_company_data(
    "Adaro"
)

print(result.financial_highlights)
