from pydantic import BaseModel
from typing import List, Optional


class CompanyCandidate(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    description: Optional[str] = None

class CandidateExtractionResult(BaseModel):
    candidates: List[str]