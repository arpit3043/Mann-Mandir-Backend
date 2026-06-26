from abc import ABC, abstractmethod
from typing import List

from schemas.dtos import GitaChapterDto, GitaVerseDto


class GitaService(ABC):
    @abstractmethod
    async def get_gita_chapters(self) -> List[GitaChapterDto]:
        pass

    @abstractmethod
    async def get_gita_chapter(self, chapter_number: int) -> GitaChapterDto:
        pass

    @abstractmethod
    async def get_gita_verses_by_chapter(self, chapter_number: int) -> List[GitaVerseDto]:
        pass

    @abstractmethod
    async def get_gita_verse(self, chapter_number: int, verse_number: int) -> GitaVerseDto:
        pass
