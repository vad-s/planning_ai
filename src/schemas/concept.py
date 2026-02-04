"""
Concept: The root level (Level 0) in the hierarchy.

A Concept represents the entire project or initiative. It is the top-level
container that holds all Modules and represents the complete vision.
"""

from typing import List, Optional
from pydantic import Field
from ..generic.base_schema import BaseSchema


class Concept(BaseSchema):
    """
    Level 0 (Root): The top-level project concept.

    A Concept represents:
    - The entire project/product
    - The complete vision and mission
    - All high-level goals and objectives
    - Root node of the project hierarchy

    Examples:
    - "Fitness Tracking Platform"
    - "E-Commerce Marketplace"
    - "Smart Home System"
    - "AI-Powered Planning Tool"
    """

    modules: List["Module"] = Field(
        default_factory=list, description="Top-level modules that compose this concept"
    )

    vision: str = Field(
        default="", description="The overarching vision and purpose of this project"
    )

    goals: List[str] = Field(
        default_factory=list, description="High-level goals and objectives"
    )

    constraints: List[str] = Field(
        default_factory=list, description="Technical, business, or resource constraints"
    )

    target_audience: str = Field(
        default="", description="Primary users or stakeholders"
    )

    success_criteria: List[str] = Field(
        default_factory=list,
        description="How success will be measured at the project level",
    )

    timeline: Optional[str] = Field(
        default=None, description="Overall project timeline or roadmap"
    )

    budget: Optional[str] = Field(
        default=None, description="Budget considerations or constraints"
    )

    def __repr__(self) -> str:
        return f"Concept(title='{self.title}', modules={len(self.modules)}, status={self.status})"


# Import after class definition to avoid circular imports
from .module import Module

Concept.model_rebuild()
