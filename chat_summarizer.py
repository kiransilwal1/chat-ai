from llama_cpp import Llama
from code_assistant import CodeAssistant
from typing import Dict, List, Optional
from chat_summarizer_interface import ChatSummarizer


class ChatSummaryGenerator(ChatSummarizer):
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the Code Assistant with configuration from a YAML file."""
        self.config: Dict[str, Optional[str]] = CodeAssistant.load_config(
            config_path
        )  # Type: dict or any specific structure

        model_path: str | None = self.config.get("summary_model_path")
        self.model_path: str = model_path if model_path is not None else ""
        context_size: str | None = self.config.get("summary_context_size")
        self.context_size: int = int(context_size) if context_size is not None else 1024
        # self.context_size: int = self.config.get("context_size", 1024)
        gpu_layers: str | None = self.config.get("summary_gpu_layers")
        self.gpu_layers: int = int(gpu_layers) if gpu_layers is not None else 100
        threads: str | None = self.config.get("summary_threads")
        self.threads: int = int(threads) if threads is not None else 100

        self.llm: Optional[Llama] = (
            None  # Model is not loaded at start (using Optional)
        )
        self.chat_history: List[str] = (
            []
        )  # List of strings to store conversation history

    def summarize(self, text: str) -> str:
        return "Summarized Text"
