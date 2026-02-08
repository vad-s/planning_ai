import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class PlannersCrew:
    """Planners Crew"""

    # agents_config = os.path.join(_base_path, "config/agents_new.yaml")
    # tasks_config = os.path.join(_base_path, "config/tasks.yaml")

    agents_config = "config/agents_new.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, llm_name_creative: LLMName = LLMName.MOCK):
        self.llm = get_llm(llm_name_creative, "planners_crew_creative")

    @agent
    def architect(self) -> Agent:
        print(f"DEBUG: Architect Agent LLM passed: {self.llm}")
        print(self.agents_config.keys())
        return Agent(
            agents_config=self.agents_config["creative_product_designer1"],
            verbose=True,
            llm=self.llm,
        )

    @task
    def vision_init_task(self) -> Task:
        return Task(
            tasks_config=self.tasks_config["create_creative_plan"],
            # output_pydantic=TaskPrompt
        )

    @crew
    def crew(self) -> Crew:
        print(self.agents_config.keys())
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
