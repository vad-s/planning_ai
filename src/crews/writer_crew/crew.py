import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tests.fake_crewai_llm import MockLLM
from dotenv import load_dotenv

load_dotenv()

mock_llm = MockLLM(responses=["Final Answer: Here is the written content."])

@CrewBase
class WriterCrew:
    """Writer Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, use_mock=False):
        self.llm = mock_llm if use_mock else LLM(
            provider="azure",
            model=os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
            api_key=os.getenv("AZURE_API_KEY"),
            endpoint=os.getenv("AZURE_API_BASE"),
            api_version=os.getenv("AZURE_API_VERSION"),
            temperature=0.7,
            max_tokens=80,
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer"],
            verbose=True,
            llm=self.llm
        )

    @task
    def write_content(self) -> Task:
        return Task(
            config=self.tasks_config["write_content"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning_llm=self.llm
        )
