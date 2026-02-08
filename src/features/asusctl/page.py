"""UI del slice Asusctl: información del sistema y controles."""

import re
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
    QGroupBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .cli import (
    get_info,
    get_battery_info,
    set_battery_limit,
    profile_list,
    profile_get,
    profile_set,
    profile_set_battery,
)


class AsusctlPage(QWidget):
    """Página asusctl: información del dispositivo y controles (por implementar)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Asusctl")
        title.setObjectName("pageTitle")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Sección Información (asusctl info)
        info_label = QLabel("Información")
        info_label.setFont(QFont("", 11, QFont.Weight.Bold))
        layout.addWidget(info_label)

        self._info_text = QLabel()
        self._info_text.setObjectName("asusctlInfoText")
        self._info_text.setWordWrap(True)
        self._info_text.setFont(QFont("Monospace", 10))
        self._info_text.setText("Cargando…")
        self._info_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.StyledPanel)
        scroll.setMinimumHeight(120)
        scroll.setWidget(self._info_text)
        layout.addWidget(scroll)

        btn_refresh = QPushButton("Actualizar información")
        btn_refresh.clicked.connect(self._load_info)
        layout.addWidget(btn_refresh)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Sección Batería
        battery_label = QLabel("Batería")
        battery_label.setFont(QFont("", 11, QFont.Weight.Bold))
        layout.addWidget(battery_label)

        self._battery_info_text = QLabel()
        self._battery_info_text.setWordWrap(True)
        self._battery_info_text.setFont(QFont("Monospace", 10))
        self._battery_info_text.setText("Cargando…")
        self._battery_info_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        battery_scroll = QScrollArea()
        battery_scroll.setWidgetResizable(True)
        battery_scroll.setFrameShape(QFrame.Shape.StyledPanel)
        battery_scroll.setMinimumHeight(60)
        battery_scroll.setWidget(self._battery_info_text)
        layout.addWidget(battery_scroll)

        # Límite de carga: solo números (20-100)
        limit_row = QHBoxLayout()
        limit_row.addWidget(QLabel("Límite de carga (%):"))
        self._limit_spin = QSpinBox()
        self._limit_spin.setRange(20, 100)
        self._limit_spin.setSuffix(" %")
        self._limit_spin.setMinimumWidth(100)
        limit_row.addWidget(self._limit_spin)
        limit_row.addStretch(1)
        layout.addLayout(limit_row)

        btn_apply_limit = QPushButton("Establecer límite")
        btn_apply_limit.clicked.connect(self._apply_battery_limit)
        layout.addWidget(btn_apply_limit)

        # --- Separador Perfiles ---
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line2)

        # Sección Perfiles
        profile_sec = QLabel("Perfiles")
        profile_sec.setFont(QFont("", 11, QFont.Weight.Bold))
        layout.addWidget(profile_sec)

        # Estado actual (card)
        self._profile_state_group = QGroupBox("Estado actual")
        self._profile_state_group.setFont(QFont("", 10, QFont.Weight.Bold))
        state_layout = QVBoxLayout(self._profile_state_group)
        self._profile_active_label = QLabel("Activo: —")
        self._profile_ac_label = QLabel("En AC: —")
        self._profile_battery_label = QLabel("Con batería: —")
        for lbl in (self._profile_active_label, self._profile_ac_label, self._profile_battery_label):
            lbl.setFont(QFont("", 10))
            state_layout.addWidget(lbl)
        layout.addWidget(self._profile_state_group)

        # Perfil en uso ahora
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

        # Perfil con batería (automático)
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

        btn_refresh_profiles = QPushButton("Actualizar perfiles")
        btn_refresh_profiles.clicked.connect(self._load_profiles)
        layout.addWidget(btn_refresh_profiles)

        layout.addStretch(1)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._load_info()
        self._load_battery_info()
        self._load_profiles()

    def _load_info(self) -> None:
        """Carga y muestra la salida de asusctl info."""
        self._info_text.setText("Cargando…")
        text = get_info()
        self._info_text.setText(text or "Sin datos.")

    def _load_battery_info(self) -> None:
        """Carga y muestra la salida de asusctl battery info."""
        self._battery_info_text.setText("Cargando…")
        text = get_battery_info()
        self._battery_info_text.setText(text or "Sin datos.")
        # Rellenar el spin con el límite actual si aparece (ej. "Current battery charge limit: 80%")
        match = re.search(r"limit[:\s]+(\d+)\s*%?", text, re.IGNORECASE)
        if match:
            val = int(match.group(1))
            if 20 <= val <= 100:
                self._limit_spin.setValue(val)

    def _apply_battery_limit(self) -> None:
        """Aplica el límite de carga con asusctl battery limit."""
        percent = self._limit_spin.value()
        ok, err = set_battery_limit(percent)
        if ok:
            QMessageBox.information(
                self,
                "Límite de batería",
                f"Límite de carga establecido en {percent}%.",
            )
            self._load_battery_info()
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo establecer el límite:\n{err}",
            )

    def _parse_profile_get(self, text: str) -> tuple[str, str, str]:
        """Extrae activo, AC y batería del texto de asusctl profile get."""
        active = ac = battery = ""
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if "active" in line.lower() and "profile" in line.lower():
                # "Active profile: Performance"
                parts = line.split(":", 1)
                if len(parts) == 2:
                    active = parts[1].strip()
            elif line.lower().startswith("ac profile"):
                ac = line[10:].strip()
            elif "battery" in line.lower() and "profile" in line.lower():
                # "Battery profile Balanced"
                parts = line.split("profile", 1)
                if len(parts) == 2:
                    battery = parts[1].strip()
        return active, ac, battery

    def _load_profiles(self) -> None:
        """Carga lista de perfiles, estado actual y crea botones."""
        profiles = profile_list()
        state_text = profile_get()

        active, ac, battery = self._parse_profile_get(state_text)
        self._profile_active_label.setText(f"Activo: {active or '—'}")
        self._profile_ac_label.setText(f"En AC: {ac or '—'}")
        self._profile_battery_label.setText(f"Con batería: {battery or '—'}")

        # Limpiar botones anteriores
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
            btn_now.clicked.connect(lambda checked, n=name: self._set_current_profile(n))
            self._current_buttons_layout.addWidget(btn_now)

        for name in profiles:
            btn_bat = QPushButton(name)
            btn_bat.setMinimumHeight(36)
            btn_bat.setMinimumWidth(100)
            if name == battery:
                btn_bat.setStyleSheet("font-weight: bold;")
            btn_bat.clicked.connect(lambda checked, n=name: self._set_battery_profile(n))
            self._battery_buttons_layout.addWidget(btn_bat)

        self._current_buttons_layout.addStretch(1)
        self._battery_buttons_layout.addStretch(1)

    def _set_current_profile(self, profile: str) -> None:
        """Establece el perfil actual (asusctl profile set <nombre>)."""
        ok, err = profile_set(profile)
        if ok:
            QMessageBox.information(
                self,
                "Perfil actual",
                f"Perfil actual establecido en «{profile}».",
            )
            self._load_profiles()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el perfil:\n{err}")

    def _set_battery_profile(self, profile: str) -> None:
        """Establece el perfil cuando está en batería (--battery)."""
        ok, err = profile_set_battery(profile)
        if ok:
            QMessageBox.information(
                self,
                "Perfil con batería",
                f"Cuando uses batería se aplicará el perfil «{profile}».",
            )
            self._load_profiles()
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo establecer el perfil en batería:\n{err}",
            )
