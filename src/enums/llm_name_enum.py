from enum import Enum

class LLMName(str, Enum):
    MOCK = "mock"
    GPT4 = "gpt4"
    GPT5 = "gpt5"
