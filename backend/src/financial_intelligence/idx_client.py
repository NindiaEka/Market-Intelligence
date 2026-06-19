import os
import json
import requests

from playwright.sync_api import sync_playwright
from financial_intelligence.models import (FinancialReport, FinancialAttachment, IDXCompanyProfile)
from html import unescape
from pathlib import Path


class IDXClient:

    BASE_URL = "https://www.idx.co.id"

    def _get_json(self, url: str):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/137.0.0.0 Safari/537.36"
                )
            )

            page = context.new_page()

            page.goto(url)

            page.wait_for_load_state(
                "networkidle"
            )

            content = page.content()

            start = content.find("<pre>")
            end = content.find("</pre>")

            raw_json = content[start + 5:end]

            browser.close()

            return json.loads(raw_json)

    def get_emiten(self):

        url = (
            f"{self.BASE_URL}"
            "/primary/Helper/GetEmiten"
            "?emitenType=s"
        )

        return self._get_json(url)
    
    def get_company_profile(self, ticker: str,):

        url = (
            f"{self.BASE_URL}"
            "/primary/ListedCompany/"
            f"GetCompanyProfilesDetail"
            f"?KodeEmiten={ticker}"
            "&language=id-id"
        )
        
        data = self._get_json(url)
        
        profile = data["Profiles"][0]

        return IDXCompanyProfile(
            ticker=profile["KodeEmiten"],
            company_name=unescape(profile["NamaEmiten"]),
            sector=unescape(profile["Sektor"]),
            sub_sector=unescape(profile["SubSektor"]),
            industry=unescape(profile["Industri"]),
            website=unescape(profile["Website"]),
            email=unescape(profile["Email"]),
            phone=unescape(profile["Telepon"]),
            address=unescape(profile["Alamat"]),
            listing_board=unescape(profile["PapanPencatatan"]),
            listing_date=profile["TanggalPencatatan"],
        )

    def get_financial_report(
        self,
        ticker: str,
        year: int,
        period: str,
    ):

        url = (
            f"{self.BASE_URL}"
            "/primary/ListedCompany/GetFinancialReport"
            f"?periode={period}"
            f"&year={year}"
            "&indexFrom=0"
            "&pageSize=1000"
            "&reportType=rdf"
            f"&kodeEmiten={ticker}"
        )

        data = self._get_json(url)

        if data["ResultCount"] == 0:
            return None

        result = data["Results"][0]

        attachments = []

        for item in result["Attachments"]:

            attachments.append(
                FinancialAttachment(
                    file_name=item["File_Name"],
                    file_path=item["File_Path"],
                    file_type=item["File_Type"],
                )
            )

        return FinancialReport(
            ticker=result["KodeEmiten"],
            company_name=result["NamaEmiten"],
            year=int(result["Report_Year"]),
            period=result["Report_Period"],
            attachments=attachments,
        )

    def download_attachment(
        self,
        attachment: FinancialAttachment,
        output_dir: str = "downloads",
    ):

        Path(output_dir).mkdir(
            parents=True,
            exist_ok=True
        )

        file_url = (
            f"{self.BASE_URL}"
            f"{attachment.file_path}"
        )

        output_path = (
            Path(output_dir)
            / attachment.file_name
        )
        
        if output_path.exists():

            print(
                f"Using cached file: {output_path}"
            )

            return str(output_path)

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            context = browser.new_context(
                accept_downloads=True,
                user_agent=(
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/137.0.0.0 "
                    "Safari/537.36"
                )
            )

            page = context.new_page()

            with page.expect_download() as download_info:

                try:
                    page.goto(file_url)

                except Exception as e:

                    # Normal untuk file download IDX
                    print(e)

            download = download_info.value

            download.save_as(
                str(output_path)
            )

            browser.close()

        return str(output_path)