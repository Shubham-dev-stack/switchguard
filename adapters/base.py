from abc import ABC, abstractmethod
from typing import Dict, Any
from core.models import Incident

class BaseChatAdapter(ABC):
    """
    Abstract interface for chat platforms (Discord, Slack, Teams).
    """

    @abstractmethod
    def format_incident_card(self, incident: Incident) -> Dict[str, Any]:
        """Formats the initial incident notification card."""
        pass

    @abstractmethod
    def format_approval_request(self, incident: Incident, patch_summary: str) -> Dict[str, Any]:
        """Formats human signoff request with action buttons."""
        pass
