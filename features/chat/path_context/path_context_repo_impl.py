from features.chat.path_context.path_context_datasource_interface import (
    IPathContextDatasource,
)
from features.chat.path_context.path_context_repository_interface import (
    IPathContextRepository,
)


class PathContextRepository(IPathContextRepository):
    def __init__(self, datasource: IPathContextDatasource):
        self._datasource = datasource

    async def summarize(self, response_string: str, model_path: str) -> str:
        return "This is a summary"

    async def get_summaries(self) -> str:
        return "I got a summary for you"

    async def limit_context(self, text: str) -> str:
        return ""
