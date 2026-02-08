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

from src.app.i18n import tr
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

        self._title_label = QLabel(tr("asusctl_profiles.title"))
        self._title_label.setObjectName("pageTitle")
        self._title_label.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(self._title_label)

        self._profile_active_label = QLabel(tr("asusctl_profiles.active"))
        self._profile_ac_label = QLabel(tr("asusctl_profiles.ac"))
        self._profile_battery_label = QLabel(tr("asusctl_profiles.battery"))
        for lbl in (self._profile_active_label, self._profile_ac_label, self._profile_battery_label):
            lbl.setFont(QFont("", 10))
            layout.addWidget(lbl)

        self._now_group = QGroupBox(tr("asusctl_profiles.now_group"))
        self._now_group.setFont(QFont("", 9))
        now_layout = QVBoxLayout(self._now_group)
        now_desc = QLabel(tr("asusctl_profiles.now_desc"))
        now_desc.setWordWrap(True)
        now_desc.setStyleSheet("color: gray; font-weight: normal;")
        now_layout.addWidget(now_desc)
        self._current_buttons_layout = QHBoxLayout()
        self._current_buttons_layout.setSpacing(8)
        now_layout.addLayout(self._current_buttons_layout)
        layout.addWidget(self._now_group)

        self._bat_group = QGroupBox(tr("asusctl_profiles.battery_group"))
        self._bat_group.setFont(QFont("", 9))
        bat_layout = QVBoxLayout(self._bat_group)
        bat_desc = QLabel(tr("asusctl_profiles.battery_desc"))
        bat_desc.setWordWrap(True)
        bat_desc.setStyleSheet("color: gray; font-weight: normal;")
        bat_layout.addWidget(bat_desc)
        self._battery_buttons_layout = QHBoxLayout()
        self._battery_buttons_layout.setSpacing(8)
        bat_layout.addLayout(self._battery_buttons_layout)
        layout.addWidget(self._bat_group)

        self._refresh_btn = QPushButton(tr("asusctl_profiles.refresh"))
        self._refresh_btn.clicked.connect(self._load)
        layout.addWidget(self._refresh_btn)
        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load()

    def _load(self) -> None:
        profiles = get_profile_list()
        _, active, ac, battery = get_profile_state()

        self._profile_active_label.setText(tr("asusctl_profiles.active").replace("--", active or "—"))
        self._profile_ac_label.setText(tr("asusctl_profiles.ac").replace("--", ac or "—"))
        self._profile_battery_label.setText(tr("asusctl_profiles.battery").replace("--", battery or "—"))

        while self._current_buttons_layout.count():
            item = self._current_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        while self._battery_buttons_layout.count():
            item = self._battery_buttons_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not profiles:
            self._current_buttons_layout.addWidget(QLabel(tr("asusctl_profiles.no_profiles")))
            self._battery_buttons_layout.addWidget(QLabel(tr("asusctl_profiles.no_profiles")))
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
            QMessageBox.information(self, tr("dialogs.profile_set"), tr("dialogs.profile_set_message", profile=profile))
            self._load()
        else:
            QMessageBox.critical(self, tr("dialogs.error"), tr("dialogs.profile_error", err=err))

    def _set_battery(self, profile: str) -> None:
        ok, err = set_battery_profile(profile)
        if ok:
            QMessageBox.information(
                self,
                tr("dialogs.battery_profile"),
                tr("dialogs.battery_profile_message", profile=profile),
            )
            self._load()
        else:
            QMessageBox.critical(self, tr("dialogs.error"), tr("dialogs.battery_profile_error", err=err))

    def refresh_ui(self) -> None:
        self._title_label.setText(tr("asusctl_profiles.title"))
        self._profile_active_label.setText(tr("asusctl_profiles.active"))
        self._profile_ac_label.setText(tr("asusctl_profiles.ac"))
        self._profile_battery_label.setText(tr("asusctl_profiles.battery"))
        self._now_group.setTitle(tr("asusctl_profiles.now_group"))
        self._bat_group.setTitle(tr("asusctl_profiles.battery_group"))
        self._refresh_btn.setText(tr("asusctl_profiles.refresh"))
        self._load()
