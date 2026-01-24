import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tests.fake_crewai_llm import MockLLM
from dotenv import load_dotenv

load_dotenv()

mock_llm_creative = MockLLM(responses=["Final Answer: Creative Plan v1"])
mock_llm_balanced = MockLLM(responses=["Final Answer: Balanced Plan v1"])
mock_llm_conservative = MockLLM(responses=["Final Answer: Conservative Plan v1"])

@CrewBase
class PlannersCrew:
    """Planners Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, use_mock=False):
        if use_mock:
            self.llm_creative = mock_llm_creative
            self.llm_balanced = mock_llm_balanced
            self.llm_conservative = mock_llm_conservative
        else:
            base_config = {
                "provider": "azure",
                "model": os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"),
                "api_key": os.getenv("AZURE_API_KEY"),
                "endpoint": os.getenv("AZURE_API_BASE"),
                "api_version": os.getenv("AZURE_API_VERSION"),
                "max_tokens": 80,
            }
            self.llm_creative = LLM(**base_config, temperature=1.0)
            self.llm_balanced = LLM(**base_config, temperature=0.8)
            self.llm_conservative = LLM(**base_config, temperature=0.6)

    @agent
    def creative_planner(self) -> Agent:
        return Agent(
            config="creative_planner",
            verbose=True,
            llm=self.llm_creative
        )

    @agent
    def balanced_planner(self) -> Agent:
        return Agent(
            config="balanced_planner",
            verbose=True,
            llm=self.llm_balanced
        )
    
    @agent
    def conservative_planner(self) -> Agent:
        return Agent(
            config="conservative_planner",
            verbose=True,
            llm=self.llm_conservative
        )

    @task
    def create_creative_plan(self) -> Task:
        return Task(
            config="create_creative_plan",
        )
    
    @task
    def create_balanced_plan(self) -> Task:
        return Task(
            config="create_balanced_plan",
        )

    @task
    def create_conservative_plan(self) -> Task:
        return Task(
            config="create_conservative_plan",
        )

    def run_creative(self, inputs):
        return Crew(
            agents=[self.creative_planner()],
            tasks=[self.create_creative_plan()],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs=inputs)

    def run_balanced(self, inputs):
        return Crew(
            agents=[self.balanced_planner()],
            tasks=[self.create_balanced_plan()],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs=inputs)

    def run_conservative(self, inputs):
        return Crew(
            agents=[self.conservative_planner()],
            tasks=[self.create_conservative_plan()],
            process=Process.sequential,
            verbose=True,
        ).kickoff(inputs=inputs)
