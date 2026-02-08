"""Caso de uso: obtener información del sistema (asusctl info)."""

from ..cli import get_info


def get_system_info() -> str:
    """Obtiene la información del dispositivo (versión, familia, placa)."""
    return get_info()
