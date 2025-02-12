from abc import abstractmethod, ABC
from typing import List

from features.chat.chat_explorer.chat_repositroy_interface import ChatEntity


class IChatExplorerDatasource(ABC):
    @abstractmethod
    async def get_all_chats(self, path_id: str) -> List[ChatEntity]:
        pass
