"""
Step: The most granular level (Level 4) in the hierarchy.

A Step represents a single, actionable work item that cannot be further decomposed.
Steps are the leaf nodes of the project tree and contain the actual execution details.
"""

from typing import Optional
from pydantic import Field
from ..generic.base_schema import BaseSchema


class Step(BaseSchema):
    """
    Level 4 (Leaf): A single actionable step within a Task.

    Steps are atomic work units that:
    - Cannot have children (leaf nodes)
    - Contain concrete execution instructions
    - Have clear completion criteria
    - Are assigned to specific executors

    Examples:
    - "Write unit tests for authentication module"
    - "Deploy container to production environment"
    - "Review pull request #123"
    """

    step: str = Field(
        default="", description="Detailed instructions for executing this step"
    )

    estimated_hours: Optional[float] = Field(
        default=None, description="Estimated time to complete this step (in hours)"
    )

    assigned_to: Optional[str] = Field(
        default=None, description="Person or role responsible for this step"
    )

    prerequisites: list[str] = Field(
        default_factory=list,
        description="Step IDs that must be completed before this step",
    )

    validation_criteria: str = Field(
        default="", description="How to verify this step is complete"
    )

    def __repr__(self) -> str:
        return f"Step(title='{self.title}', status={self.status})"
