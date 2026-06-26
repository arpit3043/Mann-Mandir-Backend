from __future__ import annotations

import json
import logging
from itertools import cycle
from typing import Any, List, Optional

import redis

logger = logging.getLogger(__name__)


class RedisCache:

    def __init__(
        self,
        master: redis.StrictRedis,
        replicas: Optional[List[redis.StrictRedis]] = None,
    ) -> None:
        self._master = master
        self._replicas: List[redis.StrictRedis] = replicas or []
        # Round-robin iterator over replicas; falls back to master when empty.
        self._replica_cycle = cycle(self._replicas) if self._replicas else None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str) -> Optional[Any]:
        """Return the cached Python object for *key*, or None on miss/error."""
        client = self._next_read_client()
        try:
            raw = client.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except redis.RedisError as exc:
            logger.warning("Redis GET error for key=%r: %s", key, exc)
            # Will try master as last resort if a replica failed
            if client is not self._master:
                try:
                    raw = self._master.get(key)
                    return json.loads(raw) if raw is not None else None
                except redis.RedisError:
                    pass
            return None

    def set(self, key: str, value: Any, ttl: int) -> bool:
        """Serialize *value* to JSON and store it on the master with TTL seconds."""
        try:
            payload = json.dumps(value, ensure_ascii=False)
            self._master.setex(key, ttl, payload)
            return True
        except redis.RedisError as exc:
            logger.warning("Redis SET error for key=%r: %s", key, exc)
            return False

    @staticmethod
    def make_key(url: str) -> str:
        """Deterministic cache key derived from a URL."""
        return f"mm:{url}"

    def ping_master(self) -> bool:
        """Return True if the master is reachable."""
        try:
            return self._master.ping()
        except redis.RedisError:
            return False

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _next_read_client(self) -> redis.StrictRedis:
        """Return the next replica for reads, or master if none configured."""
        if self._replica_cycle is not None:
            return next(self._replica_cycle)
        return self._master


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def build_redis_cache(
    master_host: str,
    master_port: int,
    replica_specs: List[tuple[str, int]],
    password: str,
    db: int,
    socket_timeout: float,
    tls: bool = False,
) -> RedisCache:
    common: dict[str, Any] = {
        "db": db,
        "socket_timeout": socket_timeout,
        "socket_connect_timeout": socket_timeout,
        "decode_responses": False,
    }
    if password:
        common["password"] = password
    if tls:
        common["ssl"] = True
        common["ssl_cert_reqs"] = None 

    master = redis.StrictRedis(host=master_host, port=master_port, **common)

    replicas: List[redis.StrictRedis] = [
        redis.StrictRedis(host=h, port=p, **common) for h, p in replica_specs
    ]

    return RedisCache(master=master, replicas=replicas)
