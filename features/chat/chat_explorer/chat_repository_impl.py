from typing import List, Optional
from core.usecase import Either, Failure
from features.chat.chat_explorer.chat_explorer_datasource_interface import (
    IChatExplorerDatasource,
)
from features.chat.chat_explorer.chat_repositroy_interface import (
    ChatEntity,
    IChatExplorerRepository,
)


class ChatExplorerRepository(IChatExplorerRepository):
    def __init__(self, datasource: IChatExplorerDatasource):
        self._datasource = datasource

    async def get_all_chats(self, path: str) -> Either[Failure, List[ChatEntity]]:
        try:
            print(f"Path Id for the chat inside implementation : {path}")
            result: Optional[List[ChatEntity]] = await self._datasource.get_all_chats(
                path_id=path
            )

            if not isinstance(result, list):  # Ensure result is a List[ChatEntity]
                return Either.left(Failure("Invalid data received"))

            return Either.right(result)  # Return successful result

        except Exception as e:
            return Either.left(
                Failure(f"Error retrieving chats: {str(e)}")
            )  # Handle errors
