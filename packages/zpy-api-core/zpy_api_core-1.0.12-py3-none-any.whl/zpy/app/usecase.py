from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class UseCase(ABC, Generic[T, S]):
    @abstractmethod
    def execute(self, input: T, *args, **kwargs) -> S:
        """Execute use case"""
        pass
