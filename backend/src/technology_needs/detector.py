from abc import ABC
from abc import abstractmethod

from src.fact_extraction.models import (CompanyFacts)
from .models import (TechnologyNeedsResult)


class TechnologyDetector(ABC):

    @abstractmethod
    def detect(self, facts: CompanyFacts) -> TechnologyNeedsResult:
        pass