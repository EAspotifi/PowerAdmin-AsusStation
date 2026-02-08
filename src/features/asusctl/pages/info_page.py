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

from ..use_cases.info import get_system_info


class InfoPage(QWidget):
    """Muestra la información del dispositivo (asusctl info)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Información")
        title.setObjectName("pageTitle")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        self._info_text = QLabel()
        self._info_text.setWordWrap(True)
        self._info_text.setFont(QFont("Monospace", 10))
        self._info_text.setText("Cargando…")
        self._info_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)
        scroll.setMinimumHeight(140)
        scroll.setWidget(self._info_text)
        layout.addWidget(scroll)

        btn = QPushButton("Actualizar información")
        btn.clicked.connect(self._load)
        layout.addWidget(btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        self._info_text.setText("Cargando…")
        text = get_system_info()
        self._info_text.setText(text or "Sin datos.")
