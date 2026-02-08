"""Infraestructura: ejecuta el binario supergfxctl (adaptador CLI)."""

import re
import subprocess


def get_supported_modes() -> list[str]:
    """Obtiene los modos soportados (supergfxctl -s)."""
    try:
        result = subprocess.run(
            ["supergfxctl", "-s"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return []
        output = result.stdout.strip()
        match = re.match(r"\[(.*)\]", output)
        if not match:
            return []
        modes_str = match.group(1)
        return [m.strip() for m in modes_str.split(",") if m.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def get_current_mode() -> str:
    """Obtiene el modo actual (supergfxctl -g)."""
    try:
        result = subprocess.run(
            ["supergfxctl", "-g"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_pending_mode() -> str:
    """Obtiene el modo pendiente (supergfxctl -P)."""
    try:
        result = subprocess.run(
            ["supergfxctl", "-P"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_pending_action() -> str:
    """Obtiene la acción pendiente (supergfxctl -p)."""
    try:
        result = subprocess.run(
            ["supergfxctl", "-p"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def set_mode(mode: str) -> tuple[bool, str]:
    """Establece el modo de gráficos (supergfxctl -m)."""
    try:
        result = subprocess.run(
            ["supergfxctl", "-m", mode],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True, ""
        return False, (
            result.stderr.strip() or result.stdout.strip() or "Error desconocido"
        )
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "supergfxctl no encontrado. ¿Está instalado?"
