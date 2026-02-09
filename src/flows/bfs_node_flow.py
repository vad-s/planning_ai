import random
from collections import deque
from crewai.flow.flow import Flow, start, listen, or_
from src.crews.designer_crew.crew import DesignerCrew
from src.state.node_state import NodeState
from src.enums.work_status_enum import WorkStatus
from src.generic.node import Node
from src.flows.helpers import load_flow_config, setup_output_directory

from src.crews.writer_crew.crew import WriterCrew
from src.crews.manager_crew.crew import ManagerCrew
from src.crews.reviewer_crew.crew import ReviewerCrew
from src.enums.llm_name_enum import LLMName
from src.llm_prompt.task_prompt import TaskPrompt
import yaml

# Level mapping is now inside the Node configuration passed to Root
# But we might need it for reference or just rely on the Node's logic.


class BFSNodeFlow(Flow[NodeState]):
    state: NodeState

    @start()
    def initialize_flow(self):
        print("BFS Node Flow initialized")

        # 1. Read config from resource file
        config = load_flow_config("src/resources/flow_config.yaml")

        # 2. Folder validation/creation
        self.state.output_path = setup_output_directory(config)
        print(f"Output path initialized: {self.state.output_path}")

        # 2.5 Read LLM Config
        self.state.crew_llm_types = config.get("llm_type", {})
        print(f"LLM configurations loaded: {self.state.crew_llm_types}")

        # 3 Load Init Vision as string
        with open("src/resources/init_vision.yaml", "r") as f:
            self.state.project_vision = f.read()

        # 4. Initialize Root Node
        root_title = "Smart Home System Concept"
        root = Node(
            title=root_title,
            depth_limit=4,  # 0=Vision, 1=Zone, 2=Feature, 3=Micro-feature, 4=Atomic Task
            level_titles=["Vision", "Zone", "Feature", "Micro-feature", "Atomic Task"],
            level_statuses={
                0: WorkStatus.INITIALIZING,
                1: WorkStatus.PENDING,
                2: WorkStatus.PENDING,
                3: WorkStatus.PENDING,
                4: WorkStatus.PENDING,
            },
            status=WorkStatus.INITIALIZING,
        )

        # Explicitly use deque of Nodes
        self.state.work_queue = deque([root])
        print(
            f"Queue initialized with: {root.title} ({root.status}) at level {root.level}"
        )

        return "run_manager"

    @listen(or_("initialize_flow", "writer_done"))
    def run_manager(self):
        # 1. Finalize Previous Item
        if (
            self.state.current_item
            and self.state.current_item.status == WorkStatus.WRITING
        ):
            prev_item = self.state.current_item
            print(f"Manager Finalizing: {prev_item.title}")

            # Mark done using helper
            prev_item.mark_done()

            # Move Parent to Visited Queue
            self.state.visited_queue.append(prev_item)

            # Add New Children to Queue
            # Children are already added to prev_item.children in run_writer
            # We just need to enqueue them to work_queue
            new_children = prev_item.children
            # But wait, run_writer creates the children nodes but we processed the *parent*.
            # The newly created children are the ones we want to add to the work queue.
            # We should only add children that are NOT in the queue yet?
            # Since we just created them, they are new.

            if new_children:
                # We need to filter only the *newly created* children if prev_item had children before?
                # But here we assume we create children in this pass.

                # Actually, BFS usually adds checking neighbours.
                # Here "creating children" = "expanding neighbours".
                # We simply extend the queue with the children.

                # Careful: if we re-process a node (unlikely here since we move to visited),
                # we don't want to re-add children.
                # But we move strict to visited.

                print(f"Manager adding {len(new_children)} children to queue.")
                self.state.work_queue.extend(new_children)

            self.state.current_item = None

        # 2. Process Next Item
        if self.state.work_queue:
            item = self.state.work_queue.popleft()

            print(f"Manager processing: {item.title}")

            # Dump call to Manager Crew
            print("Calling Manager Crew...")
            # Use item.level to determine type name if needed via level_titles
            type_name = item.get_title_for_level(item.level) or "Unknown"

            is_initializing = item.status == WorkStatus.INITIALIZING
            if is_initializing:
                vision = self.state.project_vision
            else:
                vision = "none"

            # Get configured LLM
            llm_type_str = self.state.crew_llm_types.get("manager_crew", "mock")
            llm_name = LLMName(llm_type_str)

            inputs = {"vision": vision, "type": type_name}
            try:
                result = (
                    ManagerCrew(llm_name=llm_name, is_initializing=is_initializing)
                    .crew()
                    .kickoff(inputs=inputs)
                )
                print(f"Manager Output: {result}")

                # Parse raw string to TaskPrompt
                try:
                    # Strip markdown code block markers
                    raw_text = result.raw.strip()
                    if raw_text.startswith("```yaml"):
                        raw_text = raw_text[7:]
                    elif raw_text.startswith("```"):
                        raw_text = raw_text[3:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]
                    raw_text = raw_text.strip()

                    parsed_data = yaml.safe_load(raw_text)
                    task_prompt = TaskPrompt(**parsed_data)
                    print(
                        f"Successfully parsed Manager Output to TaskPrompt: {task_prompt}"
                    )
                    # Store task_prompt in state
                    self.state.manager_output = task_prompt
                except Exception as parse_err:
                    print(f"Failed to parse Manager Output to TaskPrompt: {parse_err}")
                    self.state.manager_output = None

            except Exception as e:
                print(f"Manager Crew Call Failed (Mocking continuation): {e}")

            item.status = WorkStatus.MANAGING
            self.state.current_item = item
            return "run_designers"
        else:
            print("Queue empty. Flow Complete.")
            return "flow_complete"

    @listen("run_manager")
    def run_designers(self):
        item = self.state.current_item
        if item:
            print(f"Designers processing: {item.title}")

            print("Calling Designers Crew...")
            llm_creative_str = self.state.crew_llm_types.get(
                "designer_creative_crew", "mock"
            )
            llm_name_creative = LLMName(llm_creative_str)
            print(
                f"LLM Config - Creative: {llm_creative_str}, Balanced: none, Conservative: none"
            )

            # Use manager's parsed output as description for designers
            if not self.state.manager_output:
                raise ValueError("Manager output is None - cannot proceed to designers")

            task_prompt = self.state.manager_output
            project_brief = task_prompt.project_brief
            description = task_prompt.designer_instructions
            expected_output = task_prompt.designer_expected_outputs
            # print(f"Using manager's project_brief: {project_brief[:100]}...")
            # print(f"Using manager's description: {description[:100]}...")
            # print(f"Using manager's expected output: {expected_output}")

            inputs = {
                "project_brief": project_brief,
                "description": description,
                "expected_output": expected_output,
            }
            # inputs = {
            #     "project_brief": "project_brief",
            #     "description": "description",
            #     "expected_output": "expected_output",
            # }
            try:
                # Get configured LLM
                llm_type_str = self.state.crew_llm_types.get(
                    "designer_crew_creative", "mock"
                )
                llm_name = LLMName(llm_type_str)
                result = DesignerCrew(llm_name=llm_name).crew().kickoff(inputs=inputs)
                print(f"Designers Output: {result}")
            except Exception as e:
                print(f"Designers Crew Call Failed: {e}")

            item.status = WorkStatus.DESIGNING
            self.state.current_item = item
            return "run_reviewer"

    # @listen("run_manager")
    # def run_planners(self):
    #     item = self.state.current_item
    #     if item:
    #         print(f"Planners processing: {item.title}")

    #         print("Calling Planners Crew...")
    #         llm_creative_str = self.state.crew_llm_types.get(
    #             "planners_crew_creative", "mock"
    #         )
    #         llm_balanced_str = self.state.crew_llm_types.get(
    #             "planners_crew_balanced", "mock"
    #         )
    #         llm_conservative_str = self.state.crew_llm_types.get(
    #             "planners_crew_conservative", "mock"
    #         )
    #         llm_name_creative = LLMName(llm_creative_str)
    #         llm_name_balanced = LLMName(llm_balanced_str)
    #         llm_name_conservative = LLMName(llm_conservative_str)

    #         print(
    #             f"LLM Config - Creative: {llm_creative_str}, Balanced: {llm_balanced_str}, Conservative: {llm_conservative_str}"
    #         )

    #         # Use manager's parsed output as description for planners
    #         if not self.state.manager_output:
    #             raise ValueError("Manager output is None - cannot proceed to planners")

    #         project_brief = self.state.manager_output.project_brief
    #         description = self.state.manager_output.description
    #         expected_output = self.state.manager_output.expected_output
    #         print(f"Using manager's project_brief: {project_brief[:100]}...")
    #         print(f"Using manager's description: {description[:100]}...")
    #         print(f"Using manager's expected output: {expected_output[:100]}...")

    #         inputs = {
    #             "project_brief": project_brief,
    #             "description": description,
    #             "expected_output": expected_output,
    #         }
    #         try:
    #             result = (
    #                 PlannersCrew(
    #                     llm_name_creative=llm_name_creative,
    #                     # llm_name_balanced=llm_name_balanced,
    #                     # llm_name_conservative=llm_name_conservative,
    #                 )
    #                 .crew()
    #                 .kickoff(inputs=inputs)
    #             )
    #             print(f"Planners Output: {result}")
    #         except Exception as e:
    #             print(f"Planners Crew Call Failed: {e}")

    #         item.status = WorkStatus.PLANNING
    #         self.state.current_item = item
    #         return "run_reviewer"

    @listen("run_designers")
    def run_reviewer(self):
        item = self.state.current_item
        if item:
            print(f"Reviewer processing: {item.title}")

            print("Calling Reviewer Crew...")
            llm_type_str = self.state.crew_llm_types.get("reviewer_crew", "mock")
            llm_name = LLMName(llm_type_str)

            inputs = {"plan": f"Review plan for {item.title}"}
            try:
                result = ReviewerCrew(llm_name=llm_name).crew().kickoff(inputs=inputs)
                print(f"Reviewer Output: {result}")
            except Exception as e:
                print(f"Reviewer Crew Call Failed: {e}")

            item.status = WorkStatus.REVIEWING
            self.state.current_item = item
            return "run_writer"

    @listen("run_reviewer")
    def run_writer(self):
        item = self.state.current_item
        if item:
            print(f"Writer processing: {item.title}")

            print("Calling Writer Crew...")
            llm_type_str = self.state.crew_llm_types.get("writer_crew", "mock")
            llm_name = LLMName(llm_type_str)

            inputs = {"content": f"Write content for {item.title}"}
            try:
                result = WriterCrew(llm_name=llm_name).crew().kickoff(inputs=inputs)
                print(f"Writer Output: {result}")
            except Exception as e:
                print(f"Writer Crew Call Failed: {e}")

            item.status = WorkStatus.WRITING

            # Create Children
            # Use item.add_child()
            # Decide how many children
            current_level = item.level
            # Check if we are at max depth? Node.add_child throws if we exceed.
            # We should check before calling to avoid exception or catch it.

            # Simple check:
            if item.depth_limit is None or current_level < item.depth_limit:
                num_children = random.randint(0, 2)
                # Wait, user example showed "Concept" at level 0.
                # Level 4 is Step.
                # If current is 4 (Step), next is 5.
                # User example `depth_limit=5` passed. Wait, user passed `depth_limit=5` in snippet for `level_titles` of length 5 (0-4).
                # If keys are 0,1,2,3,4.
                # If I go to level 5, `idx` 5 doesn't exist in map.
                # `depth_limit=5` means max depth is 5? Or 5 levels (0-4)?
                # The snippet comment says `depth_limit=5`.
                # The map has keys 0..4.
                # If I am at level 4 (Step), adding child goes to level 5.
                # If map doesn't have 5, `get_title_for_level` returns None.
                # `add_child` logic: `resolved_title = ... else self.get_title_for_level(next_level)`.
                # If None, title is empty "" -> validation might fail if title required?
                # No, `title` is required field in Pydantic model (`BaseSchema`).

                # So we should probably stop if next level doesn't exist in titles map.
                next_level = current_level + 1
                next_type_name = item.get_title_for_level(next_level)

                if next_type_name:
                    print(
                        f"Creating {num_children} children of type {next_type_name} (Level {next_level})"
                    )
                    for i in range(1, num_children + 1):
                        child_name = f"{next_type_name} {i} of {item.title[:15]}..."
                        try:
                            item.add_child(title=child_name)
                        except ValueError as ve:
                            print(f"Skipping child creation: {ve}")
                            break
                else:
                    print("Max Depth reached (no type title), no children.")
            else:
                print("Max Depth limit reached, no children.")

            return "writer_done"
        else:
            print("No current item for writer.")
            return "writer_done"
