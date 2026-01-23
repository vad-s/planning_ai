from ..schemas.concept import Concept
from ..generic.base_schema import BaseSchema

class ProjectState(BaseSchema):
    title: str = "Project State"
    concept: Concept=None
    all_done: bool = False
    