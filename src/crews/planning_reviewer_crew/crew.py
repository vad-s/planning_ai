import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tests.fake_crewai_llm import MockLLM
from dotenv import load_dotenv

load_dotenv()

# reuse the same mock or create a new one if needed, keeping consistency with manager_crew
mock_llm = MockLLM(responses=["Final Answer: Plan looks good, proceed."])

@CrewBase
class PlanningReviewerCrew:
    """Planning Reviewer Crew"""

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
    def planner(self) -> Agent:
        return Agent(
            config=self.agents_config["planner"],
            verbose=True,
            llm=self.llm
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["reviewer"],
            verbose=True,
            llm=self.llm
        )

    @task
    def create_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_plan"],
        )

    @task
    def review_plan(self) -> Task:
        return Task(
            config=self.tasks_config["review_plan"],
            context=[self.create_plan()]
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
