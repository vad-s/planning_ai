import sys
import os

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
# current_dir is .../src/crews/manager_crew
# we need to go up 3 levels to get to repo root to see 'src' as a package? 
# Actually if we run from repo root, it's fine. Use robust path addition.
src_path = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.crews.manager_crew.crew import ManagerCrew

def test_manager_crew():
    print("Testing Manager Crew...")
    
    # Initialize crew with mock
    manager_crew = ManagerCrew(use_mock=True).crew()
    
    inputs = {
        'topic': 'Create a bank app'
    }
    
    print(f"Kicking off Manager Crew with inputs: {inputs}")
    result = manager_crew.kickoff(inputs=inputs)
    
    print(f"Result Type: {type(result)}")
    print(f"Result: {result}")
    
    # Basic validation of result
    # We expect the mock LLM to return something specific.
    # checking src/crews/manager_crew/crew.py, line 25: 
    # mock_llm = MockLLM(responses=["Final Answer: Test response 1", "Final Answer: Test response 2"])
    
    if result:
        print("Test Passed: Manager Crew returned a result.")
    else:
        print("Test Failed: Manager Crew returned None or empty result.")

if __name__ == "__main__":
    test_manager_crew()
