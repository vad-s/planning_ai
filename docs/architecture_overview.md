# Architecture Overview - Planning AI System

**Last Updated:** February 4, 2026  
**Version:** 1.0.0

## Table of Contents
1. [System Purpose](#system-purpose)
2. [High-Level Architecture](#high-level-architecture)
3. [Core Components](#core-components)
4. [Flow Execution Models](#flow-execution-models)
5. [Data Models](#data-models)
6. [Multi-Crew Orchestration](#multi-crew-orchestration)
7. [State Management](#state-management)
8. [Design Decisions](#design-decisions)
9. [Future Architecture](#future-architecture)

---

## System Purpose

The Planning AI system is a **hierarchical project decomposition engine** that uses multiple AI agent crews to break down complex projects into progressively smaller, actionable units.

### Core Mission
Build a "living flow" fitness ecosystem with:
- **Unified API-first architecture**
- **Local LLM capabilities** (privacy-focused)
- **Hybrid RAG system** (local + internet search)
- **Zero-latency planning** for immediate user feedback

### Key Innovation
Rather than a single AI decomposing a project, **4 specialized crews collaborate** at each level of the hierarchy:
1. **Manager** translates high-level ideas into structured briefs
2. **Planners** create 3 parallel plans with different risk profiles
3. **Reviewer** evaluates and synthesizes the best aspects
4. **Writer** produces final documentation and generates child nodes

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Input                              │
│                  (Initial Idea/Concept)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  BFS/DFS Flow Engine                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Work Queue (FIFO/LIFO)                  │  │
│  │  Manages pending nodes at each level                 │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              For Each Node: Multi-Crew Pipeline              │
│                                                               │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌────────┐ │
│  │ Manager │───▶│ Planners │───▶│ Reviewer │───▶│ Writer │ │
│  │  Crew   │    │   Crew   │    │   Crew   │    │  Crew  │ │
│  └─────────┘    └──────────┘    └──────────┘    └────────┘ │
│       │              │                │               │      │
│   [Brief]      [3 Plans]         [Synthesis]    [Children]  │
└─────────────────────┴───────────────────┴──────────────────┘
                      │                   │
                      ▼                   ▼
         ┌────────────────────┐  ┌──────────────────┐
         │   Node Hierarchy   │  │  Output Files    │
         │  (Tree Structure)  │  │  (Markdown/JSON) │
         └────────────────────┘  └──────────────────┘
```

---

## Core Components

### 1. Flow Engine (`src/flows/`)

**Purpose:** Orchestrates traversal of the node hierarchy and crew execution.

**Implementations:**

#### A. BFSNodeFlow (Current/Recommended)
- **File:** `bfs_node_flow.py`
- **Strategy:** Breadth-First Search (level-by-level)
- **Data Model:** Node-based (uses `src/generic/node.py`)
- **Queue:** Processes all nodes at level N before moving to level N+1

**Execution Flow:**
```python
@start()
def start_flow(self):
    # 1. Load configuration (flow_config.yaml, init_idea.yaml)
    # 2. Create root node (depth=0)
    # 3. Enqueue root node
    # 4. Trigger processing

@router(start_flow)
def continue_or_complete(self):
    # Decides whether to process next node or finish
    if pending_queue.empty():
        return "complete"
    else:
        return "process_node"

@listen("process_node")
def process_node(self):
    # 1. Dequeue next node
    # 2. Route through 4-crew pipeline:
    #    manager_crew_done → planners_crew_done → 
    #    reviewer_crew_done → writer_crew_done
    # 3. Writer creates 0-2 child nodes
    # 4. Enqueue children
    # 5. Move processed node to completed queue
```

#### B. BFSFlow (Legacy/Dict-Based)
- **File:** `bfs_flow.py`
- **Strategy:** Breadth-First Search
- **Data Model:** Dict-based work items
- **Status:** Deprecated, kept for reference

#### C. DepthFirstTraversalFlow
- **File:** `depth_first_traversal_flow.py`
- **Strategy:** Depth-First Search (explore one branch fully)
- **Status:** Experimental, not production-ready

---

### 2. Multi-Crew System (`src/crews/`)

Each crew is a self-contained CrewAI agent system with:
- **Agents:** AI personas with specific roles (`agents.yaml`)
- **Tasks:** Work units assigned to agents (`tasks.yaml`)
- **Crew Logic:** Orchestration code (`crew.py`)

#### Crew 1: ManagerCrew
**Purpose:** Transform initial ideas into structured project briefs

**Input:** Raw concept or high-level goal  
**Output:** Detailed project brief with objectives, constraints, success criteria

**Agent Configuration:**
```yaml
manager_agent:
  role: "Project Manager"
  goal: "Transform ideas into clear, actionable project briefs"
  backstory: "Expert at understanding stakeholder needs and translating 
              them into technical requirements"
```

**Current Status:** ✅ Functional (with mock LLM)

---

#### Crew 2: PlannersCrew
**Purpose:** Generate 3 parallel planning approaches

**Input:** Project brief from Manager  
**Output:** 
- **Creative Plan** (temperature=1.0, high-risk/high-reward)
- **Balanced Plan** (temperature=0.8, moderate approach)
- **Conservative Plan** (temperature=0.6, low-risk/proven methods)

**Key Feature:** Async execution - all 3 plans generated in parallel

**Implementation:**
```python
async def kickoff(self) -> TaskOutput:
    creative_task = self.creative_crew.kickoff_async()
    balanced_task = self.balanced_crew.kickoff_async()
    conservative_task = self.conservative_crew.kickoff_async()
    
    return await asyncio.gather(
        creative_task, balanced_task, conservative_task
    )
```

**Current Status:** ✅ Functional (with mock LLM)

---

#### Crew 3: ReviewerCrew
**Purpose:** Evaluate all 3 plans and synthesize best approach

**Input:** 3 plans from Planners  
**Output:** 
- Scores for each plan (creativity, feasibility, risk)
- Synthesized "best-of-all-worlds" recommendation
- Risk analysis

**Agent Configuration:**
```yaml
reviewer_agent:
  role: "Technical Reviewer"
  goal: "Objectively evaluate plans and identify strengths/weaknesses"
  backstory: "Senior architect with experience across multiple domains"
```

**Current Status:** ⚠️ Functional but not integrated (doesn't receive plans)

---

#### Crew 4: WriterCrew
**Purpose:** Finalize documentation and generate child nodes

**Input:** Synthesized plan from Reviewer  
**Output:**
- Markdown documentation for current node
- Decision on child node creation (0-2 children)
- Metadata for next level

**Current Implementation Issues:**
- ❌ Random child generation (should be LLM-driven)
- ❌ Doesn't use reviewer output
- ❌ No actual file writing

**Current Status:** ⚠️ Functional but incomplete

---

### 3. Data Models (`src/generic/`, `src/state/`)

#### Node Hierarchy Model

**BaseSchema** (`base_schema.py`)
```python
class BaseSchema(BaseModel):
    id: str                    # UUID
    created_at: datetime
    updated_at: datetime
    status: str                # WorkStatus enum
    depth_limit: int = 5       # Max tree depth
    level_titles: Dict[int, str]    # {0: "COMPONENT", 1: "MODULE", ...}
    level_statuses: Dict[int, str]  # Status at each level
```

**Node** (`node.py`)
```python
class Node(BaseSchema):
    name: str                  # Node display name
    content: str = ""          # Description/documentation
    depth: int                 # Current level (0=root)
    path: str = ""             # "0->1->2" (lineage)
    parent_id: Optional[str]   # Parent node UUID
    children: List[Node] = []  # Child nodes
```

**Key Features:**
- Self-referencing hierarchy (children contain Node objects)
- Path tracking for lineage visualization
- Depth-aware processing (different behavior per level)
- Immutable IDs (UUID4)

---

#### State Management

**NodeState** (`node_state.py`) - Current/Recommended
```python
class NodeState(BaseModel):
    pending_queue: Deque[Node]     # Work to be done
    completed_queue: Deque[Node]   # Finished work
    current_node: Optional[Node]   # Currently processing
    root_node: Optional[Node]      # Tree root
    depth_limit: int
    save_folder: Path
    project_name: str
```

**ProjectState** (`state.py`) - Legacy/Dict-Based
```python
class ProjectState(BaseModel):
    # 18 fields total (too many responsibilities)
    work_items: List[Dict]         # Legacy dict items
    init_idea: InitIdea
    llm_type: Dict[str, LLMName]
    # ... plus 14 more fields
```

**Recommendation:** Use NodeState exclusively, deprecate ProjectState

---

### 4. LLM Abstraction (`src/generic/llm_utils.py`)

**Purpose:** Provide uniform interface to multiple LLM providers

**Supported Providers:**
```python
class LLMName(Enum):
    MOCK = "mock"      # For testing (returns predefined responses)
    GPT4 = "gpt4"      # Azure OpenAI gpt-4o-mini
    GPT5 = "gpt5"      # Azure OpenAI gpt-5-nano
```

**Usage:**
```python
llm = LLMUtils.get_llm(
    llm_type=LLMName.GPT4,
    temperature=0.8
)
```

**Configuration:** `flow_config.yaml` specifies LLM per crew
```yaml
llm_type:
  manager_crew: "mock"
  planners_crew: "gpt4"
  reviewer_crew: "gpt4"
  writer_crew: "gpt5"
```

---

## Flow Execution Models

### Breadth-First Search (BFS) - Primary

**Strategy:** Process all nodes at level N before moving to level N+1

**Visual:**
```
Root (L0)
├── Child1 (L1)  ◄── Process all L1 first
├── Child2 (L1)  ◄──
└── Child3 (L1)  ◄──
    ├── GrandChild1 (L2)  ◄── Then all L2
    ├── GrandChild2 (L2)  ◄──
    └── GrandChild3 (L2)  ◄──
```

**Advantages:**
- Ensures balanced decomposition
- All siblings at same level of detail
- Easy to visualize progress (by level)

**Implementation:** `BFSNodeFlow` uses `collections.deque` with FIFO behavior

---

### Depth-First Search (DFS) - Experimental

**Strategy:** Explore one branch completely before moving to siblings

**Visual:**
```
Root (L0)
└── Child1 (L1)
    └── GrandChild1 (L2)
        └── GreatGrandChild1 (L3)
            └── ... (explore to leaf)
# Then backtrack to Child2 (L1)
```

**Advantages:**
- Natural for sequential workflows
- Can quickly reach bottom level
- Better for dependency chains

**Status:** Not production-ready, experimental

---

## Design Decisions

### 1. Why Node-Based vs Dict-Based?

**Legacy Approach (Dict-Based):**
```python
work_item = {
    "id": "123",
    "name": "Component",
    "depth": 0,
    "status": "PENDING"
}
```

**Problems:**
- No type safety (typos not caught)
- No validation
- No hierarchical relationships
- Manual serialization

**Current Approach (Node-Based):**
```python
node = Node(
    id="123",
    name="Component",
    depth=0,
    status=WorkStatus.PENDING
)
```

**Benefits:**
- Pydantic validation
- Type hints throughout
- Self-referencing hierarchy
- Auto-serialization to JSON

**Decision:** Commit to Node-based, deprecate dict-based

---

### 2. Why 4 Separate Crews Instead of 1?

**Rationale:**
1. **Specialization:** Each crew optimized for specific task (planning ≠ reviewing)
2. **Parallelism:** Planners run 3 agents concurrently
3. **Temperature Control:** Different creativity levels per crew
4. **Modularity:** Easy to replace/upgrade individual crews
5. **Auditability:** Clear handoffs between stages

**Trade-off:** More complex orchestration, but higher quality output

---

### 3. Why Random Child Generation? (Current Implementation)

**Current Code:**
```python
random_child_count = random.randint(0, 2)
```

**Rationale (Assumed):** Placeholder implementation during development

**Issues:**
- Non-deterministic (breaks testing)
- Ignores complexity analysis
- Not leveraging LLM intelligence

**Planned Fix:** Make Writer LLM decide child count based on:
- Complexity of current node
- Remaining depth budget
- Natural decomposition boundaries

---

### 4. Why BFS as Primary Strategy?

**BFS Advantages:**
- Ensures all high-level components defined before details
- Prevents premature over-engineering of one branch
- Easier to visualize and explain to users
- Natural fit for "level of detail" concept

**DFS Trade-offs:**
- Can dive too deep too fast
- Unbalanced trees
- Harder to estimate total work

**Decision:** BFS primary, DFS available for specialized workflows

---

## State Management Details

### WorkStatus Lifecycle

```
PENDING ──▶ MANAGING ──▶ PLANNING ──▶ REVIEWING ──▶ WRITING ──▶ FINALIZING ──▶ DONE
   │             │            │             │            │             │          │
   │         Manager      Planners      Reviewer      Writer       (Future)   Complete
   │          Crew         Crew          Crew          Crew         Steps
   │
   └──▶ ERROR (if crew fails)
```

**Implementation:**
```python
class WorkStatus(str, Enum):
    PENDING = "PENDING"
    MANAGING = "MANAGING"
    PLANNING = "PLANNING"
    REVIEWING = "REVIEWING"
    WRITING = "WRITING"
    FINALIZING = "FINALIZING"
    DONE = "DONE"
    ERROR = "ERROR"
```

---

### Queue Operations

**Pending Queue (Work To Do):**
```python
# Add new work
state.pending_queue.append(child_node)

# Get next work item
current_node = state.pending_queue.popleft()  # FIFO for BFS
```

**Completed Queue (Audit Trail):**
```python
# Mark work complete
state.completed_queue.append(processed_node)
```

**Current Node (Active Work):**
```python
state.current_node = node_being_processed
```

---

## Future Architecture

### Planned Enhancements

#### 1. Persistence Layer
**Goal:** Save/resume flows, audit history

**Design:**
```python
# Save checkpoint
flow_state.save("output/checkpoint_20260204.json")

# Resume from checkpoint
flow_state = NodeState.load("output/checkpoint_20260204.json")
flow.kickoff(resume=True)
```

**Storage Format:** JSON (human-readable, diff-friendly)

---

#### 2. Output Generation
**Goal:** Write results to markdown/HTML for review

**Design:**
```
output/
├── bfs_runs/
│   └── fitness_v1.0.0_20260204/
│       ├── component_1.md
│       ├── module_1_1.md
│       ├── concept_1_1_1.md
│       └── tree_visualization.html
```

**Features:**
- Markdown per node with AI-generated content
- Interactive tree visualization (D3.js)
- Diff view for iterations

---

#### 3. Crew Output Integration
**Goal:** Pass data between crews

**Design:**
```python
# Manager output
brief = manager_crew.kickoff()
node.metadata["brief"] = parse_brief(brief.raw)

# Pass to Planners
planners_input = {
    "brief": node.metadata["brief"],
    "constraints": node.metadata["constraints"]
}
plans = planners_crew.kickoff(inputs=planners_input)

# Pass to Reviewer
reviewer_input = {
    "plans": plans,
    "criteria": ["feasibility", "innovation", "risk"]
}
synthesis = reviewer_crew.kickoff(inputs=reviewer_input)

# Pass to Writer
writer_input = {
    "synthesis": synthesis,
    "template": get_template_for_level(node.depth)
}
result = writer_crew.kickoff(inputs=writer_input)
```

---

#### 4. LLM-Driven Child Generation
**Goal:** Replace random child count with intelligent decision

**Design:**
```python
# Writer prompt includes:
"""
Based on the complexity of this {level_name}, determine:
1. How many child components are needed? (0-5)
2. What should each child focus on?
3. What is the appropriate level of detail?

Output JSON:
{
  "child_count": 3,
  "children": [
    {"name": "Authentication Module", "focus": "..."},
    {"name": "Data Layer", "focus": "..."},
    {"name": "API Gateway", "focus": "..."}
  ]
}
"""
```

---

#### 5. Web UI / Dashboard
**Goal:** Real-time visualization and control

**Features:**
- Live tree visualization during execution
- Pause/resume/edit flows
- Node editing (modify AI outputs)
- Cost tracking per LLM call
- Performance metrics

**Tech Stack:** React + D3.js + WebSocket

---

## Configuration Files

### flow_config.yaml
```yaml
save_folder: "output/bfs_runs"  # Where results saved
project_name: "fitness"          # Project identifier
version: "v1.0.0"                # Version for folder naming
overwrite: true                  # Reuse folder or timestamp new one

llm_type:                        # LLM per crew
  manager_crew: "mock"
  planners_crew: "gpt4"
  reviewer_crew: "gpt4"
  writer_crew: "gpt5"
```

### init_idea.yaml
```yaml
mission: "Build a living flow fitness ecosystem..."

technical_constraints:
  api_first: "All functionality exposed via API"
  local_llm: "Must support local model deployment"
  privacy: "No external data sharing"

suggestion_pillar_future_experimental:
  hybrid_rag: "Combine local + internet search"
  zero_latency: "Instant feedback for users"

required_output_format_for_planners:
  structure: "Markdown with YAML frontmatter"
  sections: "Overview, Technical, Timeline, Risks"
```

---

## Conclusion

The Planning AI system uses a **multi-crew, BFS-based, Node-hierarchical** architecture for AI-driven project decomposition. The core design is sound but requires:

1. **Integration work** (crew outputs → next crew inputs)
2. **Persistence** (save/resume capability)
3. **Output generation** (write results to files)
4. **Intelligent child generation** (remove randomness)

The Node-based model is superior to dict-based and should be the sole implementation going forward.

---

*For implementation details, see [code_review_findings.md](code_review_findings.md)*  
*For setup instructions, see [setup_guide.md](setup_guide.md)*
