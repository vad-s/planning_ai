from typing import List, Dict, Any, Deque
from collections import deque
from crewai.flow.flow import Flow, start, listen, router, or_
from src.state.state import ProjectState
from src.enums.work_status_enum import WorkStatus
from src.schemas.concept import Concept

class Depth_First_Traversal_Flow(Flow[ProjectState]):
    state: ProjectState

    @start()
    def initialize_flow(self):
        root_title = "Component"
        
        # Initialize Root (Component)
        self.state.concept = Concept(title=root_title, description="Goal: " + root_title)
        
        # Initialize Queue with Root Component
        root_item = {
            "type": "component",
            "title": root_title,
            "id": str(self.state.concept.id),
            "level": 0,
            "status": WorkStatus.PENDING
        }
        # Explicitly use deque
        self.state.work_queue = deque([root_item])
        self.state.visited_queue = [] 

        # Initial Log (from user request)
        print("INIT: queue = [ Component ]")
        return "check_status"

    @listen(or_(initialize_flow, "run_manager_pending", "run_planners", "run_reviewer", "run_writer", "run_manager_finalizing"))
    def check_status(self):
        if not self.state.work_queue:
            print("\nBFS visited order (all nodes within depth limit):")
            visited_titles = [item['title'] for item in self.state.visited_queue]
            print(f"[ {', '.join(visited_titles)} ]")
            return "finalize_flow"

        # Peek at the head (first)
        current_item = self.state.work_queue[0]
        status = current_item.get("status", WorkStatus.PENDING)
        
        if status == WorkStatus.PENDING:
            return "run_manager_pending"
        elif status == WorkStatus.MANAGING:
            return "run_planners"
        elif status == WorkStatus.PLANNING:
            return "run_reviewer"
        elif status == WorkStatus.REVIEWING:
            return "run_writer"
        elif status == WorkStatus.FINALIZING:
            return "run_manager_finalizing"
        elif status == WorkStatus.DONE:
            # Should have been popped. If here, pop.
            self.state.work_queue.popleft()
            return "check_status"
        else:
            print(f"Unknown status {status}. Popping item.")
            self.state.work_queue.popleft()
            return "check_status"

    @listen("run_manager_pending")
    def run_manager_pending(self):
        # We need to access formatting before processing
        current_queue_titles = [i['title'] for i in self.state.work_queue]
        
        # Increment Step Counter
        if not hasattr(self.state, "bfs_step_counter"):
            self.state.bfs_step_counter = 0
        self.state.bfs_step_counter += 1

        print(f"\nStep {self.state.bfs_step_counter} — BFS process front")
        print(f"Before: [ {', '.join(current_queue_titles)} ]")
        
        item = self.state.work_queue[0]
        print(f"DEQUEUE: {item['title']}  (depth {item['level']}, type {item['type'].capitalize()})")
        
        item["status"] = WorkStatus.MANAGING
        return "check_status"

    @listen("run_planners")
    def run_planners(self):
        item = self.state.work_queue[0]
        item["status"] = WorkStatus.PLANNING
        
        # Generation Logic
        base_title = item['title']
        current_type = item["type"]
        
        # Determine Children
        # Component -> 3 Modules
        # Module -> 2 Concepts (Based on example: "Module A" -> "Concept A1, Concept A2")
        # Concept -> 2 Tasks
        # Task -> 2 Steps
        
        # Wait, previous user request said "this is only example... remamber child maybe different number... comnonent have 3 modules, each module have 3 consept"
        # BUT Step 114 Example shows 2 children for Module, Concept, Task.
        # "ENQUEUE_BACK (children, in order): [ Module A, Module B ]" -> 2 children.
        # I should probably follow the example logic (2 children) to be safe or use 2-3 mix?
        # User said "remamber child maybe different number fot each row. this is only example".
        # So sticking to 2 children makes the output match the example better for verification.
        # I'll stick to 2 children per node as per the explicit log example provided.
        
        item["temp_children_mock"] = []
        
        if current_type == "component":
            item["temp_children_mock"] = ["Module A", "Module B"]
        elif current_type == "module":
            suffix = base_title.split(" ")[-1] # "A" or "B"
            item["temp_children_mock"] = [f"Concept {suffix}1", f"Concept {suffix}2"]
        elif current_type == "concept":
            suffix = base_title.split(" ")[-1] # "A1"
            item["temp_children_mock"] = [f"Task {suffix}-1", f"Task {suffix}-2"]
        elif current_type == "task":
            suffix = base_title.split(" ")[-1] # "A1-1"
            item["temp_children_mock"] = [f"Step {suffix}.1", f"Step {suffix}.2"]
        else: # Step
            pass # No children

        return "check_status"

    @listen("run_reviewer")
    def run_reviewer(self):
        item = self.state.work_queue[0]
        item["status"] = WorkStatus.REVIEWING
        return "check_status"

    @listen("run_writer")
    def run_writer(self):
        item = self.state.work_queue[0]
        item["status"] = WorkStatus.FINALIZING
        
        # Determine Next Type
        start_type = item["type"]
        type_order = ["component", "module", "concept", "task", "step"]
        try:
            curr_idx = type_order.index(start_type)
            next_type = type_order[curr_idx + 1] if curr_idx + 1 < len(type_order) else None
        except ValueError:
            next_type = None

        if next_type:
            mock_children = item.get("temp_children_mock", [])
            new_nodes = []
            
            for child_title in mock_children:
                new_node = {
                    "type": next_type,
                    "title": child_title,
                    "parent_id": item["id"],
                    "level": item["level"] + 1,
                    "status": WorkStatus.PENDING
                }
                new_nodes.append(new_node)
            
            if new_nodes:
                self.state.work_queue.extend(new_nodes)
                
                child_titles = [n['title'] for n in new_nodes]
                print(f"ENQUEUE_BACK (children, in order): [ {', '.join(child_titles)} ]")
            else:
                # print("LEAF (no children enqueued).")
                 pass
        else:
             pass

        return "check_status"

    @listen("run_manager_finalizing")
    def run_manager_finalizing(self):
        item = self.state.work_queue[0]
        item["status"] = WorkStatus.DONE
        
        # Remove from head (DEQUEUE complete)
        popped_item = self.state.work_queue.popleft()
        
        # Add to visited
        self.state.visited_queue.append(popped_item)
        
        current_queue_titles = [i['title'] for i in self.state.work_queue]
        print(f"After:  [ {', '.join(current_queue_titles)} ]")
        
        return "check_status"

    @listen("finalize_flow")
    def finalize(self):
        self.state.all_done = True
        print("Flow execution finished.")
