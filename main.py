from src.flows.bfs_flow import BFSFlow
from src.state.state import ProjectState

def run_flow():
    print("Starting BFSFlow...")
    state = ProjectState()
    flow = BFSFlow(state=state)
    flow.kickoff()
    print("Flow execution complete.")

if __name__ == "__main__":
    run_flow()
