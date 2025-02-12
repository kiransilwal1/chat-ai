from features.chat.chat_explorer.chat_repositroy_interface import (
    ChatEntity,
    IChatExplorerRepository,
)
from core.usecase import UseCase, Either, Failure
from typing import List, cast
import os

from features.chat.path_context.path_context_repository_interface import (
    IPathContextRepository,
)


class GetAllChatsUseCase(UseCase[List[ChatEntity], None]):
    """Source code dependency on path context repository."""

    def __init__(
        self,
        path_context_repo: IPathContextRepository,
        chat_explorer_repo: IChatExplorerRepository,
    ):
        self._path_context_repo = path_context_repo
        self._chat_explorer_repo = chat_explorer_repo

    async def call(self, params: None) -> Either[Failure, List[ChatEntity]]:
        # find the current path
        path: str = os.getcwd()

        # Get the path id from the database
        path_id = await self._path_context_repo.has_path(path=path)
        print(f"Path id for the chat {path_id}")
        if path_id is None:
            raise ValueError("No history for this project")
        return await self._chat_explorer_repo.get_all_chats(path=path_id)
