from pydantic import BaseModel, Field, RootModel
from typing import List, Optional, Dict


class ComponentDetail(BaseModel):
    """
    Individual component from designer output.

    Standard format:
    - name: Component name (required)
    - description: Component function description (required)
    - relevant_details: List of additional details (optional)
    """

    name: str = Field(..., description="Name of the component")
    description: str = Field(..., description="Description of the component's function")
    relevant_details: Optional[List[str]] = Field(
        None, description="List of additional relevant details about the component"
    )

    class Config:
        populate_by_name = True


class DesignerCompletionYaml(BaseModel):
    """
    Pydantic model for designer crew YAML response structure.

    Standard YAML format (all designers should follow):
    ```yaml
    agent_name: creative_product_designer
    components:
      - name: Component Name
        description: Component description
        relevant_details:
          - Detail 1
          - Detail 2
    ```

    This standardized format ensures consistency across:
    - Creative designer (exploratory, novel designs)
    - Balanced designer (practical, feasible designs)
    - Conservative designer (safe, proven designs)
    """

    agent_name: str = Field(
        ...,
        description="Name of the designer agent that produced this output (creative/balanced/conservative)",
    )
    components: List[ComponentDetail] = Field(
        ..., description="List of system components identified by the designer"
    )

    class Config:
        populate_by_name = True


class DesignerAgentData(BaseModel):
    """Data for a specific designer agent"""

    is_approved: bool = Field(
        default=False,
        description="Whether the design is approved by conservative standards",
    )
    components: List[ComponentDetail] = Field(
        ..., description="List of system components identified by the designer"
    )

    class Config:
        populate_by_name = True


class DesignerCompletionJson(BaseModel):
    """
    Pydantic model for designer crew JSON response structure.

    Standard JSON format (all designers should follow):
    ```json
    {
        "agent_name": "conservative_product_designer",
        "is_approved": true,
        "components": [
          {
            "name": "Component Name",
            "description": "Component description",
            "relevant_details": [
              "Detail 1",
              "Detail 2"
            ]
          }
        ]
    }
    ```

    The root key is the agent name (e.g., "conservative_product_designer")
    containing is_approved and components.

    This standardized format ensures consistency across:
    - Creative designer (exploratory, novel designs)
    - Balanced designer (practical, feasible designs)
    - Conservative designer (safe, proven designs)
    """

    agent_name: str = Field(
        ...,
        description="Name of the designer agent that produced this output (creative/balanced/conservative)",
    )
    is_approved: bool = Field(
        default=False,
        description="Whether the design is approved by conservative standards",
    )
    components: List[ComponentDetail] = Field(
        ..., description="List of system components identified by the designer"
    )

    class Config:
        populate_by_name = True


# Alias for backward compatibility
DesignerCompletion = DesignerCompletionYaml
