from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Any, Dict
import json

try:
    import yaml  # Optional: PyYAML (pip install pyyaml)
    HAS_YAML = True
except Exception:
    HAS_YAML = False


# ----------------------------
# Domain Model
# ----------------------------

@dataclass
class Task:
    name: str
    steps: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "steps": self.steps}


@dataclass
class Concept:
    name: str
    tasks: List[Task]

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "tasks": [t.to_dict() for t in self.tasks]}


@dataclass
class Module:
    name: str
    concepts: List[Concept]

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "concepts": [c.to_dict() for c in self.concepts]}


@dataclass
class Component:
    name: str
    modules: List[Module]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "component": {
                "name": self.name,
                "modules": [m.to_dict() for m in self.modules]
            }
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# -------------------------------------------------------------------

def build_example_component() -> Component:
    """Build a tree with EXACTLY 3 children at every level."""

    def make_steps(task_num: int) -> List[str]:
        return [f"Step {task_num}.{i}" for i in range(1, 4)]

    def make_tasks(concept_num: int) -> List[Task]:
        return [
            Task(name=f"Task {concept_num}.{i}", steps=make_steps(i))
            for i in range(1, 4)
        ]

    def make_concepts(module_num: int) -> List[Concept]:
        return [
            Concept(name=f"Concept {module_num}.{i}", tasks=make_tasks(i))
            for i in range(1, 4)
        ]

    modules = [
        Module(name=f"Module {i}", concepts=make_concepts(i))
        for i in range(1, 4)
    ]

    return Component(name="Component", modules=modules)



# ----------------------------
# CLI Demo
# ----------------------------

if __name__ == "__main__":
    comp = build_example_component()

    print("# JSON")
    print(comp.to_json())
