from abc import ABC, abstractmethod


class ChatSummarizer(ABC):
    @abstractmethod
    def summarize(self, text) -> str:
        pass
