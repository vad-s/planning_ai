import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Union
from pydantic import BaseModel, Field, model_validator, PrivateAttr
from ..enums.work_status_enum import WorkStatus

def utcnow():
    return datetime.now(timezone.utc)

LevelTitleInput = Union[List[str], Dict[int, str]]
LevelStatusInput = Union[List[WorkStatus], Dict[int, WorkStatus]]

class BaseSchema(BaseModel):
    #model_config = {"frozen": True}
    
    # identity / meta
    id: uuid.UUID = Field(default_factory=uuid.uuid4, description="Stable unique identifier")
    title: str
    description: Optional[str] = None

    # time fields
    created_at: datetime = Field(default_factory=utcnow)
    finished_at: Optional[datetime] = None

    # status
    status: WorkStatus = WorkStatus.PENDING

    # tree constraints / defaults
    depth_limit: Optional[int] = Field(
        default=None,
        ge=0,
        description="If set, maximum allowed depth (root is level 0).",
    )
    
    # Per-level metadata (input may be list or dict; will be normalized to dicts below)
    level_titles: Optional[LevelTitleInput] = Field(
        default=None,
        description="Optional per-level titles. Accepts list[str] (index = level) or dict[int,str]."
    )
    level_statuses: Optional[LevelStatusInput] = Field(
        default=None,
        description="Optional per-level statuses. Accepts list[WorkStatus] (index = level) or dict[int, WorkStatus]."
    )

    # Internal normalized views (computed in validator)
    level_titles_map: Dict[int, str] = Field(default_factory=dict, exclude=True)
    level_statuses_map: Dict[int, WorkStatus] = Field(default_factory=dict, exclude=True)

    
    @model_validator(mode="after")
    def _normalize_level_maps(self) -> "BaseSchema":
        # Normalize titles
        if isinstance(self.level_titles, list):
            self.level_titles_map = {i: v for i, v in enumerate(self.level_titles)}
        elif isinstance(self.level_titles, dict):
            self.level_titles_map = dict(self.level_titles)
        else:
            self.level_titles_map = {}

        # Normalize statuses
        if isinstance(self.level_statuses, list):
            self.level_statuses_map = {i: v for i, v in enumerate(self.level_statuses)}
        elif isinstance(self.level_statuses, dict):
            self.level_statuses_map = dict(self.level_statuses)
        else:
            self.level_statuses_map = {}

        # Sanity checks
        for k in list(self.level_titles_map.keys()):
            if k < 0:
                raise ValueError(f"level_titles: level must be >= 0, got {k}")
        for k in list(self.level_statuses_map.keys()):
            if k < 0:
                raise ValueError(f"level_statuses: level must be >= 0, got {k}")

        if self.depth_limit is not None:
            if self.depth_limit < 0:
                raise ValueError("depth_limit must be >= 0")
            # Optional: warn/error if maps define levels beyond depth_limit
            over_titles = [lvl for lvl in self.level_titles_map if lvl > self.depth_limit]
            over_status = [lvl for lvl in self.level_statuses_map if lvl > self.depth_limit]
            if over_titles:
                raise ValueError(f"level_titles contains levels beyond depth_limit: {over_titles}")
            if over_status:
                raise ValueError(f"level_statuses contains levels beyond depth_limit: {over_status}")

        return self

    # Helper getters for children to use
    def get_title_for_level(self, level: int) -> Optional[str]:
        return self.level_titles_map.get(level)

    def get_status_for_level(self, level: int) -> Optional[WorkStatus]:
        return self.level_statuses_map.get(level)


