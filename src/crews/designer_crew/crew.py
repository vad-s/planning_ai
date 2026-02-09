import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class DesignerCrew:
    """Designer Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(
        self,
        llm_name_creative: LLMName = LLMName.MOCK,
        llm_name_balanced: LLMName = LLMName.MOCK,
        llm_name_conservative: LLMName = LLMName.MOCK,
        is_conservative: bool = False,
    ):
        self.is_conservative = is_conservative
        self.llm_name_creative = llm_name_creative
        self.llm_name_balanced = llm_name_balanced
        self.llm_name_conservative = llm_name_conservative

    @agent
    def creative_product_designer(self) -> Agent:
        llm = get_llm(self.llm_name_creative, "designer_crew_creative", temperature=0.6)
        return Agent(config=self.agents_config["creative_product_designer"], llm=llm)

    @agent
    def balanced_product_designer(self) -> Agent:
        llm = get_llm(self.llm_name_balanced, "designer_crew_balanced", temperature=0.8)
        return Agent(config=self.agents_config["balanced_product_designer"], llm=llm)

    @agent
    def conservative_product_designer(self) -> Agent:
        llm = get_llm(
            self.llm_name_conservative, "designer_crew_conservative", temperature=0.4
        )
        return Agent(
            config=self.agents_config["conservative_product_designer"], llm=llm
        )

    @task
    def create_creative_plan(self) -> Task:
        return Task(config=self.tasks_config["create_creative_plan"])

    @task
    def create_balanced_plan(self) -> Task:
        return Task(config=self.tasks_config["create_balanced_plan"])

    @task
    def create_conservative_plan(self) -> Task:
        return Task(config=self.tasks_config["create_conservative_plan"])

    @crew
    def crew(self) -> Crew:
        # Use is_conservative to select agents/tasks
        if self.is_conservative:
            agents = [self.conservative_product_designer()]
            tasks = [self.create_conservative_plan()]
        else:
            agents = [
                self.creative_product_designer(),
                self.balanced_product_designer(),
            ]
            tasks = [self.create_creative_plan(), self.create_balanced_plan()]

        return Crew(agents=agents, tasks=tasks, process=Process.sequential)
