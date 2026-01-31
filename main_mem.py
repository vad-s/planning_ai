# main.py
from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple
import uuid


# -------- Work Item --------
@dataclass
class WorkItem:
    type: str  # "Idea" | "Module" | "Component" | ...
    name: str
    status: str = "pending"  # "pending" | "in_progress" | "done"
    parent_id: Optional[str] = None
    path: Tuple[int, ...] = field(default_factory=tuple)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_in_progress(self) -> None:
        self.status = "in_progress"

    def mark_done(self) -> None:
        self.status = "done"


# -------- Engine (FIFO with child-next) --------
class WorkEngine:
    """
    FIFO engine with 'child-next' semantics:
      - add item(s) -> take first -> do work
      - while current is in progress, worker may yield children
      - those children are inserted as NEXT (queue head), preserving their order
      - complete current -> immediately process its children
      - finish when the queue is empty and no current
    """

    def __init__(self) -> None:
        self._q: deque[WorkItem] = deque()
        self._current: Optional[WorkItem] = None
        self._completed: List[WorkItem] = []
        self._log: List[str] = []

    # --- enqueue ---
    def add(self, items: Iterable[WorkItem] | WorkItem) -> None:
        if isinstance(items, WorkItem):
            self._q.append(items)  # tail
        else:
            for it in items:
                self._q.append(it)

    def add_next(self, items: Iterable[WorkItem] | WorkItem) -> None:
        # Insert at head so children run immediately after current
        if isinstance(items, WorkItem):
            self._q.appendleft(items)
        else:
            buf = list(items)
            for it in reversed(buf):  # preserve given order at head
                self._q.appendleft(it)

    # --- core steps ---
    def take_first(self) -> Optional[WorkItem]:
        if self._current is not None:
            return self._current
        if not self._q:
            return None
        self._current = self._q.popleft()
        self._current.mark_in_progress()
        self._log.append(f"START: {self._current.type}:{self._current.name}")
        return self._current

    def complete_current(self) -> Optional[WorkItem]:
        if self._current is None:
            return None
        item = self._current
        item.mark_done()
        self._completed.append(item)
        self._log.append(f"DONE:  {item.type}:{item.name}")
        self._current = None
        return item

    def run(self, worker) -> List[WorkItem]:
        """
        worker(item) -> iterable of children (yield or return list)
        """
        while True:
            cur = self.take_first()
            if cur is None:
                break  # no items left

            # Let worker produce children while current is in progress
            children = list(worker(cur))
            if children:
                # Attach lineage
                for ch in children:
                    if ch.parent_id is None:
                        ch.parent_id = cur.id
                self._log.append(
                    "YIELD: "
                    + ", ".join(f"{c.type}:{c.name}" for c in children)
                    + f" (parent={cur.type}:{cur.name})"
                )
                self.add_next(children)

            # Finish current, move on to next
            self.complete_current()

        return self._completed

    # --- helpers for demo ---
    def print_log(self) -> None:
        print("\n--- Execution Log ---")
        for line in self._log:
            print(line)

    def print_completed(self, limit: int = 20) -> None:
        print("\n--- Completed (first {0}) ---".format(limit))
        for it in self._completed[:limit]:
            print(f"{it.type}:{it.name} (status={it.status})")


# -------- Example worker --------
def worker(item: WorkItem) -> Iterable[WorkItem]:
    """
    Demo logic:
      - If item is 'Idea', produce 2 'Module's
      - If 'Module', produce 2 'Component's
      - If 'Component', produce 2 'Task's
      - If 'Task', produce 2 'Step's
      - 'Step' produces nothing (leaf)
    This shows how children are placed 'next' and executed immediately after parent.
    """
    next_map = {
        "Idea": "Module",
        "Module": "Component",
        "Component": "Task",
        "Task": "Step",
    }
    child_type = next_map.get(item.type)
    if not child_type:
        return []  # no children

    children = [
        WorkItem(type=child_type, name=f"{child_type} of {item.name} A"),
        WorkItem(type=child_type, name=f"{child_type} of {item.name} B"),
    ]
    return children


# -------- Main demo --------
if __name__ == "__main__":
    engine = WorkEngine()

    # Seed multiple roots to see FIFO behavior across siblings
    engine.add(WorkItem(type="Idea", name="Build App"))
    engine.add(WorkItem(type="Idea", name="Write Docs"))

    completed = engine.run(worker)

    engine.print_log()
    engine.print_completed()
