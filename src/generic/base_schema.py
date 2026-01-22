import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseSchema(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Stable unique identifier"
    )
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    finished_at: Optional[datetime] = None