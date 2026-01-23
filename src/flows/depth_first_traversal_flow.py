from crewai.flow.flow import Flow, start, listen
from src.state.state import ProjectState
from src.crews.manager_crew.crew import ManagerCrew
from src.crews.planning_reviewer_crew.crew import PlanningReviewerCrew
from src.crews.writer_crew.crew import WriterCrew

#Runs the method while going deep before siblings.
class Depth_First_Traversal_Flow(Flow):
    state: ProjectState

    @start()
    def get_input(self):
        print("Getting Input")
        topic = "Default Topic"
        
        # Handle state as dict or object
        concept = None
        if isinstance(self.state, dict):
            concept = self.state.get('concept')
        elif hasattr(self.state, 'concept'):
            concept = self.state.concept
            
        if concept:
            if isinstance(concept, dict):
                topic = concept.get('title', topic)
            elif hasattr(concept, 'title'):
                topic = concept.title
                
        return topic

    @listen(get_input)
    def run_manager(self, topic):
        print(f"Running Manager Crew with topic: {topic}")
        inputs = {'topic': topic}
        output = ManagerCrew(use_mock=True).crew().kickoff(inputs=inputs)
        return output.raw

    @listen(run_manager)
    def run_planning_reviewer(self, input):
        print("Running Planning Reviewer Crew")
        inputs = {'plan': input}
        output = PlanningReviewerCrew(use_mock=True).crew().kickoff(inputs=inputs)
        return output.raw

    @listen(run_planning_reviewer)
    def run_writer(self, input):
        print("Running Writer Crew")
        inputs = {'topic': input} # Passing previous output as topic/context
        output = WriterCrew(use_mock=True).crew().kickoff(inputs=inputs)
        return output.raw
