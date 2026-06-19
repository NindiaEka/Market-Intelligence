from playwright.sync_api import sync_playwright

url = (
    "https://www.idx.co.id/"
    "primary/ListedCompany/"
    "GetFinancialReport"
    "?periode=TW1"
    "&year=2026"
    "&indexFrom=0"
    "&pageSize=1000"
    "&reportType=rdf"
    "&kodeEmiten=AADI"
)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(url)

    print(page.content())

    browser.close()