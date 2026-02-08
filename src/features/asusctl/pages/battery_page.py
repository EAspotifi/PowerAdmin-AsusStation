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

from src.app.i18n import tr
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

        self._title_label = QLabel(tr("asusctl_battery.title"))
        self._title_label.setObjectName("pageTitle")
        self._title_label.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(self._title_label)

        self._battery_info_text = QLabel()
        self._battery_info_text.setWordWrap(True)
        self._battery_info_text.setFont(QFont("Monospace", 10))
        self._battery_info_text.setText(tr("asusctl_battery.loading"))
        self._battery_info_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)
        scroll.setMinimumHeight(80)
        scroll.setWidget(self._battery_info_text)
        layout.addWidget(scroll)

        limit_row = QHBoxLayout()
        limit_row.addWidget(QLabel(tr("asusctl_battery.limit_label")))
        self._limit_spin = QSpinBox()
        self._limit_spin.setRange(20, 100)
        self._limit_spin.setSuffix(" %")
        self._limit_spin.setMinimumWidth(100)
        limit_row.addWidget(self._limit_spin)
        limit_row.addStretch(1)
        layout.addLayout(limit_row)

        self._set_limit_btn = QPushButton(tr("asusctl_battery.set_limit"))
        self._set_limit_btn.clicked.connect(self._apply_limit)
        layout.addWidget(self._set_limit_btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        self._battery_info_text.setText(tr("asusctl_battery.loading"))
        text = get_battery_info()
        self._battery_info_text.setText(text or tr("asusctl_battery.no_data"))
        current = parse_current_limit_from_info(text or "")
        if current is not None:
            self._limit_spin.setValue(current)

    def _apply_limit(self) -> None:
        percent = self._limit_spin.value()
        ok, err = set_battery_limit(percent)
        if ok:
            QMessageBox.information(
                self,
                tr("dialogs.battery_limit"),
                tr("dialogs.battery_limit_message", percent=str(percent)),
            )
            self._load()
        else:
            QMessageBox.critical(self, tr("dialogs.error"), tr("dialogs.battery_limit_error", err=err))

    def refresh_ui(self) -> None:
        self._title_label.setText(tr("asusctl_battery.title"))
        self._set_limit_btn.setText(tr("asusctl_battery.set_limit"))
        self._load()
