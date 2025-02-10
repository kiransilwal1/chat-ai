from abc import ABC, abstractmethod


class IChatRepository(ABC):
    @abstractmethod
    async def chat(self, query_string: str) -> str: ...
