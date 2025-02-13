from features.chat.chat_explorer.chat_explorer_datasource_interface import (
    IChatExplorerDatasource,
)
from chatai.models import ChatData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import List
from features.chat.chat_explorer.chat_repositroy_interface import ChatEntity


class ChatExplorerSqlite(IChatExplorerDatasource):
    def __init__(self, datasource: sessionmaker[Session]):
        self._datasource = datasource

    async def get_all_chats(self, path_id: str) -> List[ChatEntity]:
        session: Session = self._datasource()
        print(f"path id inside datasource {path_id}")

        # Query the database
        db_chats = (
            session.query(ChatData).filter(ChatData.chat_path_id == int(path_id)).all()
        )
        session.close()  # Close the session after use

        # Convert database results to ChatEntity objects
        chats: List[ChatEntity] = []
        for chat in chats:
            chats.append(
                ChatEntity(id=chat.id, full_chat=chat.full_chat, summary=chat.summary)
            )

        return chats
