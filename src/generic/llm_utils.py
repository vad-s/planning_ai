import os
from crewai import LLM
from src.tests.fake_crewai_llm import MockLLM
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

load_dotenv()

def get_llm(llm_name: LLMName, crew_name: str = None, responses: list = None, temperature: float = 1.0) -> LLM:
    """
    Centralized factory for LLM instances.
    """
    # 1. Handle Mock LLM
    if llm_name == LLMName.MOCK:
        if responses:
            return MockLLM(responses=responses)
        
        # Default mock responses per crew if not provided
        default_responses = {
            "manager_crew": ["project_description_for_planners: |-\n  Vision\n  Build a living flow fitness ecosystem where Nutrition, Exercise, Planning, Tracking, Insights, and a future Suggestion Pillar share a single API-first DNA. The system runs primarily on-device to guarantee privacy and zero-latency experiences, with Local LLM capabilities and a Hybrid RAG stack (Local vector stores plus optional Internet search) to keep responses relevant and up-to-date. No hardware investments are assumed in this phase; hardware considerations are captured in the Suggestion Pillar for future-work planning.\n\n  Unified API DNA\n  - All Pillars implement a single, versioned API contract (v1) that governs core entities, actions, and queries.\n  - Canonical data models (UserProfile, Plan, Meal, Exercise, Log, Insight, Notification) are shared across Pillars with pillar-specific extensions plumbed through the same endpoints.\n  - Endpoints (Create, Read, Update, Delete, Query, Summarize, Link, Notify) use identical payload shapes: { id, type, action, payload, context, metadata, version }.\n  - Inter-Pillar references use universal IDs to enable cross-pillar narratives (e.g., a single Plan referenced by both Nutrition and Planning).\n  - A local Event Bus enforces decoupled, auditable message passing with strict schema validation to ensure Pillars are always readable by any other Pillar.\n\n  Local-first Architecture\n  - Orchestrator: A lightweight on-device orchestrator routes requests to Pillars via the shared API surface. It handles LLM/RAG orchestration, caching, and conflict resolution.\n  - Local LLM: Each user environment ships with a local LLM for natural-language tasks, context management, and on-device reasoning. The LLM operates within a defined memory budget and privacy envelope.\n  - Hybrid RAG: \n    - Local vector stores hold personal documents, recipes, workouts, plans, and logs for fast, private retrieval.\n    - Internet search is optional and gated by the user’s privacy settings; results are re-scored against local knowledge before presentation.\n  - Privacy by design: All data remains on-device by default; cloud sync is opt-in with explicit user consent and strong encryption.\n\n  Pillars and SDU-oriented Growth\n  - Nutrition Pillar: meals, macros, shopping lists, and dietary goals.\n  - Exercise Pillar: workouts, sessions, progress tracking, and form/style guidance.\n  - Planning Pillar: goals, schedules, progression pathways, and milestone tracking.\n  - Tracking Pillar: day-to-day logs, metrics, and trend analysis.\n  - Insights Pillar: cross-pillar analytics, personalized recommendations, and nudges.\n  - Suggestion Pillar (future hardware considerations): capture hardware-readiness, sensor integration, and offline-capable hardware pathways to be evaluated later.\n\n  Non-functional and Roadmap\n  - Latency: on-device processing targeted to near-instant responses for common tasks; heavy computations pass through efficient local LLM/RAG pipelines.\n  - Privacy: strict on-device data handling; opt-in remote features audited and controlled by the user.\n  - Extensibility: API-first contracts enable new Pillars and data types without changing the cross-Pillar API.\n  - Hardware: hardware considerations are deferred to the Suggestion Pillar for evaluation in a future phase.\n\nplanner_task_instructions: |-\n  Objective\n  - Produce an implementable, API-first plan by decomposing the living flow into Small Doable Units (SDUs) per pillar, ensuring a single, shared API DNA across all pillars, and mapping Local LLM/RAG usage with concrete failure points and mitigations."],
            "planners_crew_creative": ["Final Answer: Creative Plan v1"],
            "planners_crew_balanced": ["Final Answer: Balanced Plan v1: 60"],
            "planners_crew_conservative": ["Creative Plan v1,Balanced Plan v1,Conservative Plan v1"],
            "reviewer_crew": ["creative: 75, balanced: 60, conservative: 80"],
            "writer_crew": ["Writer's Final Output"]
        }
        return MockLLM(responses=default_responses.get(crew_name, ["Default Mock Response"]))

    # 2. Handle Azure LLM
    if llm_name == LLMName.GPT5:
        return LLM(
            provider="azure",
            model=os.getenv("AZURE_GPT_5_DEPLOYMENT"),
            api_key=os.getenv("AZURE_GPT_5_API_KEY"),
            endpoint=os.getenv("AZURE_GPT_5_API_BASE"),
            api_version=os.getenv("AZURE_GPT_5_API_VERSION"),
            temperature=temperature,
            max_completion_tokens=1000,
        )
    
    # Default to GPT-4 if GPT4 or anything else (falling back to GPT4 behavior)
    return LLM(
        provider="azure",
        model=os.getenv("AZURE_GPT_4_DEPLOYMENT", "gpt-4o-mini"),
        api_key=os.getenv("AZURE_GPT_4_API_KEY"),
        endpoint=os.getenv("AZURE_GPT_4_API_BASE"),
        api_version=os.getenv("AZURE_GPT_4_API_VERSION"),
        temperature=temperature,
        max_tokens=1000,
    )
