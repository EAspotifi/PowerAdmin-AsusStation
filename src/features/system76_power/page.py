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

        # Modo de gráficos (título + botón ayuda)
        graphics_title_row = QHBoxLayout()
        graphics_title_row.setSpacing(8)
        graphics_label = QLabel("Modo de gráficos")
        graphics_label.setFont(QFont("", 11, QFont.Weight.Bold))
        graphics_title_row.addWidget(graphics_label)
        self._graphics_help_btn = QPushButton("?")
        self._graphics_help_btn.setFixedSize(24, 24)
        self._graphics_help_btn.setStyleSheet(
            "border-radius: 12px; font-weight: bold; font-size: 14px;"
        )
        self._graphics_help_btn.setToolTip("Explicación de los modos de gráficos")
        self._graphics_help_btn.clicked.connect(self._show_graphics_modes_help)
        graphics_title_row.addWidget(self._graphics_help_btn)
        graphics_title_row.addStretch(1)
        layout.addLayout(graphics_title_row)
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

    def _show_graphics_modes_help(self) -> None:
        """Muestra ventana emergente con la explicación de cada modo de gráficos."""
        text = """<h3>Modos de gráficos</h3>
<p><b>Integrated</b><br/>
Solo la GPU integrada. Menor consumo y mayor duración de batería. La GPU discreta (NVIDIA) no se usa.</p>

<p><b>Hybrid (PRIME)</b><br/>
Usa ambas GPUs. La integrada para la pantalla por defecto; la NVIDIA cuando una aplicación la solicita. Buen equilibrio entre rendimiento y batería.</p>

<p><b>NVIDIA</b><br/>
La GPU discreta NVIDIA como principal. Mejor rendimiento gráfico y para juegos; mayor consumo.</p>

<p><b>Compute</b><br/>
Similar a Integrated en pantalla (todo se dibuja con la integrada), pero la NVIDIA queda disponible para cálculo (CUDA, ML, etc.) sin usarla para mostrar la interfaz.</p>

<p><i>Tras cambiar el modo es necesario reiniciar el equipo.</i></p>"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Ayuda: modos de gráficos")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
