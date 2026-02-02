from typing import Deque, Optional, Union, List, Any, Dict
from collections import deque
from pydantic import Field

from ..generic.base_schema import BaseSchema
from ..generic.node import Node
from ..schemas.concept import Concept

class NodeState(BaseSchema):
    title: str = "Node Project State"
    concept: Optional[Concept] = None
    all_done: bool = False
    
    # Queue-Based Workflow State using Node
    # Using Node directly. 
    work_queue: Deque[Node] = Field(default_factory=deque)
    visited_queue: Deque[Node] = Field(default_factory=deque)
    current_item: Optional[Node] = None
    
    # Legacy/Existing (Keeping for compatibility if needed, or minimal)
    drafts: Dict[str, str] = Field(default_factory=dict)
    scores: Dict[str, int] = Field(default_factory=dict)
    retry_count: int = 0
    manager_output: str = ""
    planner_output: List[str] = Field(default_factory=list)
    reviewer_output: str = ""
    writer_output: str = ""
