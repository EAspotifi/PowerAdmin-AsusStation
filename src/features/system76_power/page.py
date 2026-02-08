"""Página System76-power: perfil de energía actual y selector."""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QGroupBox,
    QFrame,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .cli import (
    get_profile,
    get_profile_list,
    set_profile,
    get_graphics_mode,
    get_graphics_modes_list,
    set_graphics_mode,
)


class System76PowerPage(QWidget):
    """Muestra el perfil de energía actual y permite cambiar a Battery, Balanced o Performance."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("System76-power")
        title.setObjectName("pageTitle")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        desc = QLabel("Perfiles de energía para portátiles Pop!_OS / System76.")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: gray;")
        layout.addWidget(desc)

        self._current_label = QLabel("Perfil actual: —")
        self._current_label.setFont(QFont("", 11))
        layout.addWidget(self._current_label)

        group = QGroupBox("Seleccionar perfil")
        group.setFont(QFont("", 10))
        group_layout = QVBoxLayout(group)
        profile_btn_layout = QGridLayout()
        for i, name in enumerate(get_profile_list()):
            display = name.capitalize()
            btn = QPushButton(display)
            btn.setMinimumHeight(40)
            btn.setMinimumWidth(100)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(lambda checked, n=name: self._set_profile(n))
            row, col = divmod(i, 2)
            profile_btn_layout.addWidget(btn, row, col)
        group_layout.addLayout(profile_btn_layout)
        layout.addWidget(group)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Modo de gráficos
        graphics_label = QLabel("Modo de gráficos")
        graphics_label.setFont(QFont("", 11, QFont.Weight.Bold))
        layout.addWidget(graphics_label)
        graphics_note = QLabel("Se requiere reinicio después de cambiar el modo.")
        graphics_note.setWordWrap(True)
        graphics_note.setStyleSheet("color: gray;")
        layout.addWidget(graphics_note)
        self._graphics_current_label = QLabel("Modo actual: —")
        self._graphics_current_label.setFont(QFont("", 10))
        layout.addWidget(self._graphics_current_label)
        graphics_group = QGroupBox("Seleccionar modo")
        graphics_group.setFont(QFont("", 10))
        graphics_layout = QVBoxLayout(graphics_group)
        self._graphics_buttons_layout = QGridLayout()
        graphics_layout.addLayout(self._graphics_buttons_layout)
        layout.addWidget(graphics_group)

        btn_refresh = QPushButton("Actualizar")
        btn_refresh.clicked.connect(self._load)
        layout.addWidget(btn_refresh)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        current = get_profile()
        self._current_label.setText(f"Perfil actual: {current.capitalize() if current else '—'}")
        graphics_current = get_graphics_mode()
        self._graphics_current_label.setText(
            f"Modo actual: {graphics_current.capitalize() if graphics_current else '—'}"
        )
        self._refresh_graphics_buttons(graphics_current)

    def _refresh_graphics_buttons(self, current: str) -> None:
        """Recrea los botones de modo de gráficos y marca el actual."""
        while self._graphics_buttons_layout.count():
            item = self._graphics_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        modes = get_graphics_modes_list()
        for i, name in enumerate(modes):
            display = name.capitalize()
            btn = QPushButton(display)
            btn.setMinimumHeight(38)
            btn.setMinimumWidth(100)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            if name == current:
                btn.setStyleSheet("font-weight: bold;")
            btn.clicked.connect(lambda checked, n=name: self._set_graphics_mode(n))
            row, col = divmod(i, 2)
            self._graphics_buttons_layout.addWidget(btn, row, col)

    def _set_profile(self, profile: str) -> None:
        ok, err = set_profile(profile)
        if ok:
            QMessageBox.information(
                self,
                "Perfil de energía",
                f"Perfil establecido en «{profile.capitalize()}».",
            )
            self._load()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el perfil:\n{err}")

    def _set_graphics_mode(self, mode: str) -> None:
        ok, err = set_graphics_mode(mode)
        if ok:
            QMessageBox.information(
                self,
                "Modo de gráficos",
                f"Modo establecido en «{mode.capitalize()}».\n\nSe requiere reiniciar el equipo para aplicar el cambio.",
            )
            self._load()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el modo:\n{err}")
