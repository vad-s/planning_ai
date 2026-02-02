import random

from collections import deque
from crewai.flow.flow import Flow, start, listen, or_
from src.state.state import ProjectState
from src.enums.work_status_enum import WorkStatus
from src.schemas.concept import Concept

from src.crews.writer_crew.crew import WriterCrew
from src.crews.manager_crew.crew import ManagerCrew
from src.crews.reviewer_crew.crew import ReviewerCrew
from src.crews.planners_crew.crew import PlannersCrew

HIERARCHY_LEVELS = {
    0: "concept",
    1: "module",
    2: "component",
    3: "task",
    4: "step"
}

class BFSFlow(Flow[ProjectState]):
    state: ProjectState

    @start()
    def initialize_flow(self):
        print("BFS Flow initialized")
        root_title = "Smart Home System Concept"
        
        # Initialize Root (Concept)
        self.state.concept = Concept(title=root_title, description="Goal: " + root_title)
        
        # Initialize Queue with Root Concept
        root_item = {
            "type": HIERARCHY_LEVELS[0], # "concept"
            "title": root_title,
            "path": root_title, # Root path
            "id": str(self.state.concept.id),
            "level": 0,
            "status": WorkStatus.PENDING
        }
        # Explicitly use deque
        self.state.work_queue = deque([root_item])
        print(f"Queue initialized with: {root_item['title']} ({root_item['status']})")

    @listen(or_(initialize_flow, "run_writer"))
    def run_manager(self):
        # 1. Finalize Previous Item (if returned from Writer)
        if self.state.current_item and self.state.current_item.get('status') == WorkStatus.WRITING:
            prev_item = self.state.current_item
            print(f"Manager Finalizing: {prev_item['title']}")
            prev_item['status'] = WorkStatus.DONE
            
            # Move Parent to Visited Order (Another Queue)
            self.state.visited_queue.append(prev_item)
            
            # Add New Children to Queue
            new_children = prev_item.get('new_children', [])
            if new_children:
                print(f"Manager adding {len(new_children)} new children to queue.")
                self.state.work_queue.extend(new_children)
            
            self.state.current_item = None

        # 2. Process Next Item
        if self.state.work_queue:
            # Take the head. Since DONE items are moved to visited_queue, 
            # work_queue only contains PENDING items.
            item = self.state.work_queue.popleft()
            
            print(f"Manager processing: {item['title']}")
            
            # Dump call to Manager Crew
            print("Calling Manager Crew...")
            inputs = {"idea": item['title'], "type": item['type']}
            try:
                result = ManagerCrew().crew().kickoff(inputs=inputs)
                print(f"Manager Output: {result}")
            except Exception as e:
                print(f"Manager Crew Call Failed (Mocking continuation): {e}")

            item['status'] = WorkStatus.MANAGING
            self.state.current_item = item
        else:
            print("Queue empty. Flow Complete.")

    @listen(run_manager)
    def run_planners(self):
        item = self.state.current_item
        if item:
            print(f"Planners processing: {item['title']}")
            
            # Dump call to Planners Crew
            print("Calling Planners Crew...")
            inputs = {"plan": f"Plan for {item['title']}"}
            try:
                # Use use_mock=True to use the defined MockLLMs in PlannersCrew
                result = PlannersCrew(use_mock=True).crew().kickoff(inputs=inputs)
                print(f"Planners Output: {result}")
            except Exception as e:
                print(f"Planners Crew Call Failed: {e}")

            item['status'] = WorkStatus.PLANNING
            self.state.current_item = item
        else:
            print("No current item for planners.")

    @listen(run_planners)
    def run_reviewer(self):
        item = self.state.current_item
        if item:
            print(f"Reviewer processing: {item['title']}")
            
            # Dump call to Reviewer Crew
            print("Calling Reviewer Crew...")
            inputs = {"plan": f"Review plan for {item['title']}"}
            try:
                result = ReviewerCrew(use_mock=True).crew().kickoff(inputs=inputs)
                print(f"Reviewer Output: {result}")
            except Exception as e:
                print(f"Reviewer Crew Call Failed: {e}")

            item['status'] = WorkStatus.REVIEWING
            self.state.current_item = item
        else:
            print("No current item for reviewer.")

    @listen(run_reviewer)
    def run_writer(self):
        item = self.state.current_item
        if item:
            print(f"Writer processing: {item['title']}")
            
            # Dump call to Writer Crew
            print("Calling Writer Crew...")
            inputs = {"content": f"Write content for {item['title']}"}
            try:
                result = WriterCrew(use_mock=True).crew().kickoff(inputs=inputs)
                print(f"Writer Output: {result}")
            except Exception as e:
                print(f"Writer Crew Call Failed: {e}")

            item['status'] = WorkStatus.WRITING

            # Create Children
            current_level = item["level"]
            next_level = current_level + 1
            next_type = HIERARCHY_LEVELS.get(next_level)

            item['new_children'] = []
            if next_type:
                num_children = random.randint(0, 2)
                print(f"Creating {num_children} children of type {next_type} (Level {next_level})")
                for i in range(1, num_children + 1):
                    # Naming
                    child_title = f"{next_type.capitalize()} {i} of {item['title'][:15]}..."
                    child_path = f"{item.get('path', item['title'])}/{child_title}"
                        
                    new_node = {
                        "type": next_type,
                        "title": child_title,
                        "path": child_path,
                        "id": f"{item['id']}_{i}",
                        "level": next_level,
                        "status": WorkStatus.PENDING
                    }
                    item['new_children'].append(new_node)
            else:
                print("Leaf node or Max Depth reached, no children.")

        else:
            print("No current item for writer.")
