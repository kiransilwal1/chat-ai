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


# Either class
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
    def left(value: L) -> "Either[L, R]":  # Explicitly returning Either[L, R]
        return Either(value, is_success=False)

    @staticmethod
    def right(value: R) -> "Either[L, R]":  # Explicitly returning Either[L, R]
        return Either(value, is_success=True)


class UseCase(ABC, Generic[R, Params]):
    """
    An abstract base class for all use cases in the application.

    This class enforces the `call` method, which must be implemented by all subclasses.
    The `call` method should return an `Either[Failure, R]` type, indicating
    either a failure or a successful result.

    Type Parameters:
    - `R`: The return type of the use case (Success).
    - `Params`: The input parameters type for the use case.

    Example Usage:
    ```python
    from core.usecase import UseCase, Either, Failure

    class GetUserUseCase(UseCase[str, int]):
        async def call(self, user_id: int) -> Either[Failure, str]:
            if user_id < 1:
                return Either.left(Failure("Invalid user ID"))
            return Either.right("User data for ID " + str(user_id))
    ```
    """

    @abstractmethod
    async def call(self, params: Params) -> Either[Failure, R]:
        """
        Executes the use case asynchronously.

        Args:
            params (Params): The input parameters required to execute the use case.

        Returns:
            Either[Failure, R]: An Either instance containing either a Failure or the expected result.

        Example:
            ```python
            result = await use_case.call(params)
            if result.is_right():
                print(result.unwrap())  # Successful result
            else:
                print(result.unwrap())  # Failure message
            ```
        """
        pass
