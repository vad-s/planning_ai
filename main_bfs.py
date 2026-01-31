from collections import deque
from typing import List, Tuple, Dict, Deque, Optional

# -----------------------------
# Configuration
# -----------------------------
DEPTH_LIMIT = 5            # Component=1, Module=2, Concept=3, Task=4, Step=5
SHOW_COLOR = True          # Turn off if your terminal doesn't support ANSI
ROOT_NAME  = "Component"   # BFS root


# -----------------------------
# ANSI Colors (by node type)
# -----------------------------
class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    WHITE = "\033[37m"

def node_type(name: str) -> str:
    if name == "Component":       return "Component"
    if name.startswith("Module "):  return "Module"
    if name.startswith("Concept "): return "Concept"
    if name.startswith("Task "):    return "Task"
    if name.startswith("Step "):    return "Step"
    return "Other"

TYPE_COLOR = {
    "Component": Color.BOLD + Color.CYAN,
    "Module":    Color.BOLD + Color.BLUE,
    "Concept":   Color.BOLD + Color.GREEN,
    "Task":      Color.BOLD + Color.YELLOW,
    "Step":      Color.MAGENTA,
    "Other":     Color.WHITE,
}

def colorize(name: str) -> str:
    if not SHOW_COLOR:
        return name
    return f"{TYPE_COLOR.get(node_type(name), Color.WHITE)}{name}{Color.RESET}"

# -----------------------------
# Tree fan-out: exactly 2 children (if under depth limit)
# -----------------------------
def two_children(name: str, depth: int, depth_limit: int) -> List[Tuple[str, int]]:
    """
    2 children per node naming scheme:
      Component -> Module A, Module B
      Module A  -> Concept A1, Concept A2
      Module B  -> Concept B1, Concept B2
      Concept A1 -> Task A1-1, Task A1-2
      Task A1-1 -> Step A1-1.1, Step A1-1.2
      Steps -> no children
    """
    if depth >= depth_limit:
        return []

    if name == "Component":  # depth 1
        return [("Module A", depth + 1), ("Module B", depth + 1)]

    if name.startswith("Module "):  # depth 2
        suff = name.split(" ", 1)[1]  # "A" or "B"
        return [(f"Concept {suff}1", depth + 1), (f"Concept {suff}2", depth + 1)]

    if name.startswith("Concept "):  # depth 3
        suff = name.split(" ", 1)[1]  # "A1","A2","B1","B2"
        return [(f"Task {suff}-1", depth + 1), (f"Task {suff}-2", depth + 1)]

    if name.startswith("Task "):  # depth 4
        suff = name.split(" ", 1)[1]  # "A1-1", etc.
        return [(f"Step {suff}.1", depth + 1), (f"Step {suff}.2", depth + 1)]

    # Steps (depth 5): leaves
    return []

# -----------------------------
# Visualization helpers
# -----------------------------
def build_tree_adjacency(root: str, depth_limit: int) -> Dict[str, List[str]]:
    """
    Build an adjacency list of the entire tree (bounded by depth_limit),
    using the same child-generation logic. BFS over (node, depth).
    """
    adj: Dict[str, List[str]] = {}
    q: Deque[Tuple[str, int]] = deque([(root, 1)])
    seen: set[str] = set()

    while q:
        node, depth = q.popleft()
        if node in seen:
            continue
        seen.add(node)
        children = two_children(node, depth, depth_limit)
        adj[node] = [c for (c, _) in children]
        for child, d in children:
            q.append((child, d))
    return adj

def to_mermaid(adj: Dict[str, List[str]], root: str, direction: str = "TD") -> str:
    """
    Create a Mermaid graph definition (flowchart).
    direction: "TD" (top-down), "LR" (left-right), etc.
    """
    lines = [f"graph {direction}"]
    emitted = set()
    # Emit edges node -> child
    def node_id(name: str) -> str:
        # simple id compatible with mermaid
        return name.replace(" ", "_").replace(".", "_").replace("-", "_")
    for parent, children in adj.items():
        pid = node_id(parent)
        if pid not in emitted:
            lines.append(f'    {pid}["{parent}"]')
            emitted.add(pid)
        for child in children:
            cid = node_id(child)
            if cid not in emitted:
                lines.append(f'    {cid}["{child}"]')
                emitted.add(cid)
            lines.append(f"    {pid} --> {cid}")
    return "\n".join(lines)

def to_ascii_tree(adj: Dict[str, List[str]], root: str) -> str:
    """
    Render a simple ASCII tree (depth-first for formatting).
    """
    lines: List[str] = []
    def dfs(name: str, prefix: str = "", is_last: bool = True):
        connector = "└─ " if is_last else "├─ "
        lines.append(prefix + connector + name)
        children = adj.get(name, [])
        for i, ch in enumerate(children):
            last = i == len(children) - 1
            new_prefix = prefix + ("   " if is_last else "│  ")
            dfs(ch, new_prefix, last)
    lines.append(root)  # root top line (no connector)
    kids = adj.get(root, [])
    for i, k in enumerate(kids):
        dfs(k, "", i == len(kids) - 1)
    return "\n".join(lines)

# -----------------------------
# BFS simulation (no user limit)
# -----------------------------
def fmt_queue(q: deque[Tuple[str, int]]) -> str:
    return "[ " + ", ".join(colorize(n) for (n, _) in q) + " ]"

def bfs_simulate_until_empty(depth_limit: int = DEPTH_LIMIT, visualize: bool = True) -> None:
    """
    Classic BFS:
      - Initialize queue with (Component, depth=1)
      - While queue not empty:
          1) Dequeue front node
          2) Enqueue children to the BACK
      - Print every move (Before/After/Dequeue/Enqueue)
    If visualize=True, prints Mermaid and ASCII tree before the BFS log.
    """
    root = ROOT_NAME
    if visualize:
        print("=== TREE VISUALIZATION ===")
        adj = build_tree_adjacency(root, depth_limit)
        print("\n# Mermaid (copy-paste into Markdown):")
        print("```mermaid")
        print(to_mermaid(adj, root, direction="TD"))
        print("```")
        print("\n# ASCII Tree:")
        print(to_ascii_tree(adj, root))
        print("\n=== END VISUALIZATION ===\n")

    # Legend
    print("Legend:")
    for t in ("Component", "Module", "Concept", "Task", "Step"):
        print(f"  {TYPE_COLOR[t] if SHOW_COLOR else ''}{t}{Color.RESET if SHOW_COLOR else ''}")
    print()

    q: deque[Tuple[str, int]] = deque([(root, 1)])
    print(f"INIT: queue = {fmt_queue(q)}\n")

    step = 0
    visited_queue: List[str] = []

    while q:
        step += 1
        print(f"Step {step} — BFS process front")
        print("Before:", fmt_queue(q))

        node, depth = q.popleft()
        visited_queue.append(node)
        print(f"DEQUEUE: {colorize(node)}  (depth {depth}, type {node_type(node)})")

        children = two_children(node, depth, depth_limit)
        if children:
            # Enqueue children to the BACK (BFS)
            for child_name, child_depth in children:
                q.append((child_name, child_depth))
            kids = "[ " + ", ".join(colorize(n) for (n, _) in children) + " ]"
            print("ENQUEUE_BACK (children, in order):", kids)
        else:
            print("LEAF (no children enqueued).")

        print("After: ", fmt_queue(q))
        print()

    print("BFS visited order (all nodes within depth limit):")
    print("[ " + ", ".join(colorize(n) for n in visited_queue) + " ]")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    # Runs BFS until the queue is empty (no user step limit).
    # Set visualize=False if you only want the BFS log.
    bfs_simulate_until_empty(depth_limit=DEPTH_LIMIT, visualize=True)