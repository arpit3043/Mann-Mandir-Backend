from __future__ import annotations

from difflib import SequenceMatcher, get_close_matches
from typing import Any, Iterable, Mapping, Optional, Sequence

from core.exceptions import ResourceNotFoundError

ALIASES = {
    "laxmi": "lakshmi",
    "laxami": "lakshmi",
    "lakshami": "lakshmi",
    "laxmii": "lakshmi",
    "लक्ष्मी": "lakshmi",
    "mahalakshmi": "lakshmi",
    "ganesh": "ganesha",
    "ganpati": "ganesha",
    "ganapati": "ganesha",
    "गणेश": "ganesha",
    "sarasvati": "saraswati",
    "सरस्वती": "saraswati",
    "shiv": "shiva",
    "mahadev": "shiva",
    "shankar": "shiva",
    "bholenath": "shiva",
    "शिव": "shiva",
    "महादेव": "shiva",
    "ram": "rama",
    "राम": "rama",
    "krishn": "krishna",
    "krishna": "vishnukrishna",
    "vishnu": "vishnukrishna",
    "jagdish": "vishnukrishna",
    "कृष्ण": "vishnukrishna",
    "विष्णु": "vishnukrishna",
    "narayan": "vishnukrishna",
    "narayana": "vishnukrishna",
    "bajrang": "hanuman",
    "bajrangbali": "hanuman",
    "anjaneya": "hanuman",
    "हनुमान": "hanuman",
    "ambe": "durga",
    "amba": "durga",
    "gauri": "durga",
    "devi": "durga",
    "durgamata": "durga",
    "दुर्गा": "durga",
    "aditya": "surya",
    "suryadeva": "surya",
    "सूर्य": "surya",
    "shanidev": "shani",
    "shaneshwar": "shani",
    "शनि": "shani",
    "parvati": "parvati",
    "पार्वती": "parvati",
}

_PREFIXES = ("lord", "goddess", "shri", "shree", "sri")
_SUFFIXES = ("mata", "deva", "devi")


def norm(value: str) -> str:
    return " ".join((value or "").strip().lower().replace("_", "-").split())


def compact(value: str) -> str:
    return "".join(ch for ch in norm(value) if ch.isalnum())


def deity_key(value: str) -> str:
    key = compact(value)
    for prefix in _PREFIXES:
        if key.startswith(prefix) and len(key) > len(prefix) + 2:
            key = key[len(prefix) :]
    for suffix in _SUFFIXES:
        if key.endswith(suffix) and len(key) > len(suffix) + 2:
            key = key[: -len(suffix)]
    return ALIASES.get(key, key)


def expand_term(token: str) -> list[str]:
    terms = [token]
    aliased = ALIASES.get(token) or ALIASES.get(compact(token))
    mapped = deity_key(token)
    for extra in (aliased, mapped):
        if extra and extra not in terms:
            terms.append(extra)
    return terms


def closest_match(query: str, options: Sequence[str], *, cutoff: float = 0.55) -> Optional[str]:
    wanted = deity_key(query)
    raw = compact(query)
    if not options:
        return None
    by_key = {deity_key(opt): opt for opt in options if opt}
    if wanted in by_key:
        return by_key[wanted]
    if raw in by_key:
        return by_key[raw]
    for key, opt in by_key.items():
        if wanted and (wanted in key or key in wanted):
            return opt
    labels = [str(opt) for opt in options if opt]
    close = get_close_matches(norm(query), [norm(opt) for opt in labels], n=1, cutoff=cutoff)
    if close:
        hit = close[0]
        return next((opt for opt in labels if norm(opt) == hit), labels[0])
    scored = [(SequenceMatcher(None, wanted or raw, compact(opt)).ratio(), opt) for opt in labels]
    scored.sort(reverse=True)
    if scored and scored[0][0] >= cutoff:
        return scored[0][1]
    return None


def closest_row(
    query: str,
    rows: Sequence[Mapping[str, Any]],
    fields: Sequence[str] = ("id", "name", "title", "deity", "description"),
) -> Optional[Mapping[str, Any]]:
    q = compact(query)
    if not q or not rows:
        return None
    scored: list[tuple[float, Mapping[str, Any]]] = []
    for row in rows:
        score = 0.0
        for field in fields:
            value = compact(str(row.get(field) or ""))
            if not value:
                continue
            if q == value:
                score = max(score, 1.0)
            elif q in value or value in q:
                score = max(score, 0.92)
            else:
                score = max(score, SequenceMatcher(None, q, value).ratio())
        scored.append((score, row))
    scored.sort(key=lambda item: item[0], reverse=True)
    if scored and scored[0][0] >= 0.55:
        return scored[0][1]
    return None


def suggestion_for(query: str, options: Iterable[str], *, fallback: Optional[str] = None) -> str:
    values = [str(opt) for opt in options if opt]
    match = closest_match(query, values)
    if match:
        return f"Try searching: {match}"
    unique: list[str] = []
    seen: set[str] = set()
    for item in values:
        key = norm(item)
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
        if len(unique) == 5:
            break
    if unique:
        return f"Try searching: {', '.join(unique)}"
    return fallback or "Try a different spelling or browse without filters"


def suggestion_from_row(row: Optional[Mapping[str, Any]], *, fallback: str) -> str:
    if not row:
        return fallback
    deity = str(row.get("deity") or "").strip()
    ident = str(row.get("id") or row.get("name") or row.get("title") or "").strip()
    if deity and ident:
        return f"Try searching: {deity} or {ident}"
    if deity:
        return f"Try searching: {deity}"
    if ident:
        return f"Try searching: {ident}"
    return fallback


def catalog_labels(rows: Sequence[Mapping[str, Any]], *keys: str) -> list[str]:
    fields = keys or ("id", "deity", "name", "title")
    values: list[str] = []
    for row in rows:
        for key in fields:
            value = str(row.get(key) or "").strip()
            if value:
                values.append(value)
    return values


def ensure_found(
    items: Sequence[Any],
    *,
    resource: str,
    identifier: str,
    available: Iterable[str],
    fallback: Optional[str] = None,
) -> Sequence[Any]:
    if items:
        return items
    raise ResourceNotFoundError(
        resource,
        identifier,
        suggestion=suggestion_for(identifier, available, fallback=fallback),
    )
