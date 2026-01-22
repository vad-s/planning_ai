from ..enums.work_status_enum import WorkStatus
from ..generic.base_schema import BaseSchema

class BaseComponent(BaseSchema):
    status: WorkStatus = WorkStatus.PENDING
