from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class ManagerCrew:
    """Manager Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # agents_config = "src/manager_crew/config/agents.yaml"
    # tasks_config = "src/manager_crew/config/tasks.yaml"

    def __init__(self, llm_name: LLMName = LLMName.MOCK, is_initializing: bool = True):
        self.llm = get_llm(llm_name, "manager_crew")
        self.is_initializing = is_initializing

    @agent
    def architect(self) -> Agent:
        print(f"DEBUG: Architect Agent LLM passed: {self.llm}")
        return Agent(config=self.agents_config["architect"], verbose=True, llm=self.llm)

    @task
    def vision_init_task(self) -> Task:
        return Task(
            config=self.tasks_config["vision_init_task"],
            # output_pydantic=TaskPrompt
        )

    @crew
    def crew(self) -> Crew:
        # Determine which task to run
        if self.is_initializing:
            tasks = [self.vision_init_task()]
        else:
            raise ValueError(
                "Empty Crew: No tasks assigned. Set is_initializing=True to run the vision_init_task."
            )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
