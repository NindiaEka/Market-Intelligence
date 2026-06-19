# test_download.py

from financial_intelligence.idx_client import (
    IDXClient
)

client = IDXClient()

report = (
    client.get_financial_report(
        ticker="AADI",
        year=2026,
        period="TW1"
    )
)

xlsx_file = None

for attachment in report.attachments:

    if attachment.file_type == ".xlsx":

        xlsx_file = attachment
        break

path = (
    client.download_attachment(
        xlsx_file
    )
)

print(path)
print(xlsx_file.file_path)