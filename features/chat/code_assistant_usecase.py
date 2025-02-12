from core.usecase import UseCase, Either, Failure
from features.chat.llm_loader.llm_loader_repository_inteface import ILlmLoaderRepository
from features.chat.path_context.path_context_repository_interface import (
    IPathContextRepository,
)
import os


class CodeAssistantUseCase(UseCase[str, str]):
    def __init__(
        self,
        # chat_repo: IChatRepository,
        path_context_repo: IPathContextRepository,
        llm_repo: ILlmLoaderRepository,
        summarizer_repo: ILlmLoaderRepository,
    ):
        # self._chat_repo = chat_repo
        self._path_context_repo = path_context_repo
        self._llm_repo = llm_repo
        self._summarizer_repo = summarizer_repo

    async def call(self, params: str) -> Either[Failure, str]:
        # Get chat path
        path: str = os.getcwd()

        # Get Past chat summary. If there was no path, the repo shall create path and return "".
        # In case the context of the summary is more than what the LLM can handle then it shall be truncated while getting the summaries.
        past_summary: str = await self._path_context_repo.get_summaries(path=path)

        # Prepend past summary to text just sent by the user
        new_instruction: str = f"{past_summary} \n\n\n {params}"

        # limit_context: str = await self._path_context_repo.limit_context(
        #     text=past_summary
        # )

        # Stream Chat to console and return Chat for the system to summarize
        chat = await self._llm_repo.chat(text=new_instruction)
        print(f"Response from the LLM {chat}")
        # Summarize the response of the system
        summurize_instruction: str = (
            f"Following is the question asked by the user:  {params} and following is the response from the chatbot: {chat}. Please summarize what user asked and what the chat system responded in as low words as possible"
        )
        summary = await self._summarizer_repo.chat(text=summurize_instruction)
        print(f"The summary of what we did for me to store in the memory {summary}")
        post = await self._path_context_repo.add_context(
            path=path, full_chat=chat, summary=summary
        )
        return Either[Failure, str].right(past_summary)
