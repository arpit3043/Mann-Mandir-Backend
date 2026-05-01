from __future__ import annotations

from typing import Annotated, Any

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
from core.config import Settings
from services.contracts import GodService, ScriptureService, SearchService, VedaService
from services.god import DefaultGodService
from services.scripture import DefaultScriptureService
from services.search import DefaultSearchService
from services.static_registry import StaticContentRegistry
from services.veda import DefaultVedaService


class AppServices:
    __slots__ = ("god", "scripture", "veda", "search")

    def __init__(
        self,
        god: DefaultGodService,
        scripture: DefaultScriptureService,
        veda: DefaultVedaService,
        search: DefaultSearchService,
    ) -> None:
        self.god = god
        self.scripture = scripture
        self.veda = veda
        self.search = search


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


def get_god_service(request: Request) -> GodService:
    return request.app.state.services.god


def get_scripture_service(request: Request) -> ScriptureService:
    return request.app.state.services.scripture


def get_veda_service(request: Request) -> VedaService:
    return request.app.state.services.veda


def get_search_service(request: Request) -> SearchService:
    return request.app.state.services.search


def build_services(http_client: Any, settings: Settings) -> AppServices:
    static = StaticContentRegistry()
    hanuman = HanumanChalisaClient(http_client, settings)
    havyaka = HavyakaApiClient(http_client, settings)
    shloka = ShlokaApiClient(http_client, settings)
    gita_theaum = GitaTheAumClient(http_client, settings)
    gita_vedic = GitaVedicClient(http_client, settings)
    dharmic = DharmicDataClient(http_client, settings)
    rig = RigVedaApiClient(http_client, settings)

    god = DefaultGodService(hanuman, havyaka, shloka, static)
    scripture = DefaultScriptureService(gita_theaum, gita_vedic, dharmic, static)
    veda = DefaultVedaService(rig, havyaka, dharmic, static)
    search = DefaultSearchService(god, scripture, veda)
    return AppServices(god=god, scripture=scripture, veda=veda, search=search)


GodSvc = Annotated[GodService, Depends(get_god_service)]
ScriptureSvc = Annotated[ScriptureService, Depends(get_scripture_service)]
VedaSvc = Annotated[VedaService, Depends(get_veda_service)]
SearchSvc = Annotated[SearchService, Depends(get_search_service)]
