
from pydantic import BaseModel, Field

class TaskPrompt(BaseModel):
    description: str = Field(alias="project_description_for_planners")
    expected_output: str = Field(alias="planner_task_instructions")

    class Config:
        allow_population_by_field_name = True
