from typing import Dict, Any
from pydantic import BaseModel

class InitIdea(BaseModel):
    mission: str
    technical_constraints: Dict[str, str]
    suggestion_pillar_future_experimental: Dict[str, Any]
    required_output_format_for_planners: Dict[str, str]
