from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from chatai.models import ChatPath
from features.chat.path_context.path_context_datasource_interface import (
    IPathContextDatasource,
)


class PathContextSqlite(IPathContextDatasource):
    def __init__(self, datasource: sessionmaker[Session]):
        self._datasource = datasource

    async def summarize(self, response_string: str, model_path: str) -> str:
        return ""

    async def get_summaries(self) -> str:
        session: Session = self._datasource()
        paths = session.query(ChatPath).all()
        data = ""
        for path in paths:
            data = f" {data}: {path.id}: {path.path}"
        return data

    async def limit_context(self, text: str) -> str:
        return ""
