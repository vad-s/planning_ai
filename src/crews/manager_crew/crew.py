import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tests.fake_crewai_llm import MockLLM
from .manager_schemas import ArchitectBriefing, DecomposedIdea
from dotenv import load_dotenv

load_dotenv()

azure_llm = LLM(
    # Provider name "azure" is supported in CrewAI guides/blogs
    provider="azure",
    model=os.getenv("AZURE_DEPLOYMENT"),
    api_key=os.getenv("AZURE_API_KEY"),
    # Base endpoint and API version come from your Azure OpenAI resource
    endpoint=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION"),
    # Optional tuning parameters
    temperature=1,
    max_completion_tokens=1000,
)

# Usage
mock_llm = MockLLM(responses=["Pass to planners"])

@CrewBase
class ManagerCrew:
    """Manager Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, use_mock=True, idea=None):
        self.llm = mock_llm if use_mock else azure_llm
        self.idea = idea
        #self.llm.responses[0] = "gkjgkkkg"
        #self.i = 0
        #self.llm = fake_langchain_llm if use_mock else azure_llm

    @agent
    def architect(self) -> Agent:
        print(f"DEBUG: Architect Agent LLM passed: {self.llm}")
        return Agent(
           config=self.agents_config["architect"],
            verbose=True,
            llm=self.llm
        )

    @task
    def decompose_idea(self) -> Task:
        return Task(
            config=self.tasks_config["decompose_idea"],
            #output_pydantic=DecomposedIdea
        )

    @task
    def architect_briefing_task(self) -> Task:
        return Task(
            config=self.tasks_config["architect_briefing_task"],
            #output_pydantic=ArchitectBriefing
        )

    @crew
    def crew(self) -> Crew:
        # Determine which task to run
        if self.idea == "none":
            tasks = [self.decompose_idea()]
        else:
            tasks = [self.architect_briefing_task()]

        return Crew(
            agents=self.agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
