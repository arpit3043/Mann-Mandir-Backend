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
    webclient_retry_max_attempts: int = 3
    webclient_retry_backoff_ms: float = 500.0

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
