import os
# Set dummy key BEFORE importing crewai to suppress the error
os.environ["OPENAI_API_KEY"] = "fake-key-for-testing"

from crewai import Agent, Task, Crew, BaseLLM
from typing import Any, Dict, List, Optional, Union

class MockLLM(BaseLLM):
   
    def __init__(self, responses: List[str]):
        super().__init__(model="mock", temperature=0)
        self.responses = responses
        self.call_count = 0
    
    def call(
        self,
        messages: Union[str, List[Dict[str, str]]],
        tools: Optional[List[dict]] = None,
        callbacks: Optional[List[Any]] = None,
        available_functions: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response
    
    def supports_function_calling(self) -> bool:
        return False


