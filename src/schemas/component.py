from typing import List
from .base import BaseComponent
from .task import Task

class Component(BaseComponent):
    tasks: List[Task] = []
