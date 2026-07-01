from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações centralizadas do Évora LeadFlow."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="Évora LeadFlow", alias="APP_NAME")
    app_env: str = Field(default="local", alias="APP_ENV")
    timezone: str = Field(default="America/Sao_Paulo", alias="TIMEZONE")
    enable_scheduler: bool = Field(default=True, alias="ENABLE_SCHEDULER")
    daily_reminder_hour: int = Field(default=8, alias="DAILY_REMINDER_HOUR")

    database_url: str = Field(
        default="postgresql+psycopg2://leadflow:leadflow@postgres:5432/leadflow",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    dashboard_username: str = Field(default="evora", alias="DASHBOARD_USERNAME")
    dashboard_password: str = Field(default="troque_esta_senha", alias="DASHBOARD_PASSWORD")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5.5", alias="OPENAI_MODEL")

    whatsapp_verify_token: str = Field(
        default="evora_leadflow_verify_token_change_me", alias="WHATSAPP_VERIFY_TOKEN"
    )
    whatsapp_access_token: str | None = Field(default=None, alias="WHATSAPP_ACCESS_TOKEN")
    whatsapp_phone_number_id: str | None = Field(default=None, alias="WHATSAPP_PHONE_NUMBER_ID")
    whatsapp_app_secret: str | None = Field(default=None, alias="WHATSAPP_APP_SECRET")
    whatsapp_graph_version: str = Field(default="v23.0", alias="WHATSAPP_GRAPH_VERSION")

    default_manager_phone: str | None = Field(default=None, alias="DEFAULT_MANAGER_PHONE")
    cron_secret: str | None = Field(default=None, alias="CRON_SECRET")


@lru_cache
def get_settings() -> Settings:
    return Settings()
