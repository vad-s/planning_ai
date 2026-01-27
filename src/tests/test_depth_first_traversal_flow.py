import json
import sys
import os
from types import SimpleNamespace

# Adjust path to include src
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", ".."))
if src_path not in sys.path:
    sys.path.append(src_path)

from src.flows.depth_first_traversal_flow import Depth_First_Traversal_Flow
from src.schemas.concept import Concept
from src.state.state import ProjectState


def test_flow_initialization_and_outputs():
    # Initialize State
    state = ProjectState()

    # Prepare flow instance
    flow = Depth_First_Traversal_Flow(state=state)

    # Mock Crews
    import src.crews.manager_crew.crew as manager_mod
    import src.crews.planners_crew.crew as planners_mod
    import src.crews.reviewer_crew.crew as reviewer_mod
    import src.crews.writer_crew.crew as writer_mod

    original_manager = manager_mod.ManagerCrew
    original_planners = planners_mod.PlannersCrew
    original_reviewer = reviewer_mod.ReviewerCrew
    original_writer = writer_mod.WriterCrew

    class FakeManagerCrew:
        def __init__(self, use_mock=False):
            pass
        def crew(self):
            return self
        def kickoff(self, inputs=None):
            return SimpleNamespace(raw="Pass to planners")

    class FakePlannersCrew:
        def __init__(self, use_mock=False, run_only=None, skip_final=False):
            pass
        def crew(self):
            return self
        def kickoff(self, inputs=None):
            return SimpleNamespace(raw="Creative Plan v1,Balanced Plan v1,Conservative Plan v1")

    class FakeReviewerCrew:
        def __init__(self, use_mock=False):
            pass
        def crew(self):
            return self
        def kickoff(self, inputs=None):
            return SimpleNamespace(raw="creative: 75, balanced: 60, conservative: 80")

    class FakeWriterCrew:
        def __init__(self, use_mock=False):
            pass
        def crew(self):
            return self
        def kickoff(self, inputs=None):
            return SimpleNamespace(raw="Writer's Final Output")

    manager_mod.ManagerCrew = FakeManagerCrew
    planners_mod.PlannersCrew = FakePlannersCrew
    reviewer_mod.ReviewerCrew = FakeReviewerCrew
    writer_mod.WriterCrew = FakeWriterCrew

    try:
        # Kickoff flow
        flow.kickoff()
        
        print("\nFinal State:")
        print(json.dumps(flow.state.model_dump(mode='json'), indent=2))

        # Assertions
        assert flow.state.concept['title'] == "create system", f"Expected 'create system', got {flow.state.concept['title']}"
        assert flow.state.manager_output == "Pass to planners", "Manager output not correctly saved"
        
        # Checking planner_output
        expected_planner_output = ["Creative Plan v1", "Balanced Plan v1", "Conservative Plan v1"]
        assert flow.state.planner_output == expected_planner_output, f"Expected {expected_planner_output}, got {flow.state.planner_output}"
        assert flow.state.drafts == expected_planner_output, "Drafts not correctly saved"

        # Checking reviewer_output and scores
        assert flow.state.reviewer_output == "creative: 75, balanced: 60, conservative: 80"
        assert flow.state.scores == {"creative": 75, "balanced": 60, "conservative": 80}

        # Checking writer_output
        assert flow.state.writer_output == "Writer's Final Output", "Writer output not correctly saved"
        assert flow.state.all_done is True, "all_done flag not set to True"
        
    finally:
        # restore originals
        manager_mod.ManagerCrew = original_manager
        planners_mod.PlannersCrew = original_planners
        reviewer_mod.ReviewerCrew = original_reviewer
        writer_mod.WriterCrew = original_writer


if __name__ == "__main__":
    test_flow_initialization_and_outputs()
