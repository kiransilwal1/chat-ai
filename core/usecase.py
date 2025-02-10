from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

# Define generic types
L = TypeVar("L")  # Left type (Failure)
R = TypeVar("R")  # Right type (Success)
Params = TypeVar("Params")  # Input parameters type


# Failure class representing an error
class Failure:
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Failure: {self.message}"


class Either(Generic[L, R]):
    def __init__(self, value: Union[L, R], is_success: bool):
        self.value = value
        self.is_success = is_success

    def is_left(self) -> bool:
        return not self.is_success

    def is_right(self) -> bool:
        return self.is_success

    def unwrap(self) -> Union[L, R]:
        return self.value

    @staticmethod
    def left(value: L) -> L:
        return value

    @staticmethod
    def right(value: R) -> R:
        return value


# Abstract UseCase class
class UseCase(ABC, Generic[R, Params]):
    @abstractmethod
    async def call(self, params: Params) -> Either[Failure, R]:
        pass
