import gc
from llama_cpp import Llama
from features.chat.llm_loader.llm_loader_repository_inteface import ILlmLoaderRepository
from typing import List


class LlmModelRepository(ILlmLoaderRepository):
    def __init__(
        self,
        llama_model_path: str,
        n_context_size: int,
        n_threads: int,
        n_gpu_layers: int,
        system_prompts: str,
        use_metal: bool | None,
    ):
        self._llama_model_path = llama_model_path
        self._n_context_size = n_context_size
        self._n_threads = n_threads
        self._n_gpu_layers = n_gpu_layers
        self._system_prompts = system_prompts
        self._use_metal = use_metal

    async def load_model(
        self,
    ) -> Llama:
        print(f"Initializing with {self._system_prompts}")
        model: Llama = Llama(
            verbose=True,
            model_path=self._llama_model_path,
            n_ctx=self._n_context_size,
            n_gpu_layers=self._n_gpu_layers,
            n_threads=self._n_threads,
            use_metal=self._use_metal,
            temperature=0,
            stop=["User:", ">>>"],
            system_prompts=self._system_prompts,
        )
        print(f"Model loaded from {self._llama_model_path}")

        return model

    async def unload_model(self, model: Llama | None):
        print("\nUnloading model from memory to free RAM...\n")
        del model  # Delete the model
        model = None  # Reset to None
        gc.collect()  # Force garbage collection to free memory
        print("\nModel unloaded.\n")

    async def resposne(self, model: Llama, text: str) -> str:
        return ""

    async def chat(self, text: str) -> str:
        print(f"Query from the user : {text}")
        # Load model object
        llm: Llama = await self.load_model()
        # print("Chat text: ", text)
        # Get stream of chats after sending it to the LLM
        response_stream = llm(text, stop=["User:", ">>>"], stream=True, max_tokens=2000)
        ai_response: str = ""

        for chunk in response_stream:
            token = chunk["choices"][0]["text"]
            ai_response = f"{ai_response}{token}"
            print(token, end="", flush=True)

        # unload model and free memory
        await self.unload_model(model=llm)
        return ai_response
