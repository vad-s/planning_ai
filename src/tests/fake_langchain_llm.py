from langchain_community.llms.fake import FakeListLLM
from crewai import Agent, Task, Crew

# Список ответов, которые "LLM" будет выдавать по очереди
mock_responses = [
    '{"logical_units": [{"id": 1, "title": "Auth Service"}, {"id": 2, "title": "Payment Service"}]}',  # Первый вызов (Planning)
    "The global strategy is to use microservices.",  # Второй вызов (Manager)
    '{"modules": [{"title": "Login Logic", "tasks": []}]}',  # Третий вызов (Deep Dive)
    "Done",  # Четвертый вызов (Writer)
]

fake_llm = FakeListLLM(responses=mock_responses)
