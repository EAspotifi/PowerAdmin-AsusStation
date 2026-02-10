"""Infraestructura: ejecuta el binario system76-power (adaptador CLI)."""

import subprocess

PROFILES = ("battery", "balanced", "performance")
GRAPHICS_MODES = ("compute", "hybrid", "integrated", "nvidia")


def get_profile() -> str:
    """Obtiene el perfil de energía actual (system76-power profile).

    Returns:
        Nombre del perfil en minúsculas o cadena vacía si falla.
    """
    try:
        result = subprocess.run(
            ["system76-power", "profile"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip().lower()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_profile_list() -> list[str]:
    """Lista los perfiles disponibles (battery, balanced, performance)."""
    return list(PROFILES)


def set_profile(profile: str) -> tuple[bool, str]:
    """Establece el perfil de energía (system76-power profile <nombre>)."""
    name = profile.strip().lower()
    if name not in PROFILES:
        return False, f"Perfil no válido. Usa: {', '.join(PROFILES)}"
    try:
        result = subprocess.run(
            ["system76-power", "profile", name],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr.strip() or result.stdout.strip() or "Error al cambiar perfil"
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "No disponible"


def get_graphics_mode() -> str:
    """Obtiene el modo de gráficos actual (system76-power graphics).

    Returns:
        Nombre del modo en minúsculas o cadena vacía si falla.
    """
    try:
        result = subprocess.run(
            ["system76-power", "graphics"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip().lower()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_graphics_modes_list() -> list[str]:
    """Lista los modos de gráficos seleccionables: compute, hybrid, integrated, nvidia."""
    return list(GRAPHICS_MODES)


def set_graphics_mode(mode: str) -> tuple[bool, str]:
    """Establece el modo de gráficos (system76-power graphics <modo>). Requiere reinicio."""
    name = mode.strip().lower()
    if name not in GRAPHICS_MODES:
        return False, f"Modo no válido. Usa: {', '.join(GRAPHICS_MODES)}"
    try:
        result = subprocess.run(
            ["system76-power", "graphics", name],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            return True, ""
        return False, result.stderr.strip() or result.stdout.strip() or "Error al cambiar modo"
    except subprocess.TimeoutExpired:
        return False, "Tiempo de espera agotado"
    except FileNotFoundError:
        return False, "No disponible"
