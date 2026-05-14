from typing import Any
from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):

    @abstractmethod
    def process(self, global_state: dict[str, dict[
            tuple[str, float], int]]
    ) -> tuple[list[list[Any]], float] | tuple[None, None]:
        pass
