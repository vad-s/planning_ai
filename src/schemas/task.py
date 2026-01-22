from typing import List
from .base import BaseComponent
from .step import Step

class Task(BaseComponent):
    steps: List[Step] = []
