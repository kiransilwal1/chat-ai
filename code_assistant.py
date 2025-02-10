from contextlib import redirect_stdout, redirect_stderr
import os
import gc
from llama_cpp import Llama
import yaml
from typing import List, Dict, Optional


def clear_terminal() -> None:
    """Clear the terminal screen for a cleaner UI."""
    print("\033c", end="")


class CodeAssistant:
    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize the Code Assistant with configuration from a YAML file."""
        self.config: Dict[str, Optional[str]] = self.load_config(config_path)
        self.model_path: str | None = self.config.get("model_path")
        if not self.model_path:
            raise ValueError("Error: 'model_path' is missing from the configuration.")
        context_size: str | None = self.config.get("context_size")
        self.context_size: int = int(context_size) if context_size is not None else 1024
        gpu_layers: str | None = self.config.get("gpu_layers")
        self.gpu_layers: int = int(gpu_layers) if gpu_layers is not None else 1024
        threads: str | None = self.config.get("threads")
        self.threads: int = int(threads) if threads is not None else 1024

        self.llm: Optional[Llama] = None  # Model is not loaded at start
        self.chat_history: List[Dict[str, str]] = []  # Stores conversation history

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Optional[str]]:
        """Load configuration from a YAML file."""
        try:
            with open(config_path, "r") as file:
                return yaml.safe_load(file) or {}  # Return empty dict if None
        except FileNotFoundError:
            print(f"Warning: Config file '{config_path}' not found. Using defaults.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {e}")
            return {}

    def load_model(self) -> None:
        """Load the Llama model into memory only when needed."""
        if self.llm is None:
            print("\nLoading model into memory... (This may take a while)\n")

            # Redirect stdout & stderr to suppress unwanted logs
            with (
                open(os.devnull, "w") as fnull,
                redirect_stdout(fnull),
                redirect_stderr(fnull),
            ):
                self.llm = Llama(
                    verbose=False,
                    model_path=self.model_path if self.model_path is not None else "",
                    n_ctx=self.context_size,
                    n_gpu_layers=self.gpu_layers,
                    n_threads=self.threads,
                    use_metal=True,
                )

            print("\nModel loaded successfully.\n")

    def unload_model(self) -> None:
        """Unload the Llama model from memory to free up RAM."""
        if self.llm is not None:
            print("\nUnloading model from memory to free RAM...\n")
            del self.llm  # Delete the model
            self.llm = None  # Reset to None
            gc.collect()  # Force garbage collection to free memory
            print("\nModel unloaded.\n")

    def chat(self, user_input: str) -> None:
        """Send the user's input to the AI model and stream the response."""
        self.load_model()  # Load model only when needed

        # Append the latest message to chat history
        self.chat_history.append({"role": "user", "content": user_input})

        # Estimate token count for each message (approximate words per token: 1.3)
        def estimate_tokens(text: str) -> int:
            return int(len(text.split()) // 1.3)  # Roughly estimate token usage

        # Keep history within token limit (reserve space for new response)
        total_tokens = sum(estimate_tokens(msg["content"]) for msg in self.chat_history)
        max_allowed_history = self.context_size - 500  # Leave space for the response

        while total_tokens > max_allowed_history:
            self.chat_history.pop(0)  # Remove oldest message
            total_tokens = sum(
                estimate_tokens(msg["content"]) for msg in self.chat_history
            )

        # Convert chat history into text format
        chat_history_text = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.chat_history
        )

        # Adjust max_tokens dynamically based on remaining context size
        max_response_tokens = min(2000, self.context_size - total_tokens - 500)
        if self.llm is None:
            raise ValueError("An error occurred: Invalid value")

        response_stream = self.llm(
            f"{chat_history_text}\n\nAssistant:",
            max_tokens=max_response_tokens,
            stop=["User:", ">>>"],
            stream=True,
        )

        print("AI:", end=" ", flush=True)
        ai_response = ""

        for chunk in response_stream:
            token = chunk["choices"][0]["text"]
            ai_response += token
            print(token, end="", flush=True)

        # Store only user inputs in history, AI response is not re-added to prevent unnecessary context growth
        self.chat_history.append({"role": "assistant", "content": ai_response})

        print("\n")
        self.unload_model()  # Free memory after responding

    def start(self) -> None:
        """Start the interactive assistant session with multi-line input support."""
        clear_terminal()
        print(
            "Code Assistant initialized. Type 'exit' to quit or 'EOF' on a new line to submit multi-line input.\n"
        )

        while True:
            print(
                f"How can I help you? (Press Enter for a new line, type 'EOF' to submit): context size is {self.context_size}"
            )
            user_input: List[str] = []

            while True:
                line = input()
                if line.strip().upper() == "EOF":  # Detect end of input
                    break
                user_input.append(line)

            full_input = "\n".join(user_input).strip()

            if full_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            elif full_input:
                self.chat(full_input)


if __name__ == "__main__":
    assistant = CodeAssistant()
    assistant.start()
