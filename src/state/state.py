from typing import Dict, List, Optional, Union, Any, Deque
from collections import deque

from pydantic import Field
from ..schemas.concept import Concept
from ..generic.base_schema import BaseSchema


class ProjectState(BaseSchema):
    title: str = "Project State"
    concept: Optional[Concept] = None
    all_done: bool = False
    
    # Queue-Based Workflow State
    work_queue: Deque[Dict[str, Any]] = Field(default_factory=deque)
    visited_queue: Deque[Dict[str, Any]] = Field(default_factory=deque)
    current_item: Optional[Dict[str, Any]] = None
    
    # Legacy/Existing
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