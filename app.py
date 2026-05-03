# doctor/app.py
# FastAPI entrypoint — gestion du cycle de vie (lifespan) + routes

from contextlib import asynccontextmanager
from fastapi import FastAPI
from doctor.config import cfg, Config
from doctor.logger import get_logger
from doctor.runner import run_full_diagnosis

VERSION = "1.0.0"

logger = get_logger("doctor.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──────────────────────────────────────────────
    logger.info("━━━ Neron Doctor v%s — démarrage ━━━", VERSION)
    logger.info("Config chargée depuis : %s", cfg.__class__.__module__)
    logger.info("Log dir       : %s", cfg.LOG_DIR)
    logger.info("Server health : %s", cfg.SERVER_HEALTH_URL)
    logger.info("Ollama        : %s", cfg.OLLAMA_URL)
    logger.info("Services      : %s", cfg.SYSTEM_SERVICES if hasattr(cfg, 'SYSTEM_SERVICES') else cfg.SYSTEMD_SERVICES)
    logger.info("Doctor prêt ✔")

    yield  # l'app tourne ici

    # ── SHUTDOWN ─────────────────────────────────────────────
    logger.info("━━━ Neron Doctor — arrêt propre ━━━")


app = FastAPI(
    title="neronOS_DOCTOR",
    description="Neron Doctor Agent - v" + VERSION,
    version=VERSION,
    lifespan=lifespan,
)


@app.post("/diagnose")
def diagnose():
    result = run_full_diagnosis()
    return result
