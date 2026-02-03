from typing import List, Optional
from pydantic import BaseModel, Field

class ArchitectBriefing(BaseModel):
    """Schema for the architect briefing task output."""
    project_description_for_planners: str = Field(..., description="The translated vision for the planners.")
    planner_task_instructions: str = Field(..., description="The work order and specific instructions for the next agents.")

class DecomposedIdea(BaseModel):
    """Schema for the decompose idea task output."""
    logical_units: List[str] = Field(..., description="A list of logical units or components decomposed from the concept.")
