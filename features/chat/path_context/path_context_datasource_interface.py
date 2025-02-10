from abc import ABC, abstractmethod


class IPathContextDatasource(ABC):
    @abstractmethod
    async def summarize(self, response_string: str, model_path: str) -> str: ...
    @abstractmethod
    async def get_summaries(self) -> str: ...
    @abstractmethod
    async def limit_context(self, text: str) -> str: ...
