from typing import Any
from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    """An abstract bas class that serves as a model for every algorithm"""

    @abstractmethod
    def process(self, global_state: dict[str, dict[
            tuple[str, float], int]]
    ) -> tuple[list[list[Any]], float] | tuple[None, None]:
        pass
