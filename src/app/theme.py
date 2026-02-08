"""Tema claro/oscuro para la aplicación. Solo PyQt6, sin dependencias externas."""

from enum import Enum

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt


class ThemeKind(str, Enum):
    LIGHT = "light"
    DARK = "dark"


def get_stylesheet(kind: ThemeKind) -> str:
    """Devuelve la hoja de estilos QSS para el tema dado."""
    if kind == ThemeKind.DARK:
        return _dark_stylesheet()
    return _light_stylesheet()


def _dark_stylesheet() -> str:
    return """
    QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    QMainWindow {
        background-color: #1e1e2e;
    }
    QLabel {
        color: #cdd6f4;
    }
    QPushButton {
        background-color: #45475a;
        color: #cdd6f4;
        border: 1px solid #585b70;
        border-radius: 6px;
        padding: 8px 16px;
        min-height: 20px;
    }
    QPushButton:hover {
        background-color: #585b70;
        border-color: #6c7086;
    }
    QPushButton:pressed {
        background-color: #313244;
    }
    QPushButton:disabled {
        background-color: #313244;
        color: #6c7086;
    }
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    QFrame[frameShape="4"] {
        color: #45475a;
    }
    QListWidget {
        background-color: #181825;
        color: #cdd6f4;
        border: none;
        border-radius: 8px;
        padding: 4px;
    }
    QListWidget::item {
        padding: 10px 14px;
        border-radius: 6px;
    }
    QListWidget::item:hover {
        background-color: #313244;
    }
    QListWidget::item:selected {
        background-color: #45475a;
        color: #89b4fa;
    }
    """


def _light_stylesheet() -> str:
    return """
    QWidget {
        background-color: #eff1f5;
        color: #4c4f69;
    }
    QMainWindow {
        background-color: #eff1f5;
    }
    QLabel {
        color: #4c4f69;
    }
    QPushButton {
        background-color: #e6e9ef;
        color: #4c4f69;
        border: 1px solid #ccd0da;
        border-radius: 6px;
        padding: 8px 16px;
        min-height: 20px;
    }
    QPushButton:hover {
        background-color: #dce0e8;
        border-color: #bcc0cc;
    }
    QPushButton:pressed {
        background-color: #ccd0da;
    }
    QPushButton:disabled {
        background-color: #e6e9ef;
        color: #9ca0b0;
    }
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    QFrame[frameShape="4"] {
        color: #ccd0da;
    }
    QListWidget {
        background-color: #e6e9ef;
        color: #4c4f69;
        border: 1px solid #ccd0da;
        border-radius: 8px;
        padding: 4px;
    }
    QListWidget::item {
        padding: 10px 14px;
        border-radius: 6px;
    }
    QListWidget::item:hover {
        background-color: #dce0e8;
    }
    QListWidget::item:selected {
        background-color: #bcc0cc;
        color: #1e66f5;
    }
    """


def apply_theme(app: QApplication, kind: ThemeKind) -> None:
    """Aplica el tema (QSS + paleta) a la aplicación."""
    app.setStyleSheet(get_stylesheet(kind))
    if kind == ThemeKind.DARK:
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e2e"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#cdd6f4"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#181825"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#1e1e2e"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#cdd6f4"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#45475a"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#cdd6f4"))
        app.setPalette(palette)
    else:
        app.setPalette(app.style().standardPalette())


def get_highlight_color(kind: ThemeKind) -> str:
    """Color de acento para etiquetas (ej. cambio pendiente)."""
    if kind == ThemeKind.DARK:
        return "#f9e2af"
    return "#df8e1d"
