import sys
import os

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.flows.depth_first_traversal_flow import Depth_First_Traversal_Flow
from src.state.state import ProjectState

def verify_flow():
    print("Starting DFT Flow Verification...")
    state = ProjectState()
    flow = Depth_First_Traversal_Flow(state=state)
    
    # Run the flow
    # We expect it to traverse several levels.
    # To keep the test short, we could mock the decomposition to return fewer items,
    # but the current mock returns 3 items per level.
    
    flow.kickoff()
    
    print("\nVerification Complete.")
    print(f"All done: {flow.state.all_done}")
    # Since we don't have a tree-building logic yet, let's just check the stack is empty
    print(f"Final stack size: {len(flow.state.decomposition_stack)}")

if __name__ == "__main__":
    verify_flow()
