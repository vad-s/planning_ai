from typing import List
from .base import BaseComponent
from .component import Component

class Module(BaseComponent):
    components: List[Component] = []
