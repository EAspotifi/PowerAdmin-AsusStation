"""Módulo para interactuar con supergfxctl."""

import re
import subprocess


def get_supported_modes() -> list[str]:
    """Obtiene los modos de gráficos soportados por supergfxctl.

    Ejecuta `supergfxctl -s` y parsea la salida [Modo1, Modo2, ...].

    Returns:
        Lista de nombres de modos disponibles.
    """
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
        # Parsear formato: [Integrated, Hybrid, NvidiaNoModeset]
        match = re.match(r"\[(.*)\]", output)
        if not match:
            return []

        modes_str = match.group(1)
        modes = [m.strip() for m in modes_str.split(",") if m.strip()]
        return modes
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def get_current_mode() -> str:
    """Obtiene el modo de gráficos actual.

    Returns:
        Nombre del modo actual, o cadena vacía si falla.
    """
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
    """Obtiene el modo pendiente (cambio solicitado aún no aplicado).

    Returns:
        Nombre del modo pendiente, o cadena vacía si no hay cambio pendiente.
    """
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
    """Obtiene la acción pendiente del usuario (ej: logout, reboot).

    Returns:
        Descripción de la acción pendiente, o cadena vacía si no hay.
    """
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
    """Cambia el modo de gráficos.

    Args:
        mode: Nombre del modo (ej: Integrated, Hybrid, Vfio).

    Returns:
        Tupla (éxito, mensaje de error o vacío).
    """
    try:
        result = subprocess.run(
            ["supergfxctl", "-m", mode],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr.strip() or result.stdout.strip() or "Error desconocido"
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "supergfxctl no encontrado. ¿Está instalado?"
