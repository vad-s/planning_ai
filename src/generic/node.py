from __future__ import annotations
from typing import List, Optional
from pydantic import Field
from .base_schema import BaseSchema, utcnow
from ..enums.work_status_enum import WorkStatus


class Node(BaseSchema):
    """
    A minimal hierarchical node:
      - parent is optional (None for root)
      - children is a simple list
      - level (int) and path (e.g., '0.1.2') are stored as properties
      - add_child enforces depth_limit and applies per-level defaults when available
    """

    parent: Optional["Node"] = Field(default=None, description="None for root")
    children: List["Node"] = Field(default_factory=list)
    level: int = 0
    path: str = "0"
    sep: str = "->"

    def add_child(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "Node":
        """
        Create a child node under self:
          - Checks depth_limit (if set)
          - Computes child level/path
          - Applies title/status from per-level maps if provided and not overridden
        """
        next_level = self.level + 1

        # Enforce depth limit if present
        if self.depth_limit is not None and next_level > self.depth_limit:
            raise ValueError(
                f"Cannot add child at level {next_level}: exceeds depth_limit={self.depth_limit}"
            )

        idx = len(self.children)
        child_path = f"{self.path}{self.sep}{idx}"

        # If caller didn't provide a title, try per-level default
        resolved_title = (
            title if title is not None else self.get_title_for_level(next_level)
        )
        # Prepare status (inherit current unless overridden by level map)
        resolved_status = self.get_status_for_level(next_level) or self.status

        child = Node(
            # BaseSchema fields
            title=resolved_title
            or "",  # title is required by BaseSchema; fallback to empty string
            description=description,
            status=resolved_status,
            finished_at=None,  # new child starts unfinished
            # Tree structure
            parent=self,
            children=[],
            level=next_level,
            path=child_path,
            sep=self.sep,
            # Inherit these global “settings” from parent so the child can create its own children consistently
            depth_limit=self.depth_limit,
            level_titles=self.level_titles,
            level_statuses=self.level_statuses,
        )
        self.children.append(child)
        return child

    def mark_done(self) -> None:
        """Convenience helper to mark node as DONE and set finished_at."""
        self.finished_at = utcnow()
        self.status = WorkStatus.DONE


# Important for self-referencing models in Pydantic v2
Node.model_rebuild()
