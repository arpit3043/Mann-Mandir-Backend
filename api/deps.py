from __future__ import annotations

from typing import Annotated, Any, Optional

from fastapi import Depends, Request

from clients.upstream import (
    DharmicDataClient,
    GitaTheAumClient,
    GitaVedicClient,
    HanumanChalisaClient,
    HavyakaApiClient,
    RigVedaApiClient,
    ShlokaApiClient,
)
from core.cache import RedisCache
from core.config import Settings
from services.contracts import SearchService, VedaService
from api.aarti_api.service import DefaultAartiService
from api.chalisa_api.service import DefaultChalisaService
from api.stotram_api.service import DefaultStotramService
from api.mantra_api.service import DefaultMantraService
from api.scriptures_api.gita_api.service import DefaultGitaService
from api.scriptures_api.ramayana_api.service import DefaultRamayanaService
from api.scriptures_api.mahabharata_api.service import DefaultMahabharataService
from api.panchang_api.service import DefaultPanchangService
from services.search import DefaultSearchService
from services.static_registry import StaticContentRegistry
from services.veda import DefaultVedaService


class AppServices:
    __slots__ = ("aarti", "chalisa", "stotram", "mantra", "gita", "ramayana", "mahabharata", "veda", "search", "panchang")

    def __init__(
        self,
        aarti: DefaultAartiService,
        chalisa: DefaultChalisaService,
        stotram: DefaultStotramService,
        mantra: DefaultMantraService,
        gita: DefaultGitaService,
        ramayana: DefaultRamayanaService,
        mahabharata: DefaultMahabharataService,
        veda: DefaultVedaService,
        search: DefaultSearchService,
        panchang: DefaultPanchangService,
    ) -> None:
        self.aarti = aarti
        self.chalisa = chalisa
        self.stotram = stotram
        self.mantra = mantra
        self.gita = gita
        self.ramayana = ramayana
        self.mahabharata = mahabharata
        self.veda = veda
        self.search = search
        self.panchang = panchang


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_veda_service(request: Request) -> VedaService:
    return request.app.state.services.veda


def get_search_service(request: Request) -> SearchService:
    return request.app.state.services.search


def build_services(
    http_client: Any,
    settings: Settings,
    cache: Optional[RedisCache] = None,
) -> AppServices:
    static = StaticContentRegistry()
    hanuman = HanumanChalisaClient(http_client, settings, cache)
    havyaka = HavyakaApiClient(http_client, settings, cache)
    shloka = ShlokaApiClient(http_client, settings, cache)
    gita_theaum = GitaTheAumClient(http_client, settings, cache)
    gita_vedic = GitaVedicClient(http_client, settings, cache)
    dharmic = DharmicDataClient(http_client, settings, cache)
    rig = RigVedaApiClient(http_client, settings, cache)

    aarti = DefaultAartiService(static)
    chalisa = DefaultChalisaService(hanuman, static)
    stotram = DefaultStotramService(static)
    mantra = DefaultMantraService(havyaka, shloka, static)

    gita = DefaultGitaService(gita_theaum, gita_vedic, static)
    ramayana = DefaultRamayanaService(static)
    mahabharata = DefaultMahabharataService(static)

    veda = DefaultVedaService(rig, havyaka, dharmic, static)
    search = DefaultSearchService(aarti, chalisa, stotram, mantra, gita, veda)
    panchang = DefaultPanchangService()
    return AppServices(
        aarti=aarti,
        chalisa=chalisa,
        stotram=stotram,
        mantra=mantra,
        gita=gita,
        ramayana=ramayana,
        mahabharata=mahabharata,
        veda=veda,
        search=search,
        panchang=panchang,
    )


VedaSvc = Annotated[VedaService, Depends(get_veda_service)]
SearchSvc = Annotated[SearchService, Depends(get_search_service)]
