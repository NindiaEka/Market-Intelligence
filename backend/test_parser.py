from src.financial_intelligence.financial_parser import (
    FinancialParser
)

parser = FinancialParser()

result = parser.extract_highlights(
    "FinancialStatement-2026-I-AADI.xlsx"
)

print(result)