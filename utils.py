# app/utils.py
# optionnel evolutif

import subprocess
from typing import Union, List


def run_cmd(cmd: Union[str, List[str]], shell: bool = False) -> str:
    """
    Exécute une commande de façon plus sûre.
    - Préfère une liste d'arguments (shell=False).
    - Si une chaîne est fournie et shell=False, utilise shlex.split pour la parser.
    Retourne stdout (str). En cas d'erreur, retourne stdout+stderr ou le message d'exception.
    """
    try:
        if isinstance(cmd, str) and not shell:
            import shlex
            args = shlex.split(cmd)
        else:
            args = cmd
        completed = subprocess.run(
            args, shell=shell, text=True, capture_output=True, check=True
        )
        return completed.stdout
    except subprocess.CalledProcessError as e:
        # Retourne sortie disponible (stdout + stderr) pour faciliter le debug
        out = ""
        if getattr(e, "stdout", None):
            out += e.stdout
        if getattr(e, "stderr", None):
            out += e.stderr
        return out or str(e)
    except Exception as e:
        return str(e)
