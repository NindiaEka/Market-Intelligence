from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pipeline.pipeline import MarketIntelligencePipeline

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CompanyRequest(BaseModel):
    company_name: str


class AnalyzeResponse(BaseModel):
    status: str
    report: str


@app.get("/")
def root():

    return {
        "message": "Market Intelligence API"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post(
    "/analyze",
    response_model=AnalyzeResponse
)
def analyze_company(
    request: CompanyRequest
):

    pipeline = MarketIntelligencePipeline()

    report = (
        pipeline.run(
            request.company_name
        )
    )

    return {
        "status": "success",
        "report": report
    }