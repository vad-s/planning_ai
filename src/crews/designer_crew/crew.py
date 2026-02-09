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

    def __init__(self, llm_name: LLMName = LLMName.MOCK):
        self.llm = get_llm(llm_name, "designer_crew_creative", temperature=0.7)

    @agent
    def creative_product_designer(self) -> Agent:
        return Agent(
            config=self.agents_config["creative_product_designer"],
            verbose=True,
            llm=self.llm,
        )

    @task
    def create_creative_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_creative_plan"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.creative_product_designer()],
            tasks=[self.create_creative_plan()],
            process=Process.sequential,
            verbose=True,
        )
