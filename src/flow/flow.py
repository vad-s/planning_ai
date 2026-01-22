from crewai.flow.flow import Flow, start, listen
from state.state import ProjectState


class OrcestratorFlow(Flow[ProjectState]):

    @start()
    def start_flow(self):
        # 1.init state
        # 2.init queue manager
        self.state = ProjectState()
        self.queue = []
        # 3.init log manager
        self.log = []
        # 4.init other components if needed
        self.components = []
        return "run_flow"

    @listen(start_flow)
    def run_flow(self):
        pass
