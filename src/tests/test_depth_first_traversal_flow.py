import sys
import os
import asyncio

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.flows.depth_first_traversal_flow import Depth_First_Traversal_Flow
from src.schemas.concept import Concept
from src.state.state import ProjectState

def test_depth_first_traversal_flow():
    # Initialize State
    concept = Concept(title="Create a bank app", description="A simple banking application")
    state = ProjectState(title="Project State", concept=concept)
    
    print("Initializing Flow...")
    flow = Depth_First_Traversal_Flow(state=state)

    print("Kicking off Flow...")
    result = flow.kickoff()
    
    print(f"Flow Result: {result}")
    
    if result:
         print("Test Passed: Flow completed and returned a result.")
    else:
         print("Test Failed: Flow flow did not return a result.")

if __name__ == "__main__":
    test_depth_first_traversal_flow()
