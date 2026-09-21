"""
Poste les messages de sentiment sur le canal Telegram
"""

from typing import Any, Dict, Optional

from loguru import logger
from telegram import Bot
from telegram.error import TelegramError

from config import settings
from telegram_bot.templates import MessageTemplates


class TelegramPoster:
    """Poste les messages sur le canal Telegram"""

    def __init__(self) -> None:
        self.channel_id = settings.telegram_channel_id
        self.bot: Optional[Bot] = None

        if settings.is_telegram_configured:
            self.bot = Bot(token=settings.telegram_bot_token)
            logger.info(f"Bot Telegram initialise pour {self.channel_id}")

    async def post_sentiment(self, analysis: Dict[str, Any]) -> bool:
        if not self.bot:
            logger.warning("Bot Telegram non configure")
            return False

        try:
            message = MessageTemplates.sentiment_message(analysis)
            await self.bot.send_message(
                chat_id=self.channel_id, text=message, disable_web_page_preview=True
            )
            logger.info("Message de sentiment poste avec succes")
            return True
        except TelegramError as e:
            logger.error(f"Erreur Telegram (message complet): {e}")
            try:
                short_message = MessageTemplates.quick_update(analysis)
                await self.bot.send_message(
                    chat_id=self.channel_id, text=short_message, disable_web_page_preview=True
                )
                logger.info("Message court poste (fallback)")
                return True
            except Exception as e2:
                logger.error(f"Erreur fallback Telegram: {e2}")
                return False

    async def post_error(self, error_type: str) -> bool:
        if not self.bot:
            return False
        try:
            await self.bot.send_message(
                chat_id=self.channel_id, text=MessageTemplates.error_message(error_type)
            )
            return True
        except Exception as e:
            logger.error(f"Erreur envoi message d'erreur: {e}")
            return False

    async def test_connection(self) -> bool:
        if not self.bot:
            return False
        try:
            await self.bot.send_message(
                chat_id=self.channel_id,
                text="\U0001F916 Bot connecte et operationnel !\nProchaine analyse dans 35 minutes.",
            )
            logger.info("Test connexion Telegram reussi")
            return True
        except Exception as e:
            logger.error(f"Test connexion echoue: {e}")
            return False


poster = TelegramPoster()
