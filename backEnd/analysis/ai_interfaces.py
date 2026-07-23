from abc import ABC, abstractmethod
from typing import Dict, Any, List

class WebsiteAuditorInterface(ABC):
    @abstractmethod
    async def audit(self, url: str) -> Dict[str, Any]:
        pass

class LeadScorerInterface(ABC):
    @abstractmethod
    def calculate_score(self, business_data: Dict[str, Any], audit_data: Dict[str, Any]) -> int:
        pass

class OutreachGeneratorInterface(ABC):
    @abstractmethod
    def generate_email(self, business_name: str, deficiencies: List[str]) -> Dict[str, str]:
        """Must return dict containing 'subject' and 'body'."""
        pass

class ProposalGeneratorInterface(ABC):
    @abstractmethod
    def create_proposal(self, business_data: Dict[str, Any], audit_data: Dict[str, Any]) -> str:
        """Returns document file path or URL."""
        pass