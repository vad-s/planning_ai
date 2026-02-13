import os
from typing import Optional
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
        llm_name_creative: Optional[LLMName] = None,
        llm_name_balanced: Optional[LLMName] = None,
        llm_name_conservative: Optional[LLMName] = None,
    ):

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

    @crew
    def crew(self) -> Crew:
        """Create crew with only the agents that have configured LLMs"""
        agents = []
        tasks = []

        # Add creative designer if configured (not None)
        if self.llm_name_creative is not None:
            agents.append(self.creative_product_designer())
            tasks.append(self.create_creative_plan())

        # Add balanced designer if configured (not None)
        if self.llm_name_balanced is not None:
            agents.append(self.balanced_product_designer())
            tasks.append(self.create_balanced_plan())

        # Add conservative designer if configured (not None)
        if self.llm_name_conservative is not None:
            agents.append(self.conservative_product_designer())
            tasks.append(self.create_conservative_plan())

        return Crew(agents=agents, tasks=tasks, process=Process.sequential)
