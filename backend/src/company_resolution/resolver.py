from abc import ABC, abstractmethod
from typing import List

from .models import CompanyCandidate


class CompanyResolver(ABC):

    @abstractmethod
    def resolve(self, company_name: str) -> List[CompanyCandidate]:
        pass