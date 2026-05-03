# doctor/runner.py
# Orchestrateur principal — coordonne analyse, tests, fixes

from doctor.analyzer import analyze_project
from doctor.tester import test_services
from doctor.fixer import apply_fixes
from doctor.config import cfg


def run_full_diagnosis() -> dict:
    report = {
        "analysis": {},
        "tests": {},
        "fixes": [],
        "final_status": {}
    }

    # PHASE 1 - ANALYSE STATIQUE
    report["analysis"]["core"] = analyze_project(cfg.CORE_PATH)
    report["analysis"]["llm"]  = analyze_project(cfg.LLM_PATH)

    # PHASE 2 - TESTS RUNTIME
    report["tests"] = test_services()

    # PHASE 3 - AUTOCORRECTION
    report["fixes"] = apply_fixes(report)

    # PHASE 4 - RE-TEST POST FIX
    report["final_status"] = test_services()

    return report
