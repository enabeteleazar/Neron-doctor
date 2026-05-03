# doctor/app.py
# FastAPI entrypoint — lifespan + routes avec authentification

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from doctor.config import cfg
from doctor.logger import get_logger
from doctor.auth import require_api_key
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
    logger.info("Services      : %s", cfg.SYSTEMD_SERVICES)
    auth_status = "désactivée (dev)" if not cfg.API_KEY else "active"
    logger.info("Auth          : %s", auth_status)
    logger.info("Doctor prêt ✔")

    yield

    # ── SHUTDOWN ─────────────────────────────────────────────
    logger.info("━━━ Neron Doctor — arrêt propre ━━━")


app = FastAPI(
    title="neronOS_DOCTOR",
    description="Neron Doctor Agent - v" + VERSION,
    version=VERSION,
    lifespan=lifespan,
)


@app.post("/diagnose", dependencies=[Depends(require_api_key)])
def diagnose():
    result = run_full_diagnosis()
    return result
