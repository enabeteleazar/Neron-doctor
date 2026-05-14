# app/logger.py
# Logger centralisé avec rotation de fichiers et sortie console colorée

import logging
import os
from logging.handlers import RotatingFileHandler
from doctor.config import cfg

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # déjà configuré

    logger.setLevel(logging.DEBUG)

    # --- Console handler ---
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(console)

    # --- Fichier handler avec rotation ---
    try:
        os.makedirs(cfg.LOG_DIR, exist_ok=True)
        log_file = os.path.join(cfg.LOG_DIR, "doctor.log")
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(file_handler)
    except Exception as e:
        # Si on ne peut pas créer le dossier de logs (permissions, FS en lecture seule, etc.),
        # on continue avec le handler console uniquement.
        logger.warning("Cannot use file handler for logs (%s): %s", cfg.LOG_DIR, e)

    return logger
