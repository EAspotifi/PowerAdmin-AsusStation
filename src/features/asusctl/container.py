"""Contenedor Asusctl: submenú (Información, Perfiles, Batería) + contenido."""

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .pages.info_page import InfoPage
from .pages.battery_page import BatteryPage
from .pages.profiles_page import ProfilesPage


SUB_ID_INFO = "info"
SUB_ID_PROFILES = "profiles"
SUB_ID_BATTERY = "battery"


class AsusctlContainer(QWidget):
    """Al seleccionar Asusctl en la barra principal: muestra submenú y la página elegida."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Submenú lateral
        self._sub_list = QListWidget(self)
        self._sub_list.setObjectName("asusctlSubmenu")
        self._sub_list.setFixedWidth(180)
        self._sub_list.setFont(QFont("", 10))
        self._sub_list.addItem(QListWidgetItem("Información"))
        self._sub_list.item(0).setData(Qt.ItemDataRole.UserRole, SUB_ID_INFO)
        self._sub_list.addItem(QListWidgetItem("Perfiles de rendimiento"))
        self._sub_list.item(1).setData(Qt.ItemDataRole.UserRole, SUB_ID_PROFILES)
        self._sub_list.addItem(QListWidgetItem("Batería"))
        self._sub_list.item(2).setData(Qt.ItemDataRole.UserRole, SUB_ID_BATTERY)
        self._sub_list.setCurrentRow(0)
        layout.addWidget(self._sub_list)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        sep.setFixedWidth(1)
        layout.addWidget(sep)

        # Contenido de la opción seleccionada (con margen para no pegar al submenú)
        stack_container = QWidget()
        stack_layout = QVBoxLayout(stack_container)
        stack_layout.setContentsMargins(16, 12, 16, 16)
        self._stack = QStackedWidget(self)
        self._stack.addWidget(InfoPage(self))
        self._stack.addWidget(ProfilesPage(self))
        self._stack.addWidget(BatteryPage(self))
        stack_layout.addWidget(self._stack)
        layout.addWidget(stack_container, 1)

        self._sub_list.currentRowChanged.connect(self._on_sub_changed)
        self._on_sub_changed(0)

    def _on_sub_changed(self, row: int) -> None:
        if 0 <= row < self._stack.count():
            self._stack.setCurrentIndex(row)
