"""
Scheduler pour les analyses periodiques (toutes les N minutes)
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional

from loguru import logger

from ai.sentiment import analyzer
from config import settings
from database import db
from scraper.fxstreet import scraper
from telegram_bot.poster import poster


class AnalysisScheduler:
    """Planificateur d'analyses periodiques"""

    def __init__(self) -> None:
        self.interval_minutes = settings.scraping_interval_minutes
        self.running = False
        self.last_analysis: Optional[datetime] = None
        self.cycle_count = 0

    async def run_cycle(self) -> None:
        """Execute un cycle complet: scraping -> analyse IA -> sauvegarde -> Telegram"""
        self.cycle_count += 1
        cycle_start = datetime.now()
        logger.info(f"Cycle #{self.cycle_count} - debut")

        try:
            logger.info("Scraping FXStreet...")
            # Le scraper (requests + time.sleep) est bloquant : on le lance dans un thread
            # pour ne jamais geler la boucle asyncio ni les reponses de l'API pendant ce temps.
            articles = await asyncio.to_thread(scraper.get_all_recent_articles, hours_back=6)

            if not articles:
                logger.warning("Aucun article recupere")
                await poster.post_error("scraping")
                return

            for article in articles:
                db.save_article(
                    url=article["url"],
                    title=article["title"],
                    content=article.get("content"),
                    category=article.get("category"),
                    published_at=article.get("published_at"),
                )
            logger.info(f"{len(articles)} articles recuperes")

            logger.info("Analyse IA en cours...")
            analysis = await asyncio.to_thread(analyzer.analyze, articles)

            if not analysis:
                logger.error("Echec de l'analyse")
                await poster.post_error("analysis")
                return

            db.save_analysis(analysis)

            if settings.is_telegram_configured:
                success = await poster.post_sentiment(analysis)
                logger.info("Message Telegram poste" if success else "Echec envoi Telegram")

            self.last_analysis = datetime.now()
            duration = (datetime.now() - cycle_start).total_seconds()
            logger.info(
                f"Cycle #{self.cycle_count} termine en {duration:.1f}s - "
                f"Gold: {analysis['gold']['bias']} ({analysis['gold']['confidence']}%) | "
                f"Dollar: {analysis['dollar']['bias']} ({analysis['dollar']['confidence']}%)"
            )

        except Exception as e:
            logger.error(f"Erreur cycle #{self.cycle_count}: {e}")
            await poster.post_error("scraping")

    async def start(self) -> None:
        self.running = True
        logger.info(f"Scheduler demarre - intervalle: {self.interval_minutes} min")

        if settings.is_telegram_configured:
            await poster.test_connection()

        while self.running:
            try:
                await self.run_cycle()
                next_run = datetime.now() + timedelta(minutes=self.interval_minutes)
                logger.info(f"Prochaine analyse a {next_run.strftime('%H:%M:%S')}")
                await asyncio.sleep(self.interval_minutes * 60)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Erreur scheduler: {e}")
                await asyncio.sleep(60)

    async def stop(self) -> None:
        self.running = False
        logger.info("Scheduler arrete")


scheduler = AnalysisScheduler()
