from pydantic import BaseModel
from typing import Optional, List


class Evidence(BaseModel):
    source_name: str
    source_type: str
    url: str


class Offering(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    evidence: List[Evidence]


class Partner(BaseModel):
    name: str
    evidence: List[Evidence]


class Activity(BaseModel):
    type: str
    title: str
    description: Optional[str] = None
    date: Optional[str] = None
    evidence: List[Evidence]


class CompanyProfile(BaseModel):
    company_name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    headquarters: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None


class CompanyIntelligence(BaseModel):
    company_profile: CompanyProfile
    offerings: List[Offering] = []
    partners: List[Partner] = []
    activities: List[Activity] = []