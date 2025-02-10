from abc import ABC, abstractmethod
from llama_cpp import Llama


class ILlmLoaderRepository(ABC):
    @abstractmethod
    async def load_model(self) -> str: ...

    async def offload_model(self): ...
    async def resposne(self, text: str) -> Llama | None: ...
