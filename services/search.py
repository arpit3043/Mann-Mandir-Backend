from typing import List

from api.aarti_api.service_contract import AartiService
from api.chalisa_api.service_contract import ChalisaService
from api.mantra_api.service_contract import MantraService
from api.scriptures_api.gita_api.service_contract import GitaService
from api.stotram_api.service_contract import StotramService
from schemas.dtos import SearchResultDto
from services.contracts import SearchService, VedaService


class DefaultSearchService(SearchService):
    def __init__(
        self,
        aarti: AartiService,
        chalisa: ChalisaService,
        stotram: StotramService,
        mantra: MantraService,
        gita: GitaService,
        veda: VedaService,
    ) -> None:
        self.aarti = aarti
        self.chalisa = chalisa
        self.stotram = stotram
        self.mantra = mantra
        self.gita = gita
        self.veda = veda

    async def search(self, query: str, limit: int = 10) -> List[SearchResultDto]:
        results = []
        q = query.lower()

        try:
            aartis = await self.aarti.get_aartis(None, 0, 1000)
            for a in aartis:
                if q in a.name.lower() or (a.deity and q in a.deity.lower()):
                    results.append(
                        SearchResultDto(
                            id=a.id, type="aarti", source="local", title=a.name, snippet=a.translation or ""
                        )
                    )
        except Exception:
            pass

        try:
            chalisas = await self.chalisa.get_chalisas(None, 0, 1000)
            for c in chalisas:
                if q in c.title.lower() or (c.deity and q in c.deity.lower()):
                    results.append(SearchResultDto(id=c.id, type="chalisa", source="local", title=c.title))
        except Exception:
            pass

        try:
            stotrams = await self.stotram.get_stotrams(None, 0, 1000)
            for s in stotrams:
                if q in s.name.lower() or (s.deity and q in s.deity.lower()):
                    results.append(SearchResultDto(id=s.id, type="stotram", source="local", title=s.name))
        except Exception:
            pass

        return results[:limit]
