from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from features.chat.path_context.path_context_datasource_interface import (
    IPathContextDatasource,
)


class PathContextSqlite(IPathContextDatasource):
    def __init__(self, datasource: sessionmaker[Session]):
        self._datasource = datasource

    async def summarize(self, response_string: str, model_path: str) -> str:
        return ""

    async def get_summaries(self) -> str:
        return ""

    async def limit_context(self, text: str) -> str:
        return ""
