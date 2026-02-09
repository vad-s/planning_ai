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
  FitnessSystemComponents:                                                                               
    - Name: User Profiles                                                                                
      Description: Centralized personal accounts that store user-specific data, preferences, and         
  history across health and fitness domains.                                                             
      RelevantDetails: Facilitates tailored recommendations and insights based on individual health      
  journeys.                                                                                              

    - Name: Data Tracking Mechanisms                                                                     
      Description: Systems for logging various aspects of health, such as exercises, meals, hydration,   
  sleep, and body metrics.                                                                               
      RelevantDetails: Users can input data manually, ensuring a comprehensive view of their health     
  without the need for IoT devices.                                                                      

    - Name: Adaptive Recommendation Engine                                                              
      Description: Intelligent system that analyzes user data to provide personalized suggestions for    
  workouts, meals, and habits.                                                                          
      RelevantDetails: Utilizes machine learning algorithms to adapt recommendations as user inputs      
  evolve, enhancing engagement and outcomes.                                                            

    - Name: Holistic Lifestyle Dashboard                                                                 
      Description: A user interface that presents an integrated view of health metrics, progress, and    
  insights in a coherent manner.                                                                         
      RelevantDetails: Emphasizes text-based interaction, enabling users to navigate effortlessly        
  through their health data and insights.                                                                
                                                                                                         
    - Name: Insight Generation Module                                                                   
      Description: Analytical component that transforms tracked data into actionable insights and        
  recommendations for improvement.                                                                       
      RelevantDetails: Incorporates historical data trends to offer users deeper understanding of their  
  habits and long-term performance.                                                                      

    - Name: Privacy and Consent Framework                                                               
      Description: Structures ensuring user data is handled securely, with mechanisms for obtaining      
  explicit consent for data usage.                                                                       
      RelevantDetails: Key to establishing trust and compliance with privacy regulations, laying the     
  groundwork for future enhancements.                                                                   
    
    - Name: Community Engagement Platform                                                               
      Description: A space for users to connect, share experiences, and motivate each other within the   
  fitness ecosystem.                                                                                     
      RelevantDetails: Incorporates text-based interaction to facilitate discussions, feedback, and      
  peer support without the need for visual technology.                                                  
   
    - Name: Feedback Loop System                                                                         
      Description: Mechanism for users to provide feedback on recommendations, tracking accuracy, and    
  overall system usability.                                                                              
      RelevantDetails: Helps refine the recommendation engine and improve user experience by             
  incorporating user insights into system updates.                                                       
    
    - Name: Educational Content Repository                                                              
      Description: A library of articles, videos, and resources focused on health, nutrition, and        
  fitness strategies tailored to user needs.                                                            
      RelevantDetails: Encourages user learning and informed decision-making, enhancing the overall      
Reviewer processing: Smart Home System Concept
Calling Reviewer Crew...
  experience within the fitness platform.                                                               
    - Name: Goal Setting and Progress Tracker                                                           
      Description: Tool that allows users to set personal fitness goals and monitor their progress over  
  time.                                                                                                 
      RelevantDetails: Visualizes achievements and milestones in a text-based format, motivating users   
  to stay committed to their health objectives.                                                         
  ```
"""
balanced_product_designer_response = """
```yaml
fitness_system_components:
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
```yaml
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
```
"""

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
            "designer_crew_creative": [designer_crew_creative_response],
            "designer_crew_balanced": [balanced_product_designer_response],
            "designer_crew_conservative": [designer_crew_conservative_response],
            "planners_crew_creative": [planners_crew_creative_response],
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
