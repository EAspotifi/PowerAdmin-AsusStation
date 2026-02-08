"""Página: Perfiles de rendimiento."""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..use_cases.profiles import (
    get_profile_list,
    get_profile_state,
    set_current_profile,
    set_battery_profile,
)


class ProfilesPage(QWidget):
    """Perfiles de rendimiento: estado actual, perfil en uso y perfil con batería."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Perfiles de rendimiento")
        title.setObjectName("pageTitle")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        self._profile_active_label = QLabel("Activo: —")
        self._profile_ac_label = QLabel("En AC: —")
        self._profile_battery_label = QLabel("Con batería: —")
        for lbl in (self._profile_active_label, self._profile_ac_label, self._profile_battery_label):
            lbl.setFont(QFont("", 10))
            layout.addWidget(lbl)

        now_group = QGroupBox("Perfil en uso ahora")
        now_group.setFont(QFont("", 9))
        now_layout = QVBoxLayout(now_group)
        now_desc = QLabel("Elige el perfil que quieres usar en este momento.")
        now_desc.setWordWrap(True)
        now_desc.setStyleSheet("color: gray; font-weight: normal;")
        now_layout.addWidget(now_desc)
        self._current_buttons_layout = QHBoxLayout()
        self._current_buttons_layout.setSpacing(8)
        now_layout.addLayout(self._current_buttons_layout)
        layout.addWidget(now_group)

        bat_group = QGroupBox("Perfil con batería (automático)")
        bat_group.setFont(QFont("", 9))
        bat_layout = QVBoxLayout(bat_group)
        bat_desc = QLabel("Perfil que se usará cuando el portátil esté solo con batería.")
        bat_desc.setWordWrap(True)
        bat_desc.setStyleSheet("color: gray; font-weight: normal;")
        bat_layout.addWidget(bat_desc)
        self._battery_buttons_layout = QHBoxLayout()
        self._battery_buttons_layout.setSpacing(8)
        bat_layout.addLayout(self._battery_buttons_layout)
        layout.addWidget(bat_group)

        btn = QPushButton("Actualizar perfiles")
        btn.clicked.connect(self._load)
        layout.addWidget(btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        profiles = get_profile_list()
        _, active, ac, battery = get_profile_state()

        self._profile_active_label.setText(f"Activo: {active or '—'}")
        self._profile_ac_label.setText(f"En AC: {ac or '—'}")
        self._profile_battery_label.setText(f"Con batería: {battery or '—'}")

        while self._current_buttons_layout.count():
            item = self._current_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        while self._battery_buttons_layout.count():
            item = self._battery_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not profiles:
            self._current_buttons_layout.addWidget(QLabel("No se encontraron perfiles."))
            self._battery_buttons_layout.addWidget(QLabel("No se encontraron perfiles."))
            return

        for name in profiles:
            btn_now = QPushButton(name)
            btn_now.setMinimumHeight(36)
            btn_now.setMinimumWidth(100)
            if name == active:
                btn_now.setStyleSheet("font-weight: bold;")
            btn_now.clicked.connect(lambda checked, n=name: self._set_current(n))
            self._current_buttons_layout.addWidget(btn_now)

        for name in profiles:
            btn_bat = QPushButton(name)
            btn_bat.setMinimumHeight(36)
            btn_bat.setMinimumWidth(100)
            if name == battery:
                btn_bat.setStyleSheet("font-weight: bold;")
            btn_bat.clicked.connect(lambda checked, n=name: self._set_battery(n))
            self._battery_buttons_layout.addWidget(btn_bat)

        self._current_buttons_layout.addStretch(1)
        self._battery_buttons_layout.addStretch(1)

    def _set_current(self, profile: str) -> None:
        ok, err = set_current_profile(profile)
        if ok:
            QMessageBox.information(self, "Perfil actual", f"Perfil actual establecido en «{profile}».")
            self._load()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el perfil:\n{err}")

    def _set_battery(self, profile: str) -> None:
        ok, err = set_battery_profile(profile)
        if ok:
            QMessageBox.information(
                self,
                "Perfil con batería",
                f"Cuando uses batería se aplicará el perfil «{profile}».",
            )
            self._load()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo establecer el perfil en batería:\n{err}")
