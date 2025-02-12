from abc import ABC, abstractmethod
from typing import List

from core.usecase import Either, Failure


class ChatEntity:
    def __init__(self, id: int, full_chat: str, summary: str):
        self.id = id
        self.full_chat = full_chat
        self.summary = summary


class IChatExplorerRepository(ABC):
    @abstractmethod
    async def get_all_chats(self, path: str) -> Either[Failure, List[ChatEntity]]: ...
