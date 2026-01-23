import sys
import os

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '..', '..'))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.crews.writer_crew.crew import WriterCrew

def test_writer_crew():
    print("Testing Writer Crew...")
    
    # Initialize crew with mock
    crew_instance = WriterCrew(use_mock=True).crew()
    
    inputs = {
        'topic': 'AI in Planning'
    }
    
    print(f"Kicking off Writer Crew with inputs: {inputs}")
    result = crew_instance.kickoff(inputs=inputs)
    
    print(f"Result Type: {type(result)}")
    print(f"Result: {result}")
    
    if result:
        print("Test Passed: Writer Crew returned a result.")
    else:
        print("Test Failed: Writer Crew returned None or empty result.")

if __name__ == "__main__":
    test_writer_crew()
