from __future__ import annotations

JAVA_MAX_INT = 2147483647
DEFAULT_PAGE_SIZE = 20
PATH_RESOURCES = (
    ("/god/aartis", "Aarti"),
    ("/god/chalisas", "Chalisa"),
    ("/god/stotram", "Stotram"),
    ("/god/mantras", "Mantra"),
    ("/vedas/mantras", "Mantra"),
    ("/vedas/upanishads", "Upanishad"),
    ("/vedas/rig", "Rig Veda"),
    ("/vedas", "Veda"),
    ("/scriptures/gita", "Gita"),
    ("/scriptures/ramayana", "Ramayana"),
    ("/scriptures/mahabharata", "Mahabharata"),
    ("/search", "Search"),
    ("/panchang", "Panchang"),
    ("/astro", "Astro"),
)
IDENTIFIER_QUERY_KEYS = ("deity", "query", "q", "poet", "sign", "name")
DEFAULT_RESOURCE_NAME = "Result"
UNKNOWN_IDENTIFIER = "requested data"
