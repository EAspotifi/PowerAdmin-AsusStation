"""Casos de uso: información y límite de batería."""

import re

from ..cli import get_battery_info as cli_get_battery_info
from ..cli import set_battery_limit as cli_set_battery_limit


def get_battery_info() -> str:
    """Obtiene la información de batería (asusctl battery info)."""
    return cli_get_battery_info()


def set_battery_limit(percent: int) -> tuple[bool, str]:
    """Establece el límite de carga de la batería."""
    return cli_set_battery_limit(percent)


def parse_current_limit_from_info(text: str) -> int | None:
    """Extrae el límite actual (%) del texto de battery info. None si no se encuentra."""
    match = re.search(r"limit[:\s]+(\d+)\s*%?", text, re.IGNORECASE)
    if not match:
        return None
    val = int(match.group(1))
    return val if 20 <= val <= 100 else None
