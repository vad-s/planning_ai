from pydantic import BaseModel, Field


class TaskPrompt(BaseModel):
    project_brief: str = Field(alias="project_brief")
    description: str = Field(alias="planner_instructions")
    expected_output: str = Field(alias="planner_expected_outputs")

    class Config:
        populate_by_name = True
