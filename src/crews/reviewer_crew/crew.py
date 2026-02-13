import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

from src.llm_completion.designer_completion import (
    DesignerCompletionJson,
    DesignerOutputsList,
)

load_dotenv()


@CrewBase
class ReviewerCrew:
    """Reviewer Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm_name: LLMName = LLMName.MOCK):
        self.llm_name = llm_name
        self.llm = get_llm(llm_name, "reviewer_crew", temperature=0.7)

    @agent
    def reviewer(self) -> Agent:
        return Agent(config=self.agents_config["reviewer"], verbose=True, llm=self.llm)

    @task
    def review_plan(self) -> Task:
        # Only use output_pydantic for non-mock LLMs
        if self.llm_name != LLMName.MOCK:
            return Task(
                config=self.tasks_config["review_plan"],
            )
        return Task(config=self.tasks_config["review_plan"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.reviewer()],
            tasks=[self.review_plan()],
            process=Process.sequential,
            verbose=True,
            planning_llm=self.llm,
        )
