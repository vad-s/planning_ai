import os
from crewai import LLM
from src.tests.fake_crewai_llm import MockLLM
from src.enums.llm_name_enum import LLMName
from dotenv import load_dotenv

load_dotenv()


# Mock response variables - easy to modify for testing
manager_crew_response = """
```yaml
project_brief: >
  The fitness system aims to establish a fully personal and individual-centric platform that integrates various
  domains of health and fitness, including training, nutrition, habits, and overall wellbeing. It focuses on
  providing a seamless and coherent user experience through tracking mechanisms for exercises, workouts, meals,
  hydration, sleep, and body metrics, while delivering personalized insights based on self-reported data.
  The design emphasizes text-based interaction, structured data entry, adaptive recommendations, and a
  holistic view of lifestyle and performance. Importantly, the architecture is built with future privacy,
  compliance, and security considerations, ensuring a secure, consent-driven environment for personal health.
  In Phase 1, the system purposefully excludes the integration of smartwatches, sensors, and any other
  visual or IoT technologies. Future enhancements will incorporate advanced privacy and security functionalities,
  establishing a robust foundation for the platform's evolution.

planner_instructions: >
  You as a planner need to identify and enumerate all major components implied by the Vision statement provided.
  Each part should be described with a clear name and a concise description that encapsulates its function within
  the system. Additionally, planner is encouraged to consider any relevant details that may enhance the
  understanding of each component. The focus should remain on structural aspects rather than features, ensuring
  a modular approach that aligns with the integrated fitness ecosystem concept.

planner_expected_outputs: >
  A detailed list of major parts, each with: Name, Description, and Relevant details 
```
"""
designers_crew_creative_response = "Final Answer: Creative Design v1"

planners_crew_creative_response = "Final Answer: Creative Plan v1"

planners_crew_balanced_response = "Final Answer: Balanced Plan v1: 60"

planners_crew_conservative_response = (
    "Creative Plan v1,Balanced Plan v1,Conservative Plan v1"
)

reviewer_crew_response = "creative: 75, balanced: 60, conservative: 80"

writer_crew_response = "Writer's Final Output"

default_mock_response = "Default Mock Response"


def get_llm(
    llm_name: LLMName,
    crew_name: str = None,
    responses: list = None,
    temperature: float = 1.0,
) -> LLM:
    """
    Centralized factory for LLM instances.
    """
    # 1. Handle Mock LLM
    if llm_name == LLMName.MOCK:
        if responses:
            return MockLLM(responses=responses)

        # Default mock responses per crew
        default_responses = {
            "manager_crew": [manager_crew_response],
            "designer_creative_crew": [designers_crew_creative_response],
            "planners_crew_balanced": [planners_crew_balanced_response],
            "planners_crew_conservative": [planners_crew_conservative_response],
            "reviewer_crew": [reviewer_crew_response],
            "writer_crew": [writer_crew_response],
        }
        return MockLLM(
            responses=default_responses.get(crew_name, [default_mock_response])
        )

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
        model=f"azure/{os.getenv('AZURE_GPT_4_DEPLOYMENT', 'gpt-4o-mini')}",
        api_key=os.getenv("AZURE_GPT_4_API_KEY"),
        endpoint=os.getenv("AZURE_GPT_4_API_BASE"),
        api_version=os.getenv("AZURE_GPT_4_API_VERSION"),
        temperature=temperature,
        max_tokens=1000,
    )
