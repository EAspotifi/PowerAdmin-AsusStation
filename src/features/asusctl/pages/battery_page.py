"""Página: Batería (info y límite de carga)."""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QPushButton,
    QSpinBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..use_cases.battery import (
    get_battery_info,
    set_battery_limit,
    parse_current_limit_from_info,
)


class BatteryPage(QWidget):
    """Información de batería y configuración del límite de carga."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Batería")
        title.setObjectName("pageTitle")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        self._battery_info_text = QLabel()
        self._battery_info_text.setWordWrap(True)
        self._battery_info_text.setFont(QFont("Monospace", 10))
        self._battery_info_text.setText("Cargando…")
        self._battery_info_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)
        scroll.setMinimumHeight(80)
        scroll.setWidget(self._battery_info_text)
        layout.addWidget(scroll)

        limit_row = QHBoxLayout()
        limit_row.addWidget(QLabel("Límite de carga (%):"))
        self._limit_spin = QSpinBox()
        self._limit_spin.setRange(20, 100)
        self._limit_spin.setSuffix(" %")
        self._limit_spin.setMinimumWidth(100)
        limit_row.addWidget(self._limit_spin)
        limit_row.addStretch(1)
        layout.addLayout(limit_row)

        btn = QPushButton("Establecer límite")
        btn.clicked.connect(self._apply_limit)
        layout.addWidget(btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        self._battery_info_text.setText("Cargando…")
        text = get_battery_info()
        self._battery_info_text.setText(text or "Sin datos.")
        current = parse_current_limit_from_info(text or "")
        if current is not None:
            self._limit_spin.setValue(current)

    def _apply_limit(self) -> None:
        percent = self._limit_spin.value()
        ok, err = set_battery_limit(percent)
        if ok:
            QMessageBox.information(
                self,
                "Límite de batería",
                f"Límite de carga establecido en {percent}%.",
            )
            self._load()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo establecer el límite:\n{err}")
