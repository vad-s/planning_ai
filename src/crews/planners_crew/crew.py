import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.tests.fake_crewai_llm import MockLLM
from dotenv import load_dotenv

load_dotenv()

mock_llm_creative = MockLLM(responses=["Final Answer: Creative Plan v1"])
mock_llm_balanced = MockLLM(responses=["Final Answer: Balanced Plan v1: 60"])
mock_llm_conservative = MockLLM(responses=["Creative Plan v1,Balanced Plan v1,Conservative Plan v1"])


@CrewBase
class PlannersCrew:
    """Planners Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, use_mock=False, run_only=None, skip_final=False):
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

        self.run_only = run_only
        self.skip_final = skip_final  # Skip final task on re-runs

    @agent
    def creative_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["creative_planner"],
            verbose=True,
            llm=self.llm_creative,
        )

    @agent
    def balanced_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["balanced_planner"],
            verbose=True,
            llm=self.llm_balanced,
        )

    @agent
    def conservative_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["conservative_planner"],
            verbose=True,
            llm=self.llm_conservative,
        )

    @task
    def create_creative_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_creative_plan"],
            async_execution=True,
        )

    @task
    def create_balanced_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_balanced_plan"],
            async_execution=True,
        )

    @task
    def create_conservative_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_conservative_plan"],
            async_execution=True,
        )

    @task
    def write_final(self) -> Task:
        context_tasks = []
        if self.run_only is None:
            context_tasks = [
                self.create_creative_plan(),
                self.create_balanced_plan(),
                self.create_conservative_plan(),
            ]
        else:
            if "creative" in self.run_only:
                context_tasks.append(self.create_creative_plan())
            if "balanced" in self.run_only:
                context_tasks.append(self.create_balanced_plan())
            if "conservative" in self.run_only:
                context_tasks.append(self.create_conservative_plan())

        return Task(
            config=self.tasks_config["create_final_plan"],
            context=context_tasks,
        )

    @crew
    def crew(self) -> Crew:
        tasks_to_run = []
        agents_to_run = []

        if self.run_only is None:
            tasks_to_run = [
                self.create_creative_plan(),
                self.create_balanced_plan(),
                self.create_conservative_plan(),
            ]
        else:
            if "creative" in self.run_only:
                tasks_to_run.append(self.create_creative_plan())
                agents_to_run.append(self.creative_planner())
            if "balanced" in self.run_only:
                tasks_to_run.append(self.create_balanced_plan())
                agents_to_run.append(self.balanced_planner())
            if "conservative" in self.run_only:
                tasks_to_run.append(self.create_conservative_plan())
                agents_to_run.append(self.conservative_planner())

        # Only add final task if not skipping
        if not self.skip_final:
            tasks_to_run.append(self.write_final())

        return Crew(
            agents=self.agents if not agents_to_run else agents_to_run,
            tasks=tasks_to_run,
            process=Process.sequential,
            verbose=True,
        )

    # def run_creative(self, inputs):
    #     return Crew(
    #         agents=[self.creative_planner()],
    #         tasks=[self.create_creative_plan()],
    #         process=Process.sequential,
    #         verbose=True,
    #     ).kickoff(inputs=inputs)

    # def run_balanced(self, inputs):
    #     return Crew(
    #         agents=[self.balanced_planner()],
    #         tasks=[self.create_balanced_plan()],
    #         process=Process.sequential,
    #         verbose=True,
    #     ).kickoff(inputs=inputs)

    # def run_conservative(self, inputs):
    #     return Crew(
    #         agents=[self.conservative_planner()],
    #         tasks=[self.create_conservative_plan()],
    #         process=Process.sequential,
    #         verbose=True,
    #     ).kickoff(inputs=inputs)
