"""
Module: Level 1 in the hierarchy.

A Module is a major subdivision of a Concept, representing a significant
area of functionality or a major architectural layer. Modules contain Components.
"""

from typing import List, Optional
from pydantic import Field
from ..generic.base_schema import BaseSchema


class Module(BaseSchema):
    """
    Level 1: A module containing multiple Components.

    Modules represent:
    - Major system areas (backend, frontend, infrastructure)
    - Architectural layers (presentation, business logic, data)
    - Functional domains (authentication, payments, reporting)
    - Development phases (MVP, v2.0, future enhancements)

    Examples:
    - "Backend API Services"
    - "Mobile Application"
    - "Infrastructure & DevOps"
    - "Analytics & Reporting"
    """

    components: List["Component"] = Field(
        default_factory=list, description="Components that compose this module"
    )

    scope: str = Field(
        default="", description="Overall scope and boundaries of this module"
    )

    architecture_notes: str = Field(
        default="",
        description="Key architectural decisions and patterns for this module",
    )

    key_stakeholders: List[str] = Field(
        default_factory=list,
        description="Team members or roles responsible for this module",
    )

    milestones: List[str] = Field(
        default_factory=list, description="Major milestones or releases for this module"
    )

    success_metrics: List[str] = Field(
        default_factory=list, description="KPIs or metrics to measure module success"
    )

    def __repr__(self) -> str:
        return f"Module(title='{self.title}', components={len(self.components)}, status={self.status})"


# Import after class definition to avoid circular imports
from .component import Component

Module.model_rebuild()
