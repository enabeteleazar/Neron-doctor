# doctor/tester.py
# Tests runtime — vérifie la disponibilité des endpoints HTTP

import time
import requests
from typing import Any, Dict
from doctor.config import cfg
from doctor.logger import get_logger

log = get_logger("doctor.tester")


def _probe(url: str) -> Dict[str, Any]:
    """Effectue une requête GET et retourne une structure riche."""
    try:
        start = time.perf_counter()
        r = requests.get(url, timeout=cfg.HTTP_TIMEOUT)
        # prefer requests' elapsed if present (covers redirects), fallback to perf_counter
        latency_ms = (r.elapsed.total_seconds() * 1000.0) if getattr(r, "elapsed", None) else (time.perf_counter() - start) * 1000.0
        status = r.status_code
        ok = 200 <= status < 300
        return {
            "code": status,
            "ok": ok,
            "latency_ms": round(latency_ms, 2),
            "error": None,
        }
    except Exception as e:
        log.warning("Probe failed for %s: %s", url, e)
        return {
            "code": None,
            "ok": False,
            "latency_ms": None,
            "error": str(e),
        }


def test_services() -> Dict[str, Dict[str, Any]]:
    """Teste les endpoints configurés et renvoie une structure détaillée.

    Retourne par exemple:
    {
      "server_health": {"code":200, "ok":True, "latency_ms":12.3, "error":None},
      "llm_health":    {"code":None, "ok":False, "latency_ms":None, "error":"ConnectionError"}
    }
    """
    results: Dict[str, Dict[str, Any]] = {}

    results["server_health"] = _probe(cfg.SERVER_HEALTH_URL)
    results["server_status"] = _probe(cfg.SERVER_STATUS_URL)
    results["llm_health"] = _probe(cfg.LLM_HEALTH_URL)

    for key, info in results.items():
        if info.get("error"):
            log.debug("%s → %s FAILED: %s", key, getattr(cfg, key.upper() + "_URL", "<unknown>"), info["error"])
        else:
            log.debug("%s → ok %s in %sms", key, info["code"], info["latency_ms"])

    return results
