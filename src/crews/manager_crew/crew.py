from crewai import Agent, Crew
from src.tests import fake_llm


class ManagerCrew:
    def __init__(self, use_mock=False):
        self.llm = (
            fake_llm if use_mock else None
        )  # Replace None with actual LLM initialization

    def crew(self) -> Crew:
        planner_agent = Agent(
            role="Architect", goal="Decompose the idea", llm=self.llm, backstory="..."
        )
