from src.company_resolution.models import CompanyCandidate
from typing import List


def select_candidate(candidates: List[CompanyCandidate]) -> CompanyCandidate:

    for idx, candidate in enumerate(candidates, start=1):
        print(f"{idx}. {candidate.name}")

    choice = int(input("\nSelect company: "))

    return candidates[choice - 1]