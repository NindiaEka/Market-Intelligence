from playwright.sync_api import sync_playwright

url = "https://www.idx.co.id/Portals/0/StaticData/ListedCompanies/Corporate_Actions/New_Info_JSX/Jenis_Informasi/01_Laporan_Keuangan/02_Soft_Copy_Laporan_Keuangan//Laporan%20Keuangan%20Tahun%202026/TW1/AADI/FinancialStatement-2026-I-AADI.xlsx"

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        accept_downloads=True
    )

    page = context.new_page()

    def handle_download(download):

        print(
            "DOWNLOAD:",
            download.suggested_filename
        )

        download.save_as(
            download.suggested_filename
        )

    page.on(
        "download",
        handle_download
    )

    try:

        page.goto(url)

    except Exception as e:

        print(e)

    page.wait_for_timeout(10000)

    browser.close()