# Designer Crew Standard Output Format

## Overview
All designer agents (creative, balanced, conservative) must follow this standardized YAML format to ensure consistent parsing and processing.

## Standard Format

```yaml
components:
  - name: Component Name
    description: Brief description of the component's purpose and function
    relevant_details:
      - Detail point 1
      - Detail point 2
      - Detail point 3 (optional, can have multiple)
```

## Field Specifications

### `components` (root key)
- **Type**: List
- **Required**: Yes
- **Description**: Top-level array containing all identified system components

### `name`
- **Type**: String
- **Required**: Yes
- **Format**: Use clear, descriptive names (can use spaces)
- **Example**: `"User Profile Management"`, `"Data Entry Interface"`

### `description`
- **Type**: String
- **Required**: Yes
- **Format**: Single or multi-line string describing the component's function
- **Guidelines**: 
  - Be concise but comprehensive
  - Focus on what the component does, not how
  - 1-3 sentences is ideal

### `relevant_details`
- **Type**: List of Strings
- **Required**: No (Optional)
- **Format**: Array of bullet points
- **Guidelines**:
  - Each item should be a complete thought or statement
  - Focus on implementation considerations, benefits, or constraints
  - Typically 2-4 items per component

## Naming Conventions

- **Use snake_case** for all YAML keys (`components`, `name`, `description`, `relevant_details`)
- **Use lowercase** for consistency
- **Avoid abbreviations** unless they are widely understood

## Designer-Specific Guidelines

### Creative Designer
- Focus on novel, imaginative components
- Emphasize innovation and differentiation
- relevant_details should highlight unique aspects or future potential

### Balanced Designer
- Balance innovation with feasibility
- Include practical considerations
- relevant_details should address both benefits and constraints

### Conservative Designer
- Prioritize proven, low-risk components
- Emphasize stability and maintainability
- relevant_details should focus on reliability and compliance

## Example Output

```yaml
components:
  - name: User Profile Management
    description: A secure module for users to create and manage their personal profiles, including health metrics, fitness goals, and preferences.
    relevant_details:
      - Ensures user consent and privacy compliance
      - Allows for easy updates and modifications to personal data
      - Integrates with all tracking and analytics components

  - name: Data Entry Interface
    description: A structured text-based interface for users to input data regarding workouts, meals, hydration, sleep, and body metrics.
    relevant_details:
      - Utilizes proven interaction patterns for ease of use
      - Incorporates validation checks to ensure data accuracy
      - Supports both quick entry and detailed logging modes
```

## Parsing with Pydantic

The standardized format is parsed using the `DesignerCompletion` Pydantic model:

```python
from src.llm_completion.designer_completion import DesignerCompletion
import yaml

# Parse YAML response
yaml_data = yaml.safe_load(raw_response)
designer_output = DesignerCompletion(**yaml_data)

# Access components
for component in designer_output.components:
    print(f"Component: {component.name}")
    print(f"Description: {component.description}")
    if component.relevant_details:
        print(f"Details: {', '.join(component.relevant_details)}")
```

## Migration Notes

Previous formats that are **no longer supported**:
- ❌ `FitnessSystemComponents` (PascalCase root key)
- ❌ `fitness_system_components` (snake_case but non-standard)
- ❌ `Name`, `Description`, `RelevantDetails` (PascalCase fields)
- ❌ `RelevantDetails` as a single string (must be a list)

All designer agents have been updated to use the standard format defined in this document.
