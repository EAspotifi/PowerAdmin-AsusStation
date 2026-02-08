"""Casos de uso: listar y cambiar perfiles de rendimiento."""

from ..cli import (
    profile_list as cli_profile_list,
    profile_get as cli_profile_get,
    profile_set as cli_profile_set,
    profile_set_battery as cli_profile_set_battery,
)


def get_profile_list() -> list[str]:
    """Lista los perfiles disponibles (Quiet, Balanced, Performance, etc.)."""
    return cli_profile_list()


def get_profile_state() -> tuple[str, str, str, str]:
    """Obtiene el estado de perfiles. Devuelve (texto_crudo, activo, ac, batería)."""
    text = cli_profile_get()
    active, ac, battery = _parse_profile_get(text)
    return text, active, ac, battery


def _parse_profile_get(text: str) -> tuple[str, str, str]:
    """Extrae activo, AC y batería del texto de asusctl profile get."""
    active = ac = battery = ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "active" in line.lower() and "profile" in line.lower():
            parts = line.split(":", 1)
            if len(parts) == 2:
                active = parts[1].strip()
        elif line.lower().startswith("ac profile"):
            ac = line[10:].strip()
        elif "battery" in line.lower() and "profile" in line.lower():
            parts = line.split("profile", 1)
            if len(parts) == 2:
                battery = parts[1].strip()
    return active, ac, battery


def set_current_profile(profile: str) -> tuple[bool, str]:
    """Establece el perfil actual (en uso ahora)."""
    return cli_profile_set(profile)


def set_battery_profile(profile: str) -> tuple[bool, str]:
    """Establece el perfil cuando el portátil está en batería."""
    return cli_profile_set_battery(profile)
