"""
Gestion de la base de donnees SQLite pour l'historique des sentiments
"""

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from loguru import logger

from config import settings


class Database:
    """Base de donnees des analyses de sentiment"""

    def __init__(self) -> None:
        self.db_path = settings.database_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialise les tables"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sentiment_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP NOT NULL,
                    gold_bias TEXT NOT NULL,
                    gold_confidence INTEGER NOT NULL,
                    gold_summary TEXT,
                    gold_drivers TEXT,
                    dollar_bias TEXT NOT NULL,
                    dollar_confidence INTEGER NOT NULL,
                    dollar_summary TEXT,
                    dollar_drivers TEXT,
                    overall_comment TEXT,
                    articles_analyzed INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT NOT NULL,
                    content TEXT,
                    source TEXT DEFAULT 'FXStreet',
                    category TEXT,
                    published_at TIMESTAMP,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_sentiment_timestamp
                ON sentiment_analysis(timestamp DESC)
                """
            )
            conn.commit()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def save_analysis(self, analysis: Dict[str, Any]) -> int:
        """Sauvegarde une analyse de sentiment"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO sentiment_analysis
                (timestamp, gold_bias, gold_confidence, gold_summary, gold_drivers,
                 dollar_bias, dollar_confidence, dollar_summary, dollar_drivers,
                 overall_comment, articles_analyzed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    analysis["timestamp"],
                    analysis["gold"]["bias"],
                    analysis["gold"]["confidence"],
                    analysis["gold"]["summary"],
                    json.dumps(analysis["gold"].get("key_drivers", [])),
                    analysis["dollar"]["bias"],
                    analysis["dollar"]["confidence"],
                    analysis["dollar"]["summary"],
                    json.dumps(analysis["dollar"].get("key_drivers", [])),
                    analysis.get("overall_comment", ""),
                    analysis.get("articles_analyzed", 0),
                ),
            )
            conn.commit()
            return cursor.lastrowid

    def get_latest(self) -> Optional[Dict[str, Any]]:
        """Recupere la derniere analyse"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM sentiment_analysis ORDER BY timestamp DESC LIMIT 1"
            )
            row = cursor.fetchone()
            return self._row_to_dict(row) if row else None

    def get_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Recupere l'historique des analyses"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM sentiment_analysis
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                """,
                (cutoff.isoformat(),),
            )
            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "id": row["id"],
            "timestamp": row["timestamp"],
            "gold": {
                "bias": row["gold_bias"],
                "confidence": row["gold_confidence"],
                "summary": row["gold_summary"],
                "key_drivers": json.loads(row["gold_drivers"]) if row["gold_drivers"] else [],
            },
            "dollar": {
                "bias": row["dollar_bias"],
                "confidence": row["dollar_confidence"],
                "summary": row["dollar_summary"],
                "key_drivers": json.loads(row["dollar_drivers"]) if row["dollar_drivers"] else [],
            },
            "overall_comment": row["overall_comment"],
            "articles_analyzed": row["articles_analyzed"],
        }

    def save_article(
        self,
        url: str,
        title: str,
        content: Optional[str] = None,
        category: Optional[str] = None,
        published_at: Optional[str] = None,
    ) -> bool:
        """Sauvegarde un article scrape (ignore les doublons par URL)"""
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO articles
                    (url, title, content, category, published_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (url, title, content, category, published_at),
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde article: {e}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            total_analyses = conn.execute(
                "SELECT COUNT(*) FROM sentiment_analysis"
            ).fetchone()[0]
            total_articles = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
            latest = conn.execute(
                "SELECT timestamp FROM sentiment_analysis ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()

            return {
                "total_analyses": total_analyses,
                "total_articles": total_articles,
                "latest_analysis": latest[0] if latest else None,
            }


db = Database()
