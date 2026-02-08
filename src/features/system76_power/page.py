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

from src.app.i18n import tr
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

        self._title_label = QLabel(tr("system76_power.title"))
        self._title_label.setObjectName("pageTitle")
        self._title_label.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(self._title_label)

        self._desc_label = QLabel(tr("system76_power.desc"))
        self._desc_label.setWordWrap(True)
        self._desc_label.setStyleSheet("color: gray;")
        layout.addWidget(self._desc_label)

        self._current_label = QLabel(tr("system76_power.current_profile"))
        self._current_label.setFont(QFont("", 11))
        layout.addWidget(self._current_label)

        self._profile_group = QGroupBox(tr("system76_power.select_profile"))
        self._profile_group.setFont(QFont("", 10))
        group_layout = QVBoxLayout(self._profile_group)
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
        layout.addWidget(self._profile_group)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Modo de gráficos (título + botón ayuda)
        graphics_title_row = QHBoxLayout()
        graphics_title_row.setSpacing(8)
        self._graphics_title_label = QLabel(tr("system76_power.graphics_title"))
        self._graphics_title_label.setFont(QFont("", 11, QFont.Weight.Bold))
        graphics_title_row.addWidget(self._graphics_title_label)
        self._graphics_help_btn = QPushButton("?")
        self._graphics_help_btn.setFixedSize(24, 24)
        self._graphics_help_btn.setStyleSheet(
            "border-radius: 12px; font-weight: bold; font-size: 14px;"
        )
        self._graphics_help_btn.setToolTip(tr("system76_power.graphics_help_tooltip"))
        self._graphics_help_btn.clicked.connect(self._show_graphics_modes_help)
        graphics_title_row.addWidget(self._graphics_help_btn)
        graphics_title_row.addStretch(1)
        layout.addLayout(graphics_title_row)
        self._graphics_note_label = QLabel(tr("system76_power.graphics_note"))
        self._graphics_note_label.setWordWrap(True)
        self._graphics_note_label.setStyleSheet("color: gray;")
        layout.addWidget(self._graphics_note_label)
        self._graphics_current_label = QLabel(tr("system76_power.graphics_current"))
        self._graphics_current_label.setFont(QFont("", 10))
        layout.addWidget(self._graphics_current_label)
        self._graphics_group = QGroupBox(tr("system76_power.select_graphics"))
        self._graphics_group.setFont(QFont("", 10))
        graphics_layout = QVBoxLayout(self._graphics_group)
        self._graphics_buttons_layout = QGridLayout()
        graphics_layout.addLayout(self._graphics_buttons_layout)
        layout.addWidget(self._graphics_group)

        self._refresh_btn = QPushButton(tr("system76_power.refresh"))
        self._refresh_btn.clicked.connect(self._load)
        layout.addWidget(self._refresh_btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        current = get_profile()
        base = tr("system76_power.current_profile").replace("--", current.capitalize() if current else "—")
        self._current_label.setText(base)
        graphics_current = get_graphics_mode()
        gbase = tr("system76_power.graphics_current").replace("--", graphics_current.capitalize() if graphics_current else "—")
        self._graphics_current_label.setText(gbase)
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
                tr("dialogs.system76_profile_set"),
                tr("dialogs.system76_profile_message", profile=profile.capitalize()),
            )
            self._load()
        else:
            QMessageBox.critical(self, tr("dialogs.error"), tr("dialogs.system76_profile_error", err=err))

    def _set_graphics_mode(self, mode: str) -> None:
        ok, err = set_graphics_mode(mode)
        if ok:
            QMessageBox.information(
                self,
                tr("dialogs.graphics_mode_set"),
                tr("dialogs.graphics_mode_message", mode=mode.capitalize()),
            )
            self._load()
        else:
            QMessageBox.critical(self, tr("dialogs.error"), tr("dialogs.graphics_mode_error", err=err))

    def _show_graphics_modes_help(self) -> None:
        """Muestra ventana emergente con la explicación de cada modo de gráficos."""
        t = lambda k: tr(f"help_graphics_modes.{k}")
        text = f"""<h3>{t('title')}</h3>
<p><b>Integrated</b><br/>{t('integrated')}</p>
<p><b>Hybrid (PRIME)</b><br/>{t('hybrid')}</p>
<p><b>NVIDIA</b><br/>{t('nvidia')}</p>
<p><b>Compute</b><br/>{t('compute')}</p>
<p><i>{t('reboot_note')}</i></p>"""
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("dialogs.graphics_help_title"))
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def refresh_ui(self) -> None:
        """Actualiza textos al cambiar el idioma."""
        self._title_label.setText(tr("system76_power.title"))
        self._desc_label.setText(tr("system76_power.desc"))
        self._current_label.setText(tr("system76_power.current_profile"))
        self._profile_group.setTitle(tr("system76_power.select_profile"))
        self._graphics_title_label.setText(tr("system76_power.graphics_title"))
        self._graphics_help_btn.setToolTip(tr("system76_power.graphics_help_tooltip"))
        self._graphics_note_label.setText(tr("system76_power.graphics_note"))
        self._graphics_current_label.setText(tr("system76_power.graphics_current"))
        self._graphics_group.setTitle(tr("system76_power.select_graphics"))
        self._refresh_btn.setText(tr("system76_power.refresh"))
        self._load()
