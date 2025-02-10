import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


async def main():
    DATABASE_URL = f"sqlite:///{os.path.expanduser('~')}/.chatai/db.sqlite"

    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    config: Dict[str, Optional[str]] = load_config(config_path="config.yaml")
    llm_path: str | None = config.get("model_path")
    if llm_path is None:
        raise ValueError("An error occurred: Invalid value")
    context_size: str | None = config.get("context_size")
    context_size_int: int = int(context_size) if context_size is not None else 1024
    threads: str | None = config.get("context_size")
    threads_int: int = int(threads) if threads is not None else 16
    llm_repo: ILlmLoaderRepository = LlmModelRepository(
        llama_model_path=llm_path, context_size=context_size_int, threads=threads_int
    )
    path_data: IPathContextDatasource = PathContextSqlite(datasource=SessionLocal)
    path_context_repo: IPathContextRepository = PathContextRepository(
        datasource=path_data
    )
    code_assistant = CodeAssistantUseCase(
        llm_repo=llm_repo, summary_repo=path_context_repo
    )
    result = await code_assistant.call(params="Hi how are you")
    print(result)


asyncio.run(main())
