"""Infraestructura: ejecuta el binario asusctl (adaptador CLI)."""

import subprocess


def get_info() -> str:
    """Obtiene la salida de `asusctl info` (versión, familia, placa, etc.).

    Returns:
        Texto completo de la salida, o mensaje de error si falla.
    """
    try:
        result = subprocess.run(
            ["asusctl", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return result.stderr.strip() or result.stdout.strip() or "Error al ejecutar asusctl info"
    except subprocess.TimeoutExpired:
        return "Tiempo de espera agotado"
    except FileNotFoundError:
        return "asusctl no encontrado. ¿Está instalado?"


def get_battery_info() -> str:
    """Obtiene la salida de `asusctl battery info`.

    Returns:
        Texto completo de la salida, o mensaje de error si falla.
    """
    try:
        result = subprocess.run(
            ["asusctl", "battery", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return result.stderr.strip() or result.stdout.strip() or "Error al ejecutar asusctl battery info"
    except subprocess.TimeoutExpired:
        return "Tiempo de espera agotado"
    except FileNotFoundError:
        return "asusctl no encontrado. ¿Está instalado?"


def set_battery_limit(percent: int) -> tuple[bool, str]:
    """Establece el límite de carga de la batería (asusctl battery limit <porcentaje>).

    Args:
        percent: Porcentaje entre 20 y 100 (típico para prolongar vida útil).

    Returns:
        (éxito, mensaje de error o vacío)
    """
    if not 20 <= percent <= 100:
        return False, "El porcentaje debe estar entre 20 y 100."
    try:
        result = subprocess.run(
            ["asusctl", "battery", "limit", str(percent)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr.strip() or result.stdout.strip() or "Error al establecer límite"
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "asusctl no encontrado. ¿Está instalado?"


def profile_list() -> list[str]:
    """Lista los perfiles disponibles (asusctl profile list)."""
    try:
        result = subprocess.run(
            ["asusctl", "profile", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return []
        lines = [ln.strip() for ln in result.stdout.strip().splitlines() if ln.strip()]
        return lines
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def profile_get() -> str:
    """Obtiene el estado actual de perfiles (asusctl profile get)."""
    try:
        result = subprocess.run(
            ["asusctl", "profile", "get"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return result.stderr.strip() or result.stdout.strip() or "Error al obtener perfiles"
    except subprocess.TimeoutExpired:
        return "Tiempo de espera agotado"
    except FileNotFoundError:
        return "asusctl no encontrado. ¿Está instalado?"


def profile_set(profile: str) -> tuple[bool, str]:
    """Establece el perfil actual (asusctl profile set <nombre>)."""
    if not profile.strip():
        return False, "Selecciona un perfil."
    try:
        result = subprocess.run(
            ["asusctl", "profile", "set", profile.strip()],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr.strip() or result.stdout.strip() or "Error al cambiar perfil"
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "asusctl no encontrado. ¿Está instalado?"


def profile_set_battery(profile: str) -> tuple[bool, str]:
    """Establece el perfil cuando está en batería (asusctl profile set <nombre> --battery)."""
    if not profile.strip():
        return False, "Selecciona un perfil."
    try:
        result = subprocess.run(
            ["asusctl", "profile", "set", profile.strip(), "--battery"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr.strip() or result.stdout.strip() or "Error al establecer perfil en batería"
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "asusctl no encontrado. ¿Está instalado?"
