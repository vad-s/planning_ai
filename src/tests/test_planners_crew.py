import sys
import os

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.crews.planners_crew.crew import PlannersCrew

def test_planners_crew():
    print("Testing Planners Crew...")
    
    # Initialize crew with mock
    crew_instance = PlannersCrew(use_mock=True).crew()
    
    inputs = {
        'topic': 'AI in Planning',
        'feedback': 'None'
    }
    
    print(f"Kicking off Planners Crew with inputs: {inputs}")
    result = crew_instance.kickoff(inputs=inputs)
    
    print(f"Result Type: {type(result)}")
    print(f"Result: {result}")
    
    if result:
        print("Test Passed: Planners Crew returned a result.")
    else:
        print("Test Failed: Planners Crew returned None or empty result.")

if __name__ == "__main__":
    test_planners_crew()
