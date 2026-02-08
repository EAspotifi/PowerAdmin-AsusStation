"""Internacionalización: carga de idiomas desde JSON y traducción por claves."""

import json
from pathlib import Path
from typing import Any, Callable

# Idiomas soportados
SUPPORTED = ("es", "en")
DEFAULT = "es"

# Caché: lang -> dict
_translations: dict[str, dict[str, Any]] = {}
_current = DEFAULT
_listeners: list[Callable[[], None]] = []


def _languages_dir() -> Path:
    """Ruta a la carpeta languages/ (raíz del proyecto)."""
    # src/app/i18n.py -> proyecto/languages
    return Path(__file__).resolve().parent.parent.parent / "languages"


def _load(lang: str) -> dict[str, Any]:
    """Carga el JSON del idioma. Fallback a es si falla."""
    if lang in _translations:
        return _translations[lang]
    path = _languages_dir() / f"{lang}.json"
    try:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                _translations[lang] = json.load(f)
                return _translations[lang]
    except (json.JSONDecodeError, OSError):
        pass
    if lang != DEFAULT:
        return _load(DEFAULT)
    _translations[DEFAULT] = {}
    return _translations[DEFAULT]


def _get_value(data: dict, key: str) -> str | None:
    """Obtiene un valor por clave con notación de punto (ej. app.title)."""
    keys = key.split(".")
    for k in keys:
        if isinstance(data, dict) and k in data:
            data = data[k]
        else:
            return None
    return str(data) if data is not None else None


def tr(key: str, **kwargs: str) -> str:
    """Devuelve la cadena traducida para la clave. Sustituye {name} por kwargs."""
    data = _load(_current)
    out = _get_value(data, key)
    if out is None:
        return key
    for k, v in kwargs.items():
        out = out.replace("{" + k + "}", str(v))
    return out


def get_language() -> str:
    """Idioma actual (es, en)."""
    return _current


def set_language(lang: str) -> None:
    """Cambia el idioma y notifica a los listeners."""
    global _current
    lang = lang.lower().strip()
    if lang not in SUPPORTED:
        lang = DEFAULT
    if lang == _current:
        return
    _current = lang
    _load(_current)
    for cb in _listeners:
        try:
            cb()
        except Exception:
            pass


def on_language_changed(callback: Callable[[], None]) -> None:
    """Registra un callback que se llama cuando cambia el idioma."""
    _listeners.append(callback)


def language_display_name(code: str) -> str:
    """Nombre visible del idioma (ej. es -> Español)."""
    data = _load(code)
    names = data.get("language_names") or {}
    return names.get(code, code)
