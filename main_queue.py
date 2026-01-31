from dataclasses import dataclass
from typing import List, Deque, Tuple
from collections import deque
import json


# ----------------------------
# Domain model (3 children each)
# ----------------------------

@dataclass
class Task:
    name: str
    steps: List[str]

@dataclass
class Concept:
    name: str
    tasks: List[Task]

@dataclass
class Module:
    name: str
    concepts: List[Concept]

@dataclass
class Component:
    name: str
    modules: List[Module]


def build_example_component() -> Component:
    """Build a tree with EXACTLY 3 children at every level."""
    def make_steps(task_num: int) -> List[str]:
        return [f"Step {task_num}.{i}" for i in range(1, 4)]

    def make_tasks(concept_num: int) -> List[Task]:
        return [Task(name=f"Task {concept_num}.{i}", steps=make_steps(i)) for i in range(1, 4)]

    def make_concepts(module_num: int) -> List[Concept]:
        return [Concept(name=f"Concept {module_num}.{i}", tasks=make_tasks(i)) for i in range(1, 4)]

    modules = [Module(name=f"Module {i}", concepts=make_concepts(i)) for i in range(1, 4)]
    return Component(name="Component", modules=modules)


# ----------------------------
# DFS → enqueue (pre-order)
# ----------------------------

def dfs_enqueue_paths(root: Component) -> Deque[str]:
    """
    Depth-first (pre-order) traversal.
    Enqueue readable full paths for every node into a deque.
    """
    q: Deque[str] = deque()

    def visit_component(c: Component, path: List[str]):
        cur = "/".join(path + [c.name])
        q.append(cur)  # Component
        for m in c.modules:
            visit_module(m, path + [c.name])

    def visit_module(m: Module, path: List[str]):
        cur = "/".join(path + [m.name])
        q.append(cur)  # Module
        for con in m.concepts:
            visit_concept(con, path + [m.name])

    def visit_concept(con: Concept, path: List[str]):
        cur = "/".join(path + [con.name])
        q.append(cur)  # Concept
        for t in con.tasks:
            visit_task(t, path + [con.name])

    def visit_task(t: Task, path: List[str]):
        cur = "/".join(path + [t.name])
        q.append(cur)  # Task
        for step in t.steps:
            q.append("/".join(path + [t.name, step]))  # Step (leaf as string)

    visit_component(root, [])
    return q


def dfs_enqueue_struct(root: Component) -> Deque[Tuple[str, str, str]]:
    """
    Depth-first (pre-order) traversal.
    Enqueue structured tuples: (node_type, name, full_path).
    """
    q: Deque[Tuple[str, str, str]] = deque()

    def visit_component(c: Component, path: List[str]):
        full = "/".join(path + [c.name])
        q.append(("Component", c.name, full))
        for m in c.modules:
            visit_module(m, path + [c.name])

    def visit_module(m: Module, path: List[str]):
        full = "/".join(path + [m.name])
        q.append(("Module", m.name, full))
        for con in m.concepts:
            visit_concept(con, path + [m.name])

    def visit_concept(con: Concept, path: List[str]):
        full = "/".join(path + [con.name])
        q.append(("Concept", con.name, full))
        for t in con.tasks:
            visit_task(t, path + [con.name])

    def visit_task(t: Task, path: List[str]):
        full = "/".join(path + [t.name])
        q.append(("Task", t.name, full))
        for step in t.steps:
            step_path = "/".join(path + [t.name, step])
            q.append(("Step", step, step_path))

    visit_component(root, [])
    return q


# ----------------------------
# Demo
# ----------------------------

if __name__ == "__main__":
    comp = build_example_component()

    # Option A: Queue of readable path strings (pre-order)
    q_paths = dfs_enqueue_paths(comp)
    print("# DFS queue (paths):")
    for item in q_paths:
        print(item)

    # Option B: Queue of structured tuples (pre-order)
    q_struct = dfs_enqueue_struct(comp)
    print("\n# DFS queue (structured tuples):")
    for typ, name, path in q_struct:
        print(f"{typ:9} | {name:15} | {path}")