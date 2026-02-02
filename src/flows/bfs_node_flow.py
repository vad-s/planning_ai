import random
from collections import deque
from crewai.flow.flow import Flow, start, listen, or_
from src.state.node_state import NodeState
from src.enums.work_status_enum import WorkStatus
from src.schemas.concept import Concept
from src.generic.node import Node

from src.crews.writer_crew.crew import WriterCrew
from src.crews.manager_crew.crew import ManagerCrew
from src.crews.reviewer_crew.crew import ReviewerCrew
from src.crews.planners_crew.crew import PlannersCrew

# Level mapping is now inside the Node configuration passed to Root
# But we might need it for reference or just rely on the Node's logic.

class BFSNodeFlow(Flow[NodeState]):
    state: NodeState

    @start()
    def initialize_flow(self):
        print("BFS Node Flow initialized")
        root_title = "Smart Home System Concept"
        
        # Initialize Root (Concept)
        self.state.concept = Concept(title=root_title, description="Goal: " + root_title)
        
        # Initialize Root Node with configuration
        root = Node(
            title=root_title,
            depth_limit=4, # 0=Concept, 1=Module, 2=Component, 3=Task, 4=Step
            level_titles=["Concept", "Module", "Component", "Task", "Step"],
            level_statuses={
                0: WorkStatus.PENDING,
                1: WorkStatus.PENDING,
                2: WorkStatus.PENDING,
                3: WorkStatus.PENDING,
                4: WorkStatus.PENDING,
            },
        )
        
        # Explicitly use deque of Nodes
        self.state.work_queue = deque([root])
        print(f"Queue initialized with: {root.title} ({root.status}) at level {root.level}")

    @listen(or_(initialize_flow, "run_writer"))
    def run_manager(self):
        # 1. Finalize Previous Item
        if self.state.current_item and self.state.current_item.status == WorkStatus.WRITING:
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
            inputs = {"idea": item.title, "type": type_name}
            try:
                result = ManagerCrew().crew().kickoff(inputs=inputs)
                print(f"Manager Output: {result}")
            except Exception as e:
                print(f"Manager Crew Call Failed (Mocking continuation): {e}")

            item.status = WorkStatus.MANAGING
            self.state.current_item = item
            return "run_planners"
        else:
            print("Queue empty. Flow Complete.")
            return "flow_complete"

    @listen("run_manager")
    def run_planners(self):
        item = self.state.current_item
        if item:
            print(f"Planners processing: {item.title}")
            
            print("Calling Planners Crew...")
            inputs = {"plan": f"Plan for {item.title}"}
            try:
                result = PlannersCrew(use_mock=True).crew().kickoff(inputs=inputs)
                print(f"Planners Output: {result}")
            except Exception as e:
                print(f"Planners Crew Call Failed: {e}")

            item.status = WorkStatus.PLANNING
            self.state.current_item = item

    @listen(run_planners)
    def run_reviewer(self):
        item = self.state.current_item
        if item:
            print(f"Reviewer processing: {item.title}")
            
            print("Calling Reviewer Crew...")
            inputs = {"plan": f"Review plan for {item.title}"}
            try:
                result = ReviewerCrew(use_mock=True).crew().kickoff(inputs=inputs)
                print(f"Reviewer Output: {result}")
            except Exception as e:
                print(f"Reviewer Crew Call Failed: {e}")

            item.status = WorkStatus.REVIEWING
            self.state.current_item = item

    @listen(run_reviewer)
    def run_writer(self):
        item = self.state.current_item
        if item:
            print(f"Writer processing: {item.title}")
            
            print("Calling Writer Crew...")
            inputs = {"content": f"Write content for {item.title}"}
            try:
                result = WriterCrew(use_mock=True).crew().kickoff(inputs=inputs)
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
                     print(f"Creating {num_children} children of type {next_type_name} (Level {next_level})")
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

        else:
            print("No current item for writer.")
        
