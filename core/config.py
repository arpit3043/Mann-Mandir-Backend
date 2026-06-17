from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    port: int = 8080
    api_prefix: str = "/api/v1"

    webclient_timeout_connect: float = 4.0
    webclient_timeout_read: float = 8.0
    webclient_timeout_write: float = 5.0

    api_havyaka_base_url: str = "https://havyaka-rest-api-gaonkarbhai.vercel.app/api/v1"
    api_chalisa_hanuman_base_url: str = (
        "https://raw.githubusercontent.com/anonatul/hanuman-chalisa-api/main/data"
    )
    api_gita_theaum_base_url: str = "https://vedicscriptures.github.io"
    api_gita_vedic_base_url: str = "https://vedicscriptures.github.io"
    api_shloka_base_url: str = "https://shloka.onrender.com"
    api_rigveda_base_url: str = "https://vedicscriptures.github.io"
    api_ramayana_base_url: str = "https://vedicscriptures.github.io"
    api_dharmicdata_base_url: str = (
        "https://raw.githubusercontent.com/dharmicdata/dharmic-data/main"
    )
    # Free Astrology API (server-side proxy)
    astro_api_base: str = ""
    astro_api_key: str = ""

    # ------------------------------------------------------------------
    # Redis — master / replica configuration
    # ------------------------------------------------------------------
    redis_enabled: bool = True

    redis_master_host: str = "localhost"
    redis_master_port: int = 6379

    redis_replica_hosts: str = "" 

    redis_password: str = ""
    redis_db: int = 0
    redis_socket_timeout: float = 1.0
    redis_tls: bool = False 

    redis_default_ttl: int = 2592000  # 30 days
    redis_short_ttl: int = 30         # 30 s
    redis_medium_ttl: int = 3600      # 1 h
