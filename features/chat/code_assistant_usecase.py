from core.usecase import UseCase, Either, Failure
from features.chat.llm_loader.llm_loader_repository_inteface import ILlmLoaderRepository
from features.chat.path_context.path_context_repository_interface import (
    IPathContextRepository,
)


class CodeAssistantUseCase(UseCase[str, str]):
    def __init__(
        self,
        # chat_repo: IChatRepository,
        summary_repo: IPathContextRepository,
        llm_repo: ILlmLoaderRepository,
    ):
        # self._chat_repo = chat_repo
        self._summary_repo = summary_repo
        self._llm_repo = llm_repo

    async def call(self, params: str) -> Either[Failure, str]:
        # Get Past chat summary
        past_summary: str = await self._summary_repo.get_summaries()
        limit_context: str = await self._summary_repo.limit_context(text=past_summary)
        return Either.right(past_summary)
