from typing import Any
from abc import ABC


class BaseAlgorithm(ABC):

    def process(self, global_state: dict[str, dict[
            tuple[str, float], int]]
    ) -> tuple[list[list[Any]], float] | tuple[None, None]:
        pass
