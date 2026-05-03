# doctor/analyzer.py
# Analyse statique d'un projet Python : structure, entrypoints, problèmes détectés

import os

# Dossiers à ignorer complètement
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "venv", ".venv", "node_modules"}

# Fichiers considérés comme entrypoints
ENTRYPOINT_NAMES = {"main.py", "app.py", "server.py"}


def analyze_project(path: str) -> dict:
    result = {
        "path": path,
        "exists": False,
        "files": [],
        "entrypoints": [],
        "issues": []
    }

    if not os.path.exists(path):
        result["issues"].append(f"Path does not exist: {path}")
        return result

    result["exists"] = True

    for root, dirs, files in os.walk(path):
        # Exclure les dossiers indésirables (modifie dirs en place pour stopper la récursion)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for f in files:
            full = os.path.join(root, f)
            result["files"].append(full)

            # Détection entrypoints
            if f in ENTRYPOINT_NAMES:
                result["entrypoints"].append(full)

            # Détection fichiers de test
            if f.endswith(".py") and "test" in f.lower():
                result["issues"].append(f"Test file found: {f}")

    if result["exists"] and not result["entrypoints"]:
        result["issues"].append("No entrypoint detected")

    return result
