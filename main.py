"""
Point d'entree principal - API FastAPI + Scheduler en arriere-plan
"""

import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config import settings
from database import db
from scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Demarrage du serveur Gold & Dollar Bias")
    scheduler_task = asyncio.create_task(scheduler.start())
    yield
    logger.info("Arret du serveur...")
    await scheduler.stop()
    scheduler_task.cancel()


app = FastAPI(
    title="Gold & Dollar Bias API",
    description="API de sentiment macroeconomique Or/Dollar",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "Gold & Dollar Bias",
        "version": "1.0.0",
        "endpoints": {
            "latest": "/api/latest",
            "history": "/api/history",
            "stats": "/api/stats",
            "health": "/api/health",
        },
    }


@app.get("/api/latest")
async def get_latest():
    analysis = db.get_latest()
    if not analysis:
        raise HTTPException(status_code=404, detail="Aucune analyse disponible")
    return analysis


@app.get("/api/history")
async def get_history(hours: int = 24):
    history = db.get_history(hours=hours)
    return {"count": len(history), "hours": hours, "data": history}


@app.get("/api/stats")
async def get_stats():
    stats = db.get_stats()
    stats["status"] = "running" if scheduler.running else "stopped"
    stats["last_analysis"] = (
        scheduler.last_analysis.isoformat() if scheduler.last_analysis else None
    )
    stats["cycles_completed"] = scheduler.cycle_count
    return stats


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "scheduler_running": scheduler.running,
        "last_analysis": scheduler.last_analysis.isoformat() if scheduler.last_analysis else None,
        "cycles": scheduler.cycle_count,
    }


@app.post("/api/analyze-now")
async def analyze_now():
    """Declenche un cycle d'analyse immediatement (utile pour tester sans attendre 35 min)."""
    await scheduler.run_cycle()
    latest = db.get_latest()
    if not latest:
        raise HTTPException(status_code=500, detail="Le cycle n'a produit aucune analyse")
    return latest


if __name__ == "__main__":
    print(
        f"""
============================================================
  GOLD & DOLLAR BIAS ANALYZER v1.0
============================================================
  API:        http://localhost:{settings.api_port}
  Intervalle: {settings.scraping_interval_minutes} min
  Telegram:   {'configure' if settings.is_telegram_configured else 'non configure'}
  IA:         {settings.ai_provider} ({settings.ai_model}) - {'configuree' if settings.is_ai_configured else 'NON configuree (mode fallback)'}
============================================================
"""
    )
    uvicorn.run(app, host=settings.api_host, port=settings.api_port, log_level="info")
