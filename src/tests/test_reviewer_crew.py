import sys
import os

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.crews.reviewer_crew.crew import ReviewerCrew

def test_reviewer_crew():
    print("Testing Reviewer Crew...")
    
    # Initialize crew with mock
    crew_instance = ReviewerCrew(use_mock=True).crew()
    
    inputs = {
        'plans': 'Plan A, Plan B, Plan C'
    }
    
    print(f"Kicking off Reviewer Crew with inputs: {inputs}")
    result = crew_instance.kickoff(inputs=inputs)
    
    print(f"Result Type: {type(result)}")
    print(f"Result: {result}")
    
    if result:
        print("Test Passed: Reviewer Crew returned a result.")
    else:
        print("Test Failed: Reviewer Crew returned None or empty result.")

if __name__ == "__main__":
    test_reviewer_crew()
