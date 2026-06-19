# test_profile.py

from financial_intelligence.idx_client import IDXClient

client = IDXClient()

profile = client.get_company_profile(
    "AADI")

print(profile)