from abc import ABC, abstractmethod

from .models import CompanySources


class SourceDiscovery(ABC):

    @abstractmethod
    def discover(self, company_name: str) -> CompanySources:
        pass