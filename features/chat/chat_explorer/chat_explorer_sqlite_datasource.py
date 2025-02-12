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
            session.query(ChatData).filter(ChatData.chat_path_id == path_id).all()
        )
        session.close()  # Close the session after use

        # Convert database results to ChatEntity objects
        chats: List[ChatEntity] = []
        for db_chat in db_chats:
            chats.append(
                ChatEntity(
                    id=db_chat.id, full_chat=db_chat.full_chat, summary=db_chat.summary
                )
            )

        print(f"Chats inside datasource: {chats}")
        return chats
