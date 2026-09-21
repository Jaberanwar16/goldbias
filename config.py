"""
Configuration centralisee du projet Gold & Dollar Bias
"""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration du projet, chargee depuis les variables d'environnement / .env"""

    # API Keys
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Telegram
    telegram_bot_token: str = ""
    telegram_channel_id: str = ""  # Ex: @GoldDollarBias ou -1001234567890

    # Base de donnees
    database_path: str = "data/gold_dollar_bias.db"

    # Scraping
    fxstreet_base_url: str = "https://www.fxstreet.com"
    scraping_interval_minutes: int = 35
    max_articles_per_scrape: int = 20

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # IA
    ai_provider: str = "anthropic"  # "anthropic" ou "openai"
    ai_model: str = "claude-3-5-haiku-20241022"
    max_tokens: int = 600
    temperature: float = 0.3

    class Config:
        env_file = ".env"
        extra = "ignore"

    def model_post_init(self, __context) -> None:
        self._setup_directories()

    def _setup_directories(self) -> None:
        """Cree les dossiers necessaires au demarrage"""
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        Path("logs").mkdir(exist_ok=True)

    @property
    def is_telegram_configured(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_channel_id)

    @property
    def is_ai_configured(self) -> bool:
        return bool(self.anthropic_api_key or self.openai_api_key)


settings = Settings()
