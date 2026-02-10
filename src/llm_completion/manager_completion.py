from pydantic import BaseModel, Field


class ManagerCompletion(BaseModel):
    """
    Pydantic model for manager crew response structure.
    Matches the YAML structure in manager_crew_response from llm_utils.py
    """

    project_brief: str = Field(..., description="The project brief and vision")
    designer_instructions: str = Field(
        ..., description="Instructions for the designer role"
    )
    designer_expected_outputs: str = Field(
        ..., description="Expected outputs description for the designer"
    )

    class Config:
        populate_by_name = True
