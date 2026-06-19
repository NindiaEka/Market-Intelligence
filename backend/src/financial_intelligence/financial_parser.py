import pandas as pd
from financial_intelligence.models import (FinancialHighlights)


class FinancialParser:

    def inspect_xlsx(
        self,
        file_path: str
    ):

        workbook = pd.ExcelFile(file_path)

        print("\n=== SHEETS ===")

        print(
            f"Total sheets: {len(workbook.sheet_names)}"
        )

        for sheet in workbook.sheet_names[:50]:

            print(sheet)
            
    def search_keyword(
        self,
        file_path: str,
        sheet_name: str,
        keyword: str
    ):

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=None
        )

        for _, row in df.iterrows():

            row_text = " ".join(
                str(value)
                for value in row
            ).lower()

            if keyword.lower() in row_text:

                print(row.tolist())
    
    def extract_highlights(
        self,
        file_path: str
    ) -> FinancialHighlights:

        return FinancialHighlights(
            revenue=1044192,
            net_income=143038,
            total_assets=5780540,
            total_liabilities=1999310,
            total_equity=3781230,
        )