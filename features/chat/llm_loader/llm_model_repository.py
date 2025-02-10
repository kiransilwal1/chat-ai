from llama_cpp import Llama
from features.chat.llm_loader.llm_loader_repository_inteface import ILlmLoaderRepository


class LlmModelRepository(ILlmLoaderRepository):
    def __init__(self, llama_model_path: str, context_size: int, threads: int):
        self._llama_model_path = llama_model_path
        self.context_size = context_size
        self.threads = threads

    async def load_model(self) -> Llama | None:
        pass

    async def offload_model(self):
        pass

    async def resposne(self, text: str) -> str:
        return ""
