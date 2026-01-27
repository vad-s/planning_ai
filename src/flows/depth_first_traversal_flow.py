from crewai.flow.flow import Flow, start, listen, router
from src.state.state import ProjectState
from src.crews.manager_crew.crew import ManagerCrew
from src.crews.planners_crew.crew import PlannersCrew
from src.crews.reviewer_crew.crew import ReviewerCrew
from src.crews.writer_crew.crew import WriterCrew


# Runs the method while going deep before siblings.
class Depth_First_Traversal_Flow(Flow[ProjectState]):
    state: ProjectState

    @start()
    def get_input(self):
        print("Initializing Concept")
        _concept_str = "create system"
        
        # Initialize state with a specific concept
        concept = {
            "title": _concept_str,
            "description": f"Goal: {_concept_str}",
            "status": "pending"
        }
        
        # with_concept returns a new state, we should update self.state
        self.state.concept = concept

    @listen(get_input)
    def run_manager(self):
        print(f"Running Manager Crew with concept: {self.state.concept['title']}")
        inputs = {"topic": self.state.concept['title']}
        output = ManagerCrew(use_mock=True).crew().kickoff(inputs=inputs)
        self.state.manager_output = output.raw

    @listen(run_manager)
    def run_planning(self):
        print("Running Planning Crew")
        # Use state for inputs
        inputs = {"plan": self.state.manager_output}
        output = PlannersCrew(use_mock=True).crew().kickoff(inputs=inputs)
        # Update state directly 
        self.state.planner_output = [plan.strip() for plan in output.raw.split(',')] 
        self.state.drafts = {
            item.strip().split()[0].lower(): item.strip()
            for item in output.raw.split(",")
            if item.strip()
        } 
        # self.state = self.state.model_copy(update={
        #     "planner_output": output.raw if isinstance(output.raw, list) else [output.raw],
        #     "drafts": output.raw if isinstance(output.raw, dict) else self.state['drafts']
        # })

    @listen(run_planning)
    def run_reviewer(self):
        output = (
            ReviewerCrew(use_mock=True)
            .crew()
            .kickoff(inputs={"drafts": self.state.drafts})
        )
        # Reviewer returns scores: {"creative": 75, "balanced": 60, "conservative": 80}
        self.state.scores = {
            k.strip(): int(v.strip())
            for k, v in (item.split(":") for item in output.raw.split(","))
        }
        self.state.reviewer_output = output.raw

    @router(run_reviewer)
    def check_scores(self):
        # Check which agents failed (score < 70)
        failed = [k for k, v in self.state.scores.items() if v < 70]

        if not failed:
            return "run_writer"
        elif self.state.retry_count < 3:
            return "rerun_failed"
        else:
            return "max_retries"

    @listen(run_reviewer)
    def run_writer(self):
        print("Running Writer Crew")
        # Passing context from state
        inputs = {"topic": self.state.concept['title']} 
        output = WriterCrew(use_mock=True).crew().kickoff(inputs=inputs)
        self.state.writer_output = output.raw
        self.state.all_done = True

    @listen("rerun_failed")
    def rerun_specific_agents(self):
        new_retry_count = self.state.retry_count + 1
        failed = [k for k, v in self.state.scores.items() if v < 70]

        # Re-run ONLY failed agents using same PlannersCrew
        # Using manager_output as the plan basis
        result = (
            PlannersCrew(use_mock=True, run_only=failed, skip_final=True)
            .crew()
            .kickoff(inputs={"plan": self.state.manager_output})
        )

        # Update drafts with new results immutably
        new_drafts = self.state.drafts.copy()
        for agent_type in failed:
            new_drafts[agent_type] = result.raw

        self.state.retry_count = new_retry_count
        self.state.drafts = new_drafts

        return self.run_reviewer()  # Loop back to reviewer

    # @listen("max_retries")
    # def handle_max_retries(self):
    #     return "Max retries reached, using best available drafts"
