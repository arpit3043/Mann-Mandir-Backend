from __future__ import annotations

from constants.enums import SearchType

SEARCH_TOKEN_PATTERN = r"[a-z0-9]+|[\u0900-\u097f]+"
SEARCH_TYPE_WORDS = {
    "aarti": SearchType.AARTI.value,
    "aartis": SearchType.AARTI.value,
    "arti": SearchType.AARTI.value,
    "aarties": SearchType.AARTI.value,
    "आरती": SearchType.AARTI.value,
    "chalisa": SearchType.CHALISA.value,
    "chalisas": SearchType.CHALISA.value,
    "chaleesa": SearchType.CHALISA.value,
    "चालीसा": SearchType.CHALISA.value,
    "stotram": SearchType.STOTRAM.value,
    "stotra": SearchType.STOTRAM.value,
    "stotrams": SearchType.STOTRAM.value,
    "स्तोत्र": SearchType.STOTRAM.value,
    "स्तोत्रम्": SearchType.STOTRAM.value,
    "mantra": SearchType.MANTRA.value,
    "mantras": SearchType.MANTRA.value,
    "मंत्र": SearchType.MANTRA.value,
    "मन्त्र": SearchType.MANTRA.value,
    "gita": SearchType.GITA.value,
    "geeta": SearchType.GITA.value,
    "गीता": SearchType.GITA.value,
    "veda": SearchType.VEDA.value,
    "vedas": SearchType.VEDA.value,
    "वेद": SearchType.VEDA.value,
    "upanishad": SearchType.UPANISHAD.value,
    "upanishads": SearchType.UPANISHAD.value,
    "उपनिषद": SearchType.UPANISHAD.value,
}
VALID_SEARCH_TYPES = {item.value for item in SearchType}
