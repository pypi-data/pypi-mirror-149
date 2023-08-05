from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from .Dicts import BookData


class GetNewResource(metaclass=ABCMeta):
    @abstractmethod
    def __init__(
        self, base_url: str, params: Dict[str, Any], source_path: str, user_agent: str
    ) -> None:
        pass

    @abstractmethod
    def get(self, headless: bool) -> List[BookData]:
        pass

    @abstractmethod
    def _save_data(self, data: List[BookData]) -> None:
        pass

    @abstractmethod
    async def _get_pages(self, headless: bool) -> List[str]:
        pass

    @abstractmethod
    async def _get_page(self, page: Any, page_index: int) -> Tuple[Optional[str], bool]:
        pass

    @abstractmethod
    def _extract_json(self, sources: List[str]) -> List[BookData]:
        pass
