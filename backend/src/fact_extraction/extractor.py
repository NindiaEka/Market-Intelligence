from abc import ABC, abstractmethod

from .models import CompanyFacts


class FactExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        markdown: str
    ) -> CompanyFacts:
        pass