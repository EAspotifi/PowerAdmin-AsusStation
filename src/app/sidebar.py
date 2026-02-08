"""Barra lateral para elegir entre Supergfxctl y Asusctl."""

from typing import Callable

from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .i18n import tr


# Identificadores de cada sección (screaming: lo que hace cada ítem)
SIDEBAR_ID_SUPERGFXCTL = "supergfxctl"
SIDEBAR_ID_ASUSCTL = "asusctl"
SIDEBAR_ID_SYSTEM76_POWER = "system76_power"


class Sidebar(QWidget):
    """Lista lateral: Supergfxctl, Asusctl, System76-power."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._list = QListWidget(self)
        self._list.setObjectName("sidebarList")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._title_label = QLabel(tr("sidebar.title"))
        self._title_label.setFont(QFont("", 12, QFont.Weight.Bold))
        layout.addWidget(self._title_label)
        layout.addWidget(self._list, 1)

        self._list.addItem(QListWidgetItem(tr("sidebar.supergfxctl")))
        self._list.item(0).setData(Qt.ItemDataRole.UserRole, SIDEBAR_ID_SUPERGFXCTL)
        self._list.addItem(QListWidgetItem(tr("sidebar.asusctl")))
        self._list.item(1).setData(Qt.ItemDataRole.UserRole, SIDEBAR_ID_ASUSCTL)
        self._list.addItem(QListWidgetItem(tr("sidebar.system76_power")))
        self._list.item(2).setData(Qt.ItemDataRole.UserRole, SIDEBAR_ID_SYSTEM76_POWER)
        self._list.setCurrentRow(0)

    def refresh_ui(self) -> None:
        """Actualiza textos al cambiar el idioma."""
        self._title_label.setText(tr("sidebar.title"))
        self._list.item(0).setText(tr("sidebar.supergfxctl"))
        self._list.item(1).setText(tr("sidebar.asusctl"))
        self._list.item(2).setText(tr("sidebar.system76_power"))

    def current_id(self) -> str:
        """Devuelve el id de la sección seleccionada."""
        item = self._list.currentItem()
        if not item:
            return SIDEBAR_ID_SUPERGFXCTL
        return item.data(Qt.ItemDataRole.UserRole) or SIDEBAR_ID_SUPERGFXCTL

    def on_section_changed(self, callback: Callable[[str], None]) -> None:
        """Registra callback(section_id: str) cuando cambia la sección."""
        self._list.currentRowChanged.connect(
            lambda: callback(self.current_id())
        )
