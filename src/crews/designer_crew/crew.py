import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from src.llm_completion.designer_completion import DesignerCompletionJson
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
        is_creative: bool = False,
    ):
        self.is_creative = is_creative
        self.llm_name_creative = llm_name_creative
        self.llm_name_balanced = llm_name_balanced
        self.llm_name_conservative = llm_name_conservative

    @agent
    def creative_product_designer(self) -> Agent:
        llm = get_llm(
            self.llm_name_creative, "designer_crew_creative_pydantic", temperature=0.8
        )
        return Agent(config=self.agents_config["creative_product_designer"], llm=llm)

    @agent
    def balanced_product_designer(self) -> Agent:
        llm = get_llm(
            self.llm_name_balanced, "designer_crew_balanced_pydantic", temperature=0.6
        )
        return Agent(config=self.agents_config["balanced_product_designer"], llm=llm)

    @agent
    def conservative_product_designer(self) -> Agent:
        llm = get_llm(
            self.llm_name_conservative,
            "designer_crew_conservative_pydantic",
            temperature=0.2,
        )
        return Agent(
            config=self.agents_config["conservative_product_designer"],
            llm=llm,
        )

    # @agent
    # def combiner_agent(self) -> Agent:
    #     # Use mock LLM for combining outputs
    #     llm = get_llm(LLMName.MOCK, "designer_crew_combiner", temperature=0.5)
    #     return Agent(config=self.agents_config["combiner_agent"], llm=llm)

    @task
    def create_creative_plan(self) -> Task:
        # Only use output_pydantic for non-mock LLMs
        if self.llm_name_creative != LLMName.MOCK:
            return Task(
                config=self.tasks_config["create_creative_plan"],
                output_pydantic=DesignerCompletionJson,
            )
        return Task(config=self.tasks_config["create_creative_plan"])

    @task
    def create_balanced_plan(self) -> Task:
        # Only use output_pydantic for non-mock LLMs
        if self.llm_name_balanced != LLMName.MOCK:
            return Task(
                config=self.tasks_config["create_balanced_plan"],
                output_pydantic=DesignerCompletionJson,
            )
        return Task(
            config=self.tasks_config["create_balanced_plan"],
        )

    @task
    def create_conservative_plan(self) -> Task:
        # Only use output_pydantic for non-mock LLMs
        if self.llm_name_conservative != LLMName.MOCK:
            return Task(
                config=self.tasks_config["create_conservative_plan"],
                output_pydantic=DesignerCompletionJson,
            )
        return Task(
            config=self.tasks_config["create_conservative_plan"],
        )

    @task
    def combine_plans(self) -> Task:
        return Task(
            description="Summarize",
            agent=self.conservative_product_designer(),
            async_execution=False,
            context=[
                self.create_creative_plan(),
                self.create_balanced_plan(),
                self.create_conservative_plan(),
            ],
            expected_output="Summary",
        )

    @crew
    def crew(self) -> Crew:
        # Use is_creative to select agents/tasks
        # if self.is_creative:
        #     agents = [self.creative_product_designer()]
        #     tasks = [self.create_creative_plan()]
        # else:
        #     agents = [
        #         self.balanced_product_designer(),
        #         self.conservative_product_designer(),
        #     ]
        #     tasks = [self.create_balanced_plan(), self.create_conservative_plan()]

        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential)
