from pydantic import BaseModel


class TechnologyNeed(BaseModel):
    category: str
    reason: str


class TechnologyNeedsResult(BaseModel):
    technology_needs: list[TechnologyNeed]