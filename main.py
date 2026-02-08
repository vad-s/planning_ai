import importlib
import src.flows.bfs_node_flow as module

importlib.reload(module)

import os
from pathlib import Path

# Go up until we find pyproject.toml (project root)
current = Path(__file__).resolve()
while not (current / "pyproject.toml").exists():
    current = current.parent
os.chdir(current)

print("Working directory:", os.getcwd())

from src.flows.bfs_node_flow import BFSNodeFlow
from src.state.node_state import NodeState


def run_flow():
    print("Starting BFSNodeFlow...")
    state = NodeState()
    flow = BFSNodeFlow(state=state)
    flow.kickoff()
    print("Flow execution complete.")


if __name__ == "__main__":
    run_flow()
