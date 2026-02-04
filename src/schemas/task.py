"""
Task: Level 3 in the hierarchy.

A Task is a collection of Steps that together accomplish a specific objective.
Tasks are organized within Components and break down into executable Steps.
"""

from typing import List, Optional
from pydantic import Field
from ..generic.base_schema import BaseSchema


class Task(BaseSchema):
    """
    Level 3: A task composed of multiple Steps.

    Tasks represent work units that:
    - Contain 0-N Steps
    - Have clear deliverables
    - Can be assigned to team members
    - Have dependencies on other tasks

    Examples:
    - "Implement user authentication"
    - "Set up CI/CD pipeline"
    - "Create database migration"
    """

    steps: List["Step"] = Field(
        default_factory=list, description="Steps that compose this task"
    )

    priority: int = Field(
        default=5, ge=1, le=10, description="Priority level (1=lowest, 10=highest)"
    )

    estimated_duration: Optional[str] = Field(
        default=None,
        description="Estimated time to complete (e.g., '2 days', '1 week')",
    )

    dependencies: List[str] = Field(
        default_factory=list,
        description="Task IDs that must be completed before this task",
    )

    deliverables: List[str] = Field(
        default_factory=list, description="Expected outputs from this task"
    )

    acceptance_criteria: List[str] = Field(
        default_factory=list,
        description="Conditions that must be met to consider this task complete",
    )

    def __repr__(self) -> str:
        return (
            f"Task(title='{self.title}', steps={len(self.steps)}, status={self.status})"
        )


# Import after class definition to avoid circular imports
from .step import Step

Task.model_rebuild()
