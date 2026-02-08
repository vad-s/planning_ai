import os
import yaml
from pathlib import Path
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.generic.llm_utils import get_llm
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class PlannersCrew:
    """Planners Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(
        self,
        llm_name_creative: LLMName = None,
        llm_name_balanced: LLMName = None,
        llm_name_conservative: LLMName = None,
        run_only=None,
        skip_final=False,
    ):
        # Manually load configs if CrewBase didn't do it properly
        if not isinstance(self.agents_config, dict):
            config_dir = Path(__file__).parent / "config"
            with open(config_dir / "agents.yaml", "r") as f:
                self.agents_config = yaml.safe_load(f)
            with open(config_dir / "tasks.yaml", "r") as f:
                self.tasks_config = yaml.safe_load(f)
            print(f"[INFO] Manually loaded configs from {config_dir}")

        print(
            f"[DEBUG INIT] agents_config keys: {list(self.agents_config.keys()) if isinstance(self.agents_config, dict) else 'N/A'}"
        )

        try:
            # Use individual LLM names if provided, otherwise fall back to single llm_name
            creative_llm = (
                llm_name_creative if llm_name_creative is not None else LLMName.MOCK
            )
            balanced_llm = (
                llm_name_balanced if llm_name_balanced is not None else LLMName.MOCK
            )
            conservative_llm = (
                llm_name_conservative
                if llm_name_conservative is not None
                else LLMName.MOCK
            )

            self.llm_creative = get_llm(
                creative_llm, "planners_crew_creative", temperature=0.6
            )
            self.llm_balanced = get_llm(
                balanced_llm, "planners_crew_balanced", temperature=0.8
            )
            self.llm_conservative = get_llm(
                conservative_llm, "planners_crew_conservative", temperature=1.0
            )

            self.run_only = run_only
            self.skip_final = skip_final
        except Exception as e:
            print(f"[ERROR] Failed to initialize LLMs: {e}")
            raise

    @agent
    def creative_planner(self) -> Agent:
        print("[Agent] Creative Planner initialized")
        print(
            f"[DEBUG AGENT] agents_config type in creative_planner: {type(self.agents_config)}"
        )
        print(f"[DEBUG AGENT] agents_config value: {self.agents_config}")
        if isinstance(self.agents_config, dict):
            print(f"[DEBUG] Available agent keys: {list(self.agents_config.keys())}")
            print(f"[DEBUG] Looking for key: 'creative_product_designer'")
        try:
            return Agent(
                config=self.agents_config["creative_product_designer"],
                verbose=True,
                llm=self.llm_creative,
            )
        except KeyError as e:
            print(f"[ERROR] KeyError: {e}")
            print(f"[ERROR] Available keys: {list(self.agents_config.keys())}")
            print(f"[ERROR] agents_config content: {self.agents_config}")
            raise

    @agent
    def balanced_planner(self) -> Agent:
        print("[Agent] Balanced Planner initialized")
        try:
            return Agent(
                config=self.agents_config["balanced_product_designer"],
                verbose=True,
                llm=self.llm_balanced,
            )
        except KeyError as e:
            print(f"[ERROR] KeyError in balanced_planner: {e}")
            print(f"[ERROR] Available keys: {list(self.agents_config.keys())}")
            print(f"[ERROR] agents_config content: {self.agents_config}")
            raise

    @agent
    def conservative_planner(self) -> Agent:
        print("[Agent] Conservative Planner initialized")
        try:
            return Agent(
                config=self.agents_config["conservative_product_designer"],
                verbose=True,
                llm=self.llm_conservative,
            )
        except KeyError as e:
            print(f"[ERROR] KeyError in conservative_planner: {e}")
            print(f"[ERROR] Available keys: {list(self.agents_config.keys())}")
            print(f"[ERROR] agents_config content: {self.agents_config}")
            raise

    @task
    def create_creative_plan(self) -> Task:
        print("[Task] Create Creative Plan - async execution")
        return Task(
            config=self.tasks_config["create_creative_plan"],
            async_execution=True,
        )

    @task
    def create_balanced_plan(self) -> Task:
        print("[Task] Create Balanced Plan - async execution")
        return Task(
            config=self.tasks_config["create_balanced_plan"],
            async_execution=True,
        )

    @task
    def create_conservative_plan(self) -> Task:
        print("[Task] Create Conservative Plan - async execution")
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

        print(f"[Task] Create Final Plan - waiting for {len(context_tasks)} tasks")
        return Task(
            config=self.tasks_config["create_final_plan"],
            context=context_tasks,
        )

    @crew
    def crew(self) -> Crew:
        tasks_to_run = []
        agents_to_run = []

        if self.run_only is None:
            print("[Crew] Running all planners: Creative, Balanced, Conservative")
            tasks_to_run = [
                self.create_creative_plan(),
                self.create_balanced_plan(),
                self.create_conservative_plan(),
            ]
            agents_to_run = [
                self.creative_planner(),
                self.balanced_planner(),
                self.conservative_planner(),
            ]
        else:
            print(f"[Crew] Running selected planners: {self.run_only}")
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
            print("[Crew] Adding final synthesis task (Conservative Planner)")
            tasks_to_run.append(self.write_final())
        else:
            print("[Crew] Skipping final synthesis task")

        print(
            f"[Crew] Total tasks: {len(tasks_to_run)}, Total agents: {len(agents_to_run)}"
        )
        return Crew(
            agents=agents_to_run,
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
