import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List, cast
from features.chat.chat_explorer.chat_explorer_datasource_interface import (
    IChatExplorerDatasource,
)
from features.chat.chat_explorer.chat_explorer_sqlite_datasource import (
    ChatExplorerSqlite,
)
from features.chat.chat_explorer.chat_repository_impl import ChatExplorerRepository
from features.chat.chat_explorer.chat_repositroy_interface import (
    ChatEntity,
    IChatExplorerRepository,
)
from features.chat.chat_explorer.get_all_chats_usecase import GetAllChatsUseCase
from features.chat.code_assistant_usecase import CodeAssistantUseCase
import os
import yaml
from typing import Dict, Optional

from features.chat.llm_loader.llm_loader_repository_inteface import ILlmLoaderRepository
from features.chat.llm_loader.llm_model_repository import LlmModelRepository
from features.chat.path_context.path_context_datasource_interface import (
    IPathContextDatasource,
)
from features.chat.path_context.path_context_repo_impl import PathContextRepository
from features.chat.path_context.path_context_repository_interface import (
    IPathContextRepository,
)
from features.chat.path_context.path_context_sqlite_datasource import PathContextSqlite


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


def clear_terminal() -> None:
    """Clear the terminal screen for a cleaner UI."""
    print("\033c", end="")


async def start(
    assistant: CodeAssistantUseCase, chat_explorer: GetAllChatsUseCase
) -> None:
    """Start the interactive assistant session with multi-line input support."""
    clear_terminal()
    print(
        "Code Assistant initialized. Type 'exit' to quit or 'EOF' on a new line to submit multi-line input.\n"
    )
    while True:
        print(
            f"How can I help you? (Press Enter for a new line, type 'EOF' to submit): "
        )
        user_input: List[str] = []

        while True:
            line = input()
            if line.strip().upper() == "EOF":  # Detect end of input
                break
            user_input.append(line)

        full_input = "\n".join(user_input).strip()

        if full_input.lower() in {"exit", "quit", "history"}:
            if full_input.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            elif full_input.lower() in {"history"}:
                chats = await chat_explorer.call(params=None)
                if chats.is_right():  # Check if the call was successful
                    chat_list: List[ChatEntity] = cast(
                        List[ChatEntity], chats.unwrap()
                    )  # Extract the value
                    print(f"Chat List : {chat_list}")
                    for chat in chat_list:
                        print(f"Chat ID: {chat.id}, Summary: {chat.summary}")
                else:
                    print(f"Error: {chats.unwrap()}")  # Handle failure case
                # print(chats.value)
                # break
        elif full_input:
            response = await assistant.call(params=full_input)


async def main():
    # DATABASE_URL = f"sqlite:///{os.path.expanduser('~')}/.chatai/db.sqlite"
    # CONFIG_FILE = f"{os.path.expanduser('~')}/.chatai/config.yaml"
    DATABASE_URL = f"sqlite:///{os.path.expanduser('~')}/.chatai/db.sqlite"
    CONFIG_FILE = f"{os.getcwd()}/config.yaml"

    # LLM Responder
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    config: Dict[str, Optional[str]] = load_config(config_path=CONFIG_FILE)
    llm_path: str | None = config.get("model_path")
    if llm_path is None:
        raise ValueError("An error occurred: Please provide path to your model")
    summarizer_path: str | None = config.get("summary_model_path")
    if summarizer_path is None:
        raise ValueError(
            "An error occurred: Please provide path to your summarizer model"
        )
    summarizer_model: str = summarizer_path
    context_size: str | None = config.get("context_size")
    context_size_int: int = int(context_size) if context_size is not None else 1024
    threads: str | None = config.get("context_size")
    threads_int: int = int(threads) if threads is not None else 16
    use_metal: bool | None = True if config.get("metal") == "True" else False
    llm_repo: ILlmLoaderRepository = LlmModelRepository(
        llama_model_path=llm_path,
        n_context_size=context_size_int,
        n_threads=threads_int,
        n_gpu_layers=100,
        system_prompts="You are an AI assistant, Be concise. Just respond to what user asks and do not add anything from your side on the context",
        use_metal=use_metal,
    )
    summary_repo: ILlmLoaderRepository = LlmModelRepository(
        llama_model_path=summarizer_model,
        n_context_size=100000,
        n_threads=threads_int,
        n_gpu_layers=100,
        system_prompts="You are a summarizer. Your job is to summarize conversation between the user and the chatbot in as much low words as possible keeping the context clean",
        use_metal=use_metal,
    )
    path_data: IPathContextDatasource = PathContextSqlite(datasource=SessionLocal)
    path_context_repo: IPathContextRepository = PathContextRepository(
        datasource=path_data
    )
    code_assistant = CodeAssistantUseCase(
        llm_repo=llm_repo,
        path_context_repo=path_context_repo,
        summarizer_repo=summary_repo,
    )
    chat_explorer_data: IChatExplorerDatasource = ChatExplorerSqlite(
        datasource=SessionLocal
    )
    chat_explorer_repo: IChatExplorerRepository = ChatExplorerRepository(
        datasource=chat_explorer_data
    )
    chat_explorer = GetAllChatsUseCase(
        path_context_repo=path_context_repo, chat_explorer_repo=chat_explorer_repo
    )
    await start(assistant=code_assistant, chat_explorer=chat_explorer)
    # result = await code_assistant.call(params="Hi how are you")


asyncio.run(main())
