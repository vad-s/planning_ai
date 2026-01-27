import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tests.fake_crewai_llm import MockLLM
from dotenv import load_dotenv

load_dotenv()

azure_llm = LLM(
    # Provider name "azure" is supported in CrewAI guides/blogs
    provider="azure",
    model=os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
    api_key=os.getenv("AZURE_API_KEY"),
    # Base endpoint and API version come from your Azure OpenAI resource
    endpoint=os.getenv("AZURE_API_BASE"),
    api_version=os.getenv("AZURE_API_VERSION"),
    # Optional tuning parameters
    temperature=0.7,
    max_tokens=80,
)

# Usage
mock_llm = MockLLM(responses=["Pass to planners"])

@CrewBase
class ManagerCrew:
    """Manager Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, use_mock=False):
        self.llm = mock_llm
        #self.llm = fake_langchain_llm if use_mock else azure_llm

    @agent
    def architect(self) -> Agent:
        print(f"DEBUG: Architect Agent LLM passed: {self.llm}")
        return Agent(
            role="Architect",
            goal="Decompose the idea",
            backstory="Experienced architect",
            verbose=True,
            llm=self.llm
        )

    @task
    def decompose_idea(self) -> Task:
        return Task(
            config=self.tasks_config["decompose_idea"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
