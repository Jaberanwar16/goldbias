"""
Templates de messages Telegram
"""

from datetime import datetime
from typing import Any, Dict

_EMOJI = {"Bullish": "\U0001F7E2", "Bearish": "\U0001F534", "Neutral": "\u26AA"}


class MessageTemplates:
    """Templates pour les messages Telegram"""

    @staticmethod
    def sentiment_message(analysis: Dict[str, Any]) -> str:
        gold = analysis["gold"]
        dollar = analysis["dollar"]

        gold_drivers = "\n".join(f"\u25AB\uFE0F {d}" for d in gold.get("key_drivers", [])[:3])
        dollar_drivers = "\n".join(f"\u25AB\uFE0F {d}" for d in dollar.get("key_drivers", [])[:3])

        try:
            update_time = datetime.fromisoformat(analysis["timestamp"]).strftime("%H:%M UTC")
        except Exception:
            update_time = datetime.utcnow().strftime("%H:%M UTC")

        return f"""\U0001F947 GOLD & DOLLAR BIAS \U0001F3E6
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
Mise a jour {update_time}

\U0001F7E1 GOLD BIAS
{_EMOJI.get(gold['bias'], '\u26AA')} {gold['bias'].upper()}
Confiance: {gold['confidence']}%
{gold['summary']}

{gold_drivers}

\U0001F4B5 DOLLAR BIAS
{_EMOJI.get(dollar['bias'], '\u26AA')} {dollar['bias'].upper()}
Confiance: {dollar['confidence']}%
{dollar['summary']}

{dollar_drivers}

\U0001F4CA MACRO VIEW
{analysis.get('overall_comment', '')}

\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
Prochaine analyse dans 35 minutes
#Gold #Dollar #XAUUSD #DXY #Macro
"""

    @staticmethod
    def quick_update(analysis: Dict[str, Any]) -> str:
        gold = analysis["gold"]
        dollar = analysis["dollar"]

        return f"""\U0001F504 Update 35min

{_EMOJI.get(gold['bias'], '\u26AA')} GOLD: {gold['bias']} ({gold['confidence']}%)
{_EMOJI.get(dollar['bias'], '\u26AA')} DOLLAR: {dollar['bias']} ({dollar['confidence']}%)

{analysis.get('overall_comment', '')[:100]}
"""

    @staticmethod
    def error_message(error_type: str) -> str:
        messages = {
            "scraping": "\u26A0\uFE0F Erreur de recuperation des donnees. Nouvel essai dans 35 min.",
            "analysis": "\u26A0\uFE0F Erreur d'analyse. Nouvel essai dans 35 min.",
            "telegram": "\u26A0\uFE0F Erreur d'envoi. Nouvel essai automatique.",
        }
        return messages.get(error_type, "\u26A0\uFE0F Erreur technique. Nouvel essai dans 35 min.")
