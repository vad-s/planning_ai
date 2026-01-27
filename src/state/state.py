from typing import Dict, Optional, Union

from pydantic import Field
from ..schemas.concept import Concept
from ..generic.base_schema import BaseSchema


class ProjectState(BaseSchema):
    title: str = "Project State"
    concept: Optional[Concept] = None
    all_done: bool = False
    drafts: Dict[str, str] = Field(
        default_factory=dict
    )  # {"creative": ..., "balanced": ..., "conservative": ...}
    scores: Dict[str, int] = Field(
        default_factory=dict
    )  # {"creative": 75, "balanced": 60, "conservative": 80}
    retry_count: int = 0
    manager_output: str = ""
    planner_output: list[str] = Field(default_factory=list)
    reviewer_output: str = ""
    writer_output: str = ""