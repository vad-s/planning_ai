import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from src.llm_prompt.task_prompt import TaskPrompt
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class ManagerCrew:
    """Manager Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm_name: LLMName = LLMName.MOCK, idea=None):
        self.llm = get_llm(llm_name, "manager_crew")
        self.idea = idea

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
            #output_pydantic=TaskPrompt
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
