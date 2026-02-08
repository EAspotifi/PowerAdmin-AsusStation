"""Página: Información del sistema (asusctl info)."""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.app.i18n import tr
from ..use_cases.info import get_system_info


class InfoPage(QWidget):
    """Muestra la información del dispositivo (asusctl info)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self._title_label = QLabel(tr("asusctl_info.title"))
        self._title_label.setObjectName("pageTitle")
        self._title_label.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(self._title_label)

        self._info_text = QLabel()
        self._info_text.setWordWrap(True)
        self._info_text.setFont(QFont("Monospace", 10))
        self._info_text.setText(tr("asusctl_info.loading"))
        self._info_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)
        scroll.setMinimumHeight(140)
        scroll.setWidget(self._info_text)
        layout.addWidget(scroll)

        self._refresh_btn = QPushButton(tr("asusctl_info.refresh"))
        self._refresh_btn.clicked.connect(self._load)
        layout.addWidget(self._refresh_btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        self._info_text.setText(tr("asusctl_info.loading"))
        text = get_system_info()
        self._info_text.setText(text or tr("asusctl_info.no_data"))

    def refresh_ui(self) -> None:
        self._title_label.setText(tr("asusctl_info.title"))
        self._refresh_btn.setText(tr("asusctl_info.refresh"))
        self._load()
