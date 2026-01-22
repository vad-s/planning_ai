import sys
import os
import uuid
from datetime import datetime

# Add the project root to the python path
sys.path.append(os.getcwd())

try:
    from src.schemas.step import Step
    from src.schemas.task import Task
    from src.schemas.component import Component
    from src.schemas.module import Module
    from src.schemas.concept import Concept
    from src.enums.work_status_enum import Status

    print("Imports successful")

    # Instantiate with minimal args (title is required)
    s = Step(title="Step 1", step="Do something")

    # Check inherited fields
    assert isinstance(s.id, uuid.UUID), f"ID is not UUID: {type(s.id)}"
    assert isinstance(s.created_at, datetime), "created_at is not datetime"
    assert s.status == Status.PENDING, f"Default status is {s.status}"

    print(f"Step created: {s.id} - {s.title} ({s.status})")

    t = Task(title="Task 1", steps=[s])
    c = Component(title="Comp 1", tasks=[t])
    m = Module(title="Mod 1", components=[c])
    con = Concept(title="Concept 1", modules=[m])

    print("Hierarchy instantiation successful")
    # Using json() for Pydantic v1/v2 compatibility if needed, but model_dump_json is v2
    try:
        print(con.model_dump_json(indent=2))
    except AttributeError:
        print(con.json(indent=2))

except Exception as e:
    import traceback

    traceback.print_exc()
    print(f"Verification failed: {e}")
    sys.exit(1)
