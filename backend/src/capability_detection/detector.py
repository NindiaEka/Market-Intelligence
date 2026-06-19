from abc import ABC
from abc import abstractmethod

from src.fact_extraction.models import (CompanyFacts)
from .models import (CapabilityResult)


class CapabilityDetector(ABC):

    @abstractmethod
    def detect(self, facts: CompanyFacts) -> CapabilityResult:
        pass