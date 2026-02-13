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

designer_instructions: >
  As a Designer, need to identify and enumerate all major components implied by the Vision statement provided.
  Each part should be described with a clear name and a concise description that encapsulates its function within
  the system. Additionally, designer is encouraged to consider any relevant details that may enhance the
  understanding of each component. The focus should remain on structural aspects rather than features, ensuring
  a modular approach that aligns with the integrated fitness ecosystem concept.

designer_expected_outputs: >
  A YAML document containing:
  A detailed list of major parts, each with:
  - Name
  - Description
  - Relevant details (optional)
```
"""
designer_crew_creative_response = """
```yaml
agent_name: creative_product_designer
components:
  - name: User Profiles
    description: Centralized personal accounts that store user-specific data, preferences, and history across health and fitness domains.
    relevant_details:
      - Facilitates tailored recommendations and insights based on individual health journeys
      - Supports comprehensive user personalization

  - name: Data Tracking Mechanisms
    description: Systems for logging various aspects of health, such as exercises, meals, hydration, sleep, and body metrics.
    relevant_details:
      - Users can input data manually, ensuring a comprehensive view of their health
      - No IoT devices required in Phase 1

  - name: Adaptive Recommendation Engine
    description: Intelligent system that analyzes user data to provide personalized suggestions for workouts, meals, and habits.
    relevant_details:
      - Utilizes machine learning algorithms to adapt recommendations as user inputs evolve
      - Enhances engagement and outcomes through continuous adaptation

  - name: Holistic Lifestyle Dashboard
    description: A user interface that presents an integrated view of health metrics, progress, and insights in a coherent manner.
    relevant_details:
      - Emphasizes text-based interaction for effortless navigation
      - Provides unified view across all health domains

  - name: Insight Generation Module
    description: Analytical component that transforms tracked data into actionable insights and recommendations for improvement.
    relevant_details:
      - Incorporates historical data trends for deeper understanding
      - Analyzes long-term performance patterns

  - name: Privacy and Consent Framework
    description: Structures ensuring user data is handled securely, with mechanisms for obtaining explicit consent for data usage.
    relevant_details:
      - Key to establishing trust and compliance with privacy regulations
      - Lays groundwork for future security enhancements

  - name: Community Engagement Platform
    description: A space for users to connect, share experiences, and motivate each other within the fitness ecosystem.
    relevant_details:
      - Incorporates text-based interaction to facilitate discussions and feedback
      - Provides peer support without visual technology requirements

  - name: Feedback Loop System
    description: Mechanism for users to provide feedback on recommendations, tracking accuracy, and overall system usability.
    relevant_details:
      - Helps refine the recommendation engine
      - Improves user experience by incorporating user insights into system updates

  - name: Educational Content Repository
    description: A library of articles, videos, and resources focused on health, nutrition, and fitness strategies tailored to user needs.
    relevant_details:
      - Encourages user learning and informed decision-making
      - Enhances the overall experience within the fitness platform

  - name: Goal Setting and Progress Tracker
    description: Tool that allows users to set personal fitness goals and monitor their progress over time.
    relevant_details:
      - Visualizes achievements and milestones in a text-based format
      - Motivates users to stay committed to their health objectives
```
"""
balanced_product_designer_response = """
```yaml
agent_name: balanced_product_designer
components:
  - name: User Profile
    description: A centralized repository for individual user data including demographics, fitness goals, and preferences.
    relevant_details:
      - Facilitates personalized insights and recommendations.
      - Ensures data privacy and compliance by allowing users control over their information.

  - name: Activity Tracker
    description: Mechanism for users to log various physical activities, including workouts and exercises.
    relevant_details:
      - Supports structured data entry through text-based interaction.
      - Provides analytics on performance over time to inform future training adaptations.

  - name: Nutrition Log
    description: Interface for users to record meals, snacks, and hydration intake.
    relevant_details:
      - Enables users to gain insights about their dietary habits and nutritional balance.
      - Can prompt suggestions for healthier food choices based on user preferences and goals.

  - name: Habit Tracker
    description: Tool for users to set and monitor healthy habits surrounding fitness and wellbeing.
    relevant_details:
      - Encourages accountability through reminders and progress tracking.
      - Integrates seamlessly with other components to provide a holistic view of user lifestyle.

  - name: Sleep Monitor
    description: A dedicated section for users to record and evaluate their sleep patterns and quality.
    relevant_details:
      - Offers insights into how sleep affects overall health and performance.
      - May include recommendations for improving sleep habits based on user data.

  - name: Body Metrics Dashboard
    description: Interface for tracking physical metrics such as weight, body fat percentage, and muscle mass.
    relevant_details:
      - Allows users to visualize their progress toward health and fitness goals.
      - Integrates data with activity and nutrition logs for comprehensive analysis.

  - name: Personalized Insights Engine
    description: AI-driven component providing tailored recommendations based on logged activities, nutrition, and metrics.
    relevant_details:
      - Utilizes adaptive algorithms to refine suggestions as user data grows over time.
      - Focuses on encouraging user engagement through actionable insights.

  - name: Data Security Framework
    description: Underlying architecture ensuring user data privacy and compliance with regulations.
    relevant_details:
      - Emphasizes consent-driven data handling, allowing users to manage their data permissions.
      - Prepares for future enhancements related to advanced privacy and security features.

  - name: User Experience Interface
    description: The overarching design that governs user interaction with all components.
    relevant_details:
      - Prioritizes an intuitive text-based interaction model.
      - Ensures a seamless and coherent experience across all areas of the platform.
```
"""

designer_crew_conservative_response = """
agent_name: conservative_product_designer
components:
  - name: User Profile Management
    description: A secure module for users to create and manage their personal profiles, including health metrics, fitness goals, and preferences.  
    relevant_details:
      - Ensures user consent and privacy compliance.
      - Allows for easy updates and modifications to personal data.

  - name: Data Entry Interface
    description: A structured text-based interface for users to input data regarding workouts, meals, hydration, sleep, and body metrics.
    relevant_details:
      - Utilizes proven interaction patterns for ease of use.
      - Incorporates validation checks to ensure data accuracy.

  - name: Activity Tracking System
    description: A mechanism to log and track various fitness activities, including exercises, workouts, and nutrition intake.
    relevant_details:
      - Provides a clear overview of user activity history.
      - Enables users to visualize their progress over time.

  - name: Insights and Recommendations Engine
    description: An analytical component that processes self-reported data to provide personalized insights and adaptive recommendations for health and fitness.
    relevant_details:
      - Utilizes historical data to enhance the relevance of recommendations.
      - Focuses on incremental improvements to user habits and lifestyle.

  - name: Holistic Health Dashboard
    description: A centralized view that aggregates data from various domains of health and fitness, presenting a comprehensive overview of user wellbeing.
    relevant_details:
      - Designed for clarity and usability, ensuring users can easily interpret their health data.
      - Allows for customization based on user preferences.

  - name: Privacy and Security Framework
    description: A foundational architecture ensuring that all user data is stored securely, with compliance to health data regulations and privacy standards.
    relevant_details:
      - Implements encryption and secure access protocols.
      - Regularly updated to address emerging security threats.

  - name: Feedback and Support System
    description: An interface for users to provide feedback on the platform and access support resources, enhancing user engagement and satisfaction.
    relevant_details:
      - Encourages user input for continuous improvement of the platform.
      - Provides clear pathways for addressing user concerns.

  - name: Compliance and Regulatory Module
    description: A component dedicated to ensuring that the platform adheres to relevant health regulations and privacy laws.
    relevant_details:
      - Regular audits and updates to maintain compliance.
      - Facilitates user understanding of their rights and data usage.

  - name: Future Enhancements Framework
    description: A modular architecture designed to accommodate future integrations of IoT devices and advanced privacy features.
    relevant_details:
      - Ensures that the platform can evolve without compromising existing functionality.
      - Focuses on maintaining a low-risk approach to new feature integration.
"""

designer_crew_conservative_json = """
{
  "conservative_product_designer": {
    "is_approved": true,
    "components": [
      {
        "name": "User Profile Management",
        "description": "A secure module for users to create and manage their personal profiles, including health metrics, fitness goals, and preferences.",
        "relevant_details": [
          "Ensures user consent and privacy compliance.",
          "Allows for easy updates and modifications to personal data."
        ]
      },
      {
        "name": "Data Entry Interface",
        "description": "A structured text-based interface for users to input data regarding workouts, meals, hydration, sleep, and body metrics.",
        "relevant_details": [
          "Utilizes proven interaction patterns for ease of use.",
          "Incorporates validation checks to ensure data accuracy."
        ]
      },
      {
        "name": "Activity Tracking System",
        "description": "A mechanism to log and track various fitness activities, including exercises, workouts, and nutrition intake.",
        "relevant_details": [
          "Provides a clear overview of user activity history.",
          "Enables users to visualize their progress over time."
        ]
      },
      {
        "name": "Insights and Recommendations Engine",
        "description": "An analytical component that processes self-reported data to provide personalized insights and adaptive recommendations for health and fitness.",
        "relevant_details": [
          "Utilizes historical data to enhance the relevance of recommendations.",
          "Focuses on incremental improvements to user habits and lifestyle."
        ]
      },
      {
        "name": "Holistic Health Dashboard",
        "description": "A centralized view that aggregates data from various domains of health and fitness, presenting a comprehensive overview of user wellbeing.",
        "relevant_details": [
          "Designed for clarity and usability, ensuring users can easily interpret their health data.",
          "Allows for customization based on user preferences."
        ]
      },
      {
        "name": "Privacy and Security Framework",
        "description": "A foundational architecture ensuring that all user data is stored securely, with compliance to health data regulations and privacy standards.",
        "relevant_details": [
          "Implements encryption and secure access protocols.",
          "Regularly updated to address emerging security threats."
        ]
      },
      {
        "name": "Feedback and Support System",
        "description": "An interface for users to provide feedback on the platform and access support resources, enhancing user engagement and satisfaction.",
        "relevant_details": [
          "Encourages user input for continuous improvement of the platform.",
          "Provides clear pathways for addressing user concerns."
        ]
      },
      {
        "name": "Compliance and Regulatory Module",
        "description": "A component dedicated to ensuring that the platform adheres to relevant health regulations and privacy laws.",
        "relevant_details": [
          "Regular audits and updates to maintain compliance.",
          "Facilitates user understanding of their rights and data usage."
        ]
      },
      {
        "name": "Future Enhancements Framework",
        "description": "A modular architecture designed to accommodate future integrations of IoT devices and advanced privacy features.",
        "relevant_details": [
          "Ensures that the platform can evolve without compromising existing functionality.",
          "Focuses on maintaining a low-risk approach to new feature integration."
        ]
      }
    ]
  }
}
"""
designer_crew_creative_pydantic = """{
    "agent_name": "creative_product_designer",
    "is_approved": false,
    "components": [
        {
            "name": "User Profile Management",
            "description": "Central hub for users to manage personal information, preferences, and privacy settings.",
            "relevant_details": [
                "Facilitates user onboarding and customization.",
                "Ensures compliance with privacy regulations."
            ]
        },
        {
            "name": "Activity Tracker",
            "description": "Mechanism for users to log exercises, workouts, and physical activities.",
            "relevant_details": [
                "Supports text-based entry for activities.",
                "Utilizes adaptive algorithms to suggest future activities."
            ]
        },
        {
            "name": "Nutrition Log",
            "description": "Allows users to track meals, hydration, and nutritional intake.",
            "relevant_details": [
                "Incorporates a structured data entry format for easy logging.",
                "Provides personalized dietary recommendations based on user data."
            ]
        },
        {
            "name": "Habit Formation Module",
            "description": "Tool for users to set, track, and modify lifestyle habits.",
            "relevant_details": [
                "Encourages positive behavior changes through reminders.",
                "Utilizes gamification to enhance user engagement."
            ]
        },
        {
            "name": "Sleep and Recovery Monitor",
            "description": "Component for users to input and analyze their sleep patterns and recovery metrics.",
            "relevant_details": [
                "Offers insights on sleep quality and improvement suggestions.",
                "Integrates with user-reported data for holistic analysis."
            ]
        },
        {
            "name": "Insight Generation Engine",
            "description": "Analyzes user data to provide personalized insights and recommendations.",
            "relevant_details": [
                "Utilizes machine learning to adapt insights over time.",
                "Focuses on a holistic view of health and fitness."
            ]
        },
        {
            "name": "Community Engagement Platform",
            "description": "Facilitates user interaction and support through forums and social features.",
            "relevant_details": [
                "Encourages sharing of experiences and motivation.",
                "Maintains a safe and secure environment for user discussions."
            ]
        },
        {
            "name": "Goal Setting Framework",
            "description": "Allows users to set, track, and achieve personal health and fitness goals.",
            "relevant_details": [
                "Incorporates progress tracking and milestone achievements.",
                "Aligns with user preferences for motivation."
            ]
        }
    ]
}
"""
designer_crew_balanced_pydantic = """{
    "agent_name": "balanced_product_designer",
    "is_approved": false,
    "components": [
        {
            "name": "User Profile Management",
            "description": "A component that allows users to create and manage their personal health profiles, including demographics, fitness goals, and health metrics.",
            "relevant_details": [
                "Supports data input for health conditions, preferences, and fitness aspirations.",
                "Facilitates personalized insights and recommendations based on user data."
            ]
        },
        {
            "name": "Activity Tracking System",
            "description": "An interface for users to log their physical activities, workouts, and exercises, allowing them to track progress over time.",
            "relevant_details": [
                "Enables users to input data manually about workouts and activities.",
                "Provides analytics and trends based on user input to encourage motivation."
            ]
        },
        {
            "name": "Nutrition Logging Module",
            "description": "A feature that enables users to record their food intake and monitor nutritional information to support dietary goals.",
            "relevant_details": [
                "Includes a database of foods and their nutritional values for accurate tracking.",
                "Encourages users to maintain balanced diets by providing meal suggestions."
            ]
        },
        {
            "name": "Habit Analytics Dashboard",
            "description": "A visual representation of user habits related to fitness, nutrition, hydration, and sleep, allowing for self-reflection and improvement.",
            "relevant_details": [
                "Utilizes charts and graphs to present data trends over time.",
                "Encourages healthy habits by showing correlations between habits and well-being."
            ]
        },
        {
            "name": "Personalized Insights Engine",
            "description": "An algorithm that analyzes user data and provides tailored recommendations and insights for enhancing overall health and fitness.",
            "relevant_details": [
                "Generates actionable advice based on user inputs across all tracked domains.",
                "Respects user privacy and consent through secure data handling."
            ]
        },
        {
            "name": "Privacy and Security Framework",
            "description": "A foundational component ensuring that all user data is handled securely, with compliance to privacy regulations and user consent management.",
            "relevant_details": [
                "Incorporates encryption and secure data storage practices.",
                "Offers users transparent control over their data sharing preferences."
            ]
        },
        {
            "name": "Feedback and Support System",
            "description": "A mechanism for users to provide feedback on the platform and receive support for technical or health-related queries.",
            "relevant_details": [
                "Facilitates user engagement and continuous improvement of the platform.",
                "Includes FAQs, chatbot support, and user community features."
            ]
        }
    ]
}
```
"""

designer_crew_conservative_pydantic = """{
    "agent_name": "conservative_product_designer",
    "is_approved": false,
    "components": [
        {
            "name": "User Profile",
            "description": "A secure area where users can manage their personal information, preferences, and consent settings.",
            "relevant_details": [
                "Ensures a consent-driven environment for the user's health data.",
                "Allows for personalized experiences based on user inputs."
            ]
        },
        {
            "name": "Data Entry Interface",
            "description": "Text-based forms and prompts enabling users to input their health and fitness data.",
            "relevant_details": [
                "Structured data entry to minimize user errors.",
                "Focuses on clarity and simplicity in design."
            ]
        },
        {
            "name": "Tracking Mechanisms",
            "description": "Systems that track and log exercises, meals, hydration, sleep, and body metrics over time.",
            "relevant_details": [
                "Facilitates a holistic view of lifestyle and performance.",
                "Emphasizes reliability and consistency in data recording."
            ]
        },
        {
            "name": "Personalized Insights Engine",
            "description": "Analyzes self-reported data to provide tailored feedback and recommendations to users.",
            "relevant_details": [
                "Utilizes proven algorithms for personalized insights.",
                "Incorporates potential for incremental improvements in recommendations over time."
            ]
        },
        {
            "name": "Compliance and Security Framework",
            "description": "Architectural layer ensuring adherence to privacy laws and securing personal health data.",
            "relevant_details": [
                "Established with future enhancements in mind for advanced security functionalities.",
                "Focus on maintaining user trust and data integrity."
            ]
        },
        {
            "name": "Communication Layer",
            "description": "Facilitates text-based interactions and notifications between the system and users.",
            "relevant_details": [
                "Ensures users receive timely updates and insights.",
                "Modular approach allows for easy adjustments in communication methods."
            ]
        }
    ]
}
"""
planners_crew_creative_response = "Final Answer: Creative Plan v1"

planners_crew_balanced_response = "Final Answer: Balanced Plan v1: 60"

planners_crew_conservative_response = (
    "Creative Plan v1,Balanced Plan v1,Conservative Plan v1"
)

reviewer_crew_response = """
[
  {
    "agent_name": "creative_product_designer",
    "is_approved": false,
    "components": [
      {
        "name": "User Profile Management",
        "description": "Central hub for users to manage personal information, preferences, and privacy settings.",
        "relevant_details": [
          "Facilitates user onboarding and customization.",
          "Ensures compliance with privacy regulations."
        ]
      },
      {
        "name": "Activity Tracker",
        "description": "Mechanism for users to log exercises, workouts, and physical activities.",
        "relevant_details": [
          "Supports text-based entry for activities.",
          "Utilizes adaptive algorithms to suggest future activities."
        ]
      },
      {
        "name": "Nutrition Log",
        "description": "Allows users to track meals, hydration, and nutritional intake.",
        "relevant_details": [
          "Incorporates a structured data entry format for easy logging.",
          "Provides personalized dietary recommendations based on user data."
        ]
      },
      {
        "name": "Habit Formation Module",
        "description": "Tool for users to set, track, and modify lifestyle habits.",
        "relevant_details": [
          "Encourages positive behavior changes through reminders.",
          "Utilizes gamification to enhance user engagement."
        ]
      },
      {
        "name": "Sleep and Recovery Monitor",
        "description": "Component for users to input and analyze their sleep patterns and recovery metrics.",
        "relevant_details": [
          "Offers insights on sleep quality and improvement suggestions.",
          "Integrates with user-reported data for holistic analysis."
        ]
      },
      {
        "name": "Insight Generation Engine",
        "description": "Analyzes user data to provide personalized insights and recommendations.",
        "relevant_details": [
          "Utilizes machine learning to adapt insights over time.",
          "Focuses on a holistic view of health and fitness."
        ]
      },
      {
        "name": "Community Engagement Platform",
        "description": "Facilitates user interaction and support through forums and social features.",
        "relevant_details": [
          "Encourages sharing of experiences and motivation.",
          "Maintains a safe and secure environment for user discussions."
        ]
      },
      {
        "name": "Goal Setting Framework",
        "description": "Allows users to set, track, and achieve personal health and fitness goals.",
        "relevant_details": [
          "Incorporates progress tracking and milestone achievements.",
          "Aligns with user preferences for motivation."
        ]
      }
    ]
  },
  {
    "agent_name": "balanced_product_designer",
    "is_approved": true,
    "components": [
      {
        "name": "User Profile Management",
        "description": "A component that allows users to create and manage their personal health profiles, including demographics, fitness goals, and health metrics.",
        "relevant_details": [
          "Supports data input for health conditions, preferences, and fitness aspirations.",
          "Facilitates personalized insights and recommendations based on user data."
        ]
      },
      {
        "name": "Activity Tracking System",
        "description": "An interface for users to log their physical activities, workouts, and exercises, allowing them to track progress over time.",
        "relevant_details": [
          "Enables users to input data manually about workouts and activities.",
          "Provides analytics and trends based on user input to encourage motivation."
        ]
      },
      {
        "name": "Nutrition Logging Module",
        "description": "A feature that enables users to record their food intake and monitor nutritional information to support dietary goals.",
        "relevant_details": [
          "Includes a database of foods and their nutritional values for accurate tracking.",
          "Encourages users to maintain balanced diets by providing meal suggestions."
        ]
      },
      {
        "name": "Habit Analytics Dashboard",
        "description": "A visual representation of user habits related to fitness, nutrition, hydration, and sleep, allowing for self-reflection and improvement.",
        "relevant_details": [
          "Utilizes charts and graphs to present data trends over time.",
          "Encourages healthy habits by showing correlations between habits and well-being."
        ]
      },
      {
        "name": "Personalized Insights Engine",
        "description": "An algorithm that analyzes user data and provides tailored recommendations and insights for enhancing overall health and fitness.",
        "relevant_details": [
          "Generates actionable advice based on user inputs across all tracked domains.",
          "Respects user privacy and consent through secure data handling."
        ]
      },
      {
        "name": "Privacy and Security Framework",
        "description": "A foundational component ensuring that all user data is handled securely, with compliance to privacy regulations and user consent management.",
        "relevant_details": [
          "Incorporates encryption and secure data storage practices.",
          "Offers users transparent control over their data sharing preferences."
        ]
      },
      {
        "name": "Feedback and Support System",
        "description": "A mechanism for users to provide feedback on the platform and receive support for technical or health-related queries.",
        "relevant_details": [
          "Facilitates user engagement and continuous improvement of the platform.",
          "Includes FAQs, chatbot support, and user community features."
        ]
      }
    ]
  },
  {
    "agent_name": "conservative_product_designer",
    "is_approved": true,
    "components": [
      {
        "name": "User Profile",
        "description": "A secure area where users can manage their personal information, preferences, and consent settings.",
        "relevant_details": [
          "Ensures a consent-driven environment for the user's health data.",
          "Allows for personalized experiences based on user inputs."
        ]
      },
      {
        "name": "Data Entry Interface",
        "description": "Text-based forms and prompts enabling users to input their health and fitness data.",
        "relevant_details": [
          "Structured data entry to minimize user errors.",
          "Focuses on clarity and simplicity in design."
        ]
      },
      {
        "name": "Tracking Mechanisms",
        "description": "Systems that track and log exercises, meals, hydration, sleep, and body metrics over time.",
        "relevant_details": [
          "Facilitates a holistic view of lifestyle and performance.",
          "Emphasizes reliability and consistency in data recording."
        ]
      },
      {
        "name": "Personalized Insights Engine",
        "description": "Analyzes self-reported data to provide tailored feedback and recommendations to users.",
        "relevant_details": [
          "Utilizes proven algorithms for personalized insights.",
          "Incorporates potential for incremental improvements in recommendations over time."
        ]
      },
      {
        "name": "Compliance and Security Framework",
        "description": "Architectural layer ensuring adherence to privacy laws and securing personal health data.",
        "relevant_details": [
          "Established with future enhancements in mind for advanced security functionalities.",
          "Focus on maintaining user trust and data integrity."
        ]
      },
      {
        "name": "Communication Layer",
        "description": "Facilitates text-based interactions and notifications between the system and users.",
        "relevant_details": [
          "Ensures users receive timely updates and insights.",
          "Modular approach allows for easy adjustments in communication methods."
        ]
      }
    ]
  }
]
"""

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

    Args:
        llm_name: The LLM type to use
        crew_name: Name of the crew (used for default mock responses)
        responses: Custom responses for MockLLM
        temperature: Temperature setting for the LLM
    """
    # 1. Handle Mock LLM
    if llm_name == LLMName.MOCK:
        if responses:
            return MockLLM(responses=responses)

        # Default mock responses per crew
        default_responses = {
            "manager_crew": [manager_crew_response],
            "designer_crew_creative": [designer_crew_creative_response],
            "designer_crew_creative_pydantic": [designer_crew_creative_pydantic],
            "designer_crew_balanced": [balanced_product_designer_response],
            "designer_crew_balanced_pydantic": [designer_crew_balanced_pydantic],
            "designer_crew_conservative": [designer_crew_conservative_response],
            "designer_crew_conservative_json": [designer_crew_conservative_json],
            "designer_crew_conservative_pydantic": [
                designer_crew_conservative_pydantic
            ],
            "planners_crew_creative": [planners_crew_creative_response],
            "planners_crew_balanced": [planners_crew_balanced_response],
            "planners_crew_conservative": [planners_crew_conservative_response],
            "reviewer_crew": [reviewer_crew_response],
            "writer_crew": [writer_crew_response],
        }

        crew_config = default_responses.get(crew_name, [default_mock_response])
        return MockLLM(responses=crew_config)

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
    )
