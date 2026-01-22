# 1. Инициализируем State
from src.crews.manager_crew.crew import ManagerCrew
from src.flow.flow import OrcestratorFlow
from src.schemas import concept
from src.state.state import ProjectState


state = ProjectState(concept=="Create a bank app")
    
   
flow = OrcestratorFlow()
flow.state = state
    
manager_crew = ManagerCrew(use_mock=True).crew()
    
flow.kickoff()
 
assert len(flow.state.logical_units) == 2
assert flow.state.all_done is True
print("Flow Test Passed: Manager, Planner, and Writer synced correctly!")