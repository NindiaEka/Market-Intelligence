from pydantic import BaseModel


class BusinessCapability(BaseModel):

    name: str
    reason: str
    
class CapabilityDetectionResult(BaseModel):

    capabilities: list[BusinessCapability]