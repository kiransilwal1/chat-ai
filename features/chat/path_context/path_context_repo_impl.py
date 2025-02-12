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

    async def get_summaries(self, path: str) -> str:
        # check if there is already a path in the database
        path_id = await self._datasource.has_path(path=path)

        # If yes, return the summaries
        if path_id:
            return await self._datasource.get_summaries(path_id=path_id)

        # else create path.
        created_path = await self._datasource.create_context_path(path=path)
        print(f"Create a path to the context : {created_path}")
        # If no path is in the database then create path and return empty string
        return ""

    async def limit_context(self, text: str) -> str:
        return ""

    async def create_context_path(self, path: str) -> str:
        return await self._datasource.create_context_path(path=path)

    async def has_path(self, path: str) -> str | None:
        return await self._datasource.has_path(path=path)

    async def add_context(self, path: str, full_chat: str, summary: str) -> str:
        # Get path Id from the database
        path_id = await self._datasource.has_path(path=path)
        print(f"Path : {path_id}")
        if path_id:
            return await self._datasource.add_context(
                path_id=int(path_id), full_chat=full_chat, summary=summary
            )
        raise ValueError("Path not found")
        # created_path = await self._datasource.create_context_path(path=path)
        # print(f"created_path : {created_path}")
        # return await self._datasource.add_context(
        #     path_id=int(created_path), full_chat=full_chat, summary=summary
        # )
