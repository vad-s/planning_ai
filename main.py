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
