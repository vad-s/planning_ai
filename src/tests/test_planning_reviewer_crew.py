import sys
import os

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.crews.planning_reviewer_crew.crew import PlanningReviewerCrew

def test_planning_reviewer_crew():
    print("Testing Planning Reviewer Crew...")
    
    # Initialize crew with mock
    crew_instance = PlanningReviewerCrew(use_mock=True).crew()
    
    inputs = {
        'plan': 'Initial plan draft...'
    }
    
    print(f"Kicking off Planning Reviewer Crew with inputs: {inputs}")
    result = crew_instance.kickoff(inputs=inputs)
    
    print(f"Result Type: {type(result)}")
    print(f"Result: {result}")
    
    if result:
        print("Test Passed: Planning Reviewer Crew returned a result.")
    else:
        print("Test Failed: Planning Reviewer Crew returned None or empty result.")

if __name__ == "__main__":
    test_planning_reviewer_crew()
