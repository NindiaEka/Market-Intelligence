from src.pipeline.pipeline import (MarketIntelligencePipeline)

def main():

    company_name = input("Enter company name: ")

    pipeline = (MarketIntelligencePipeline())

    pipeline.run(company_name)

if __name__ == "__main__":
    main()