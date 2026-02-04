"""
Component: Level 2 in the hierarchy.

A Component is a logical grouping of Tasks that represents a subsystem
or feature within a Module. Components organize related work items.
"""

from typing import List, Optional
from pydantic import Field
from ..generic.base_schema import BaseSchema


class Component(BaseSchema):
    """
    Level 2: A component containing multiple Tasks.

    Components represent:
    - Subsystems within a Module
    - Feature sets
    - Architectural layers
    - Functional groupings

    Examples:
    - "User Authentication System"
    - "Data Access Layer"
    - "API Gateway"
    - "Frontend Dashboard"
    """

    tasks: List["Task"] = Field(
        default_factory=list, description="Tasks that compose this component"
    )

    technical_approach: str = Field(
        default="", description="High-level technical strategy for this component"
    )

    technologies: List[str] = Field(
        default_factory=list,
        description="Technologies/frameworks used in this component",
    )

    interfaces: List[str] = Field(
        default_factory=list,
        description="APIs, contracts, or interfaces this component exposes",
    )

    dependencies: List[str] = Field(
        default_factory=list, description="Other component IDs this depends on"
    )

    risk_level: Optional[str] = Field(
        default=None, description="Risk assessment: LOW, MEDIUM, HIGH"
    )

    def __repr__(self) -> str:
        return f"Component(title='{self.title}', tasks={len(self.tasks)}, status={self.status})"


# Import after class definition to avoid circular imports
from .task import Task

Component.model_rebuild()
