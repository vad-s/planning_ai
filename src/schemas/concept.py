from typing import List
from .base import BaseComponent
from .module import Module

class Concept(BaseComponent):
    modules: List[Module] = []