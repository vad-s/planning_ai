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
        self.llm = get_llm(llm_name, "designer_crew", temperature=0.7)

    @agent
    def reviewer(self) -> Agent:
        return Agent(config=self.agents_config["reviewer"], verbose=True, llm=self.llm)

    @task
    def review_plan(self) -> Task:
        return Task(
            config=self.tasks_config["review_plan"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.reviewer()],
            tasks=[self.review_plan()],
            process=Process.sequential,
            verbose=True,
            planning_llm=self.llm,
        )
