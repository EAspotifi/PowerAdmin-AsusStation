"""Ventana principal: barra lateral, contenido por sección y selector de tema."""

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QScrollArea,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QSlider,
    QLabel,
    QComboBox,
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont

from .i18n import (
    tr,
    get_language,
    set_language,
    on_language_changed,
    SUPPORTED,
    language_display_name,
)
from .sidebar import (
    Sidebar,
    SIDEBAR_ID_SUPERGFXCTL,
    SIDEBAR_ID_ASUSCTL,
    SIDEBAR_ID_SYSTEM76_POWER,
)
from .theme import ThemeKind, apply_theme, get_highlight_color
from src.features.supergfxctl.page import SupergfxctlPage
from src.features.asusctl.container import AsusctlContainer
from src.features.system76_power.page import System76PowerPage


def _theme_slider_stylesheet() -> str:
    """Estilo del slide tema: 0 = claro, 1 = oscuro. Neutro para ambos temas."""
    return """
        QSlider::groove:horizontal {
            height: 22px;
            border-radius: 11px;
            background: #6c7086;
        }
        QSlider::handle:horizontal {
            width: 20px;
            height: 20px;
            margin: 1px;
            border-radius: 10px;
            background: #cdd6f4;
        }
        QSlider::handle:horizontal:hover {
            background: #f5e0dc;
        }
        QSlider::sub-page:horizontal {
            border-radius: 11px;
            background: #89b4fa;
        }
    """


class MainWindow(QMainWindow):
    """Shell de la aplicación: sidebar + páginas por slice + tema claro/oscuro."""

    def __init__(self) -> None:
        super().__init__()
        self._theme = ThemeKind.DARK
        self._settings = QSettings("AsusControl", "AsusControl")
        saved = self._settings.value("language", "es")
        if saved in SUPPORTED:
            set_language(saved)
        self._setup_ui()
        self._connect_sidebar()
        self._sync_lang_combo()
        on_language_changed(self._refresh_all_ui)

    def _setup_ui(self) -> None:
        self.setWindowTitle(tr("app.title"))
        self.setMinimumSize(700, 450)
        self.resize(800, 500)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Barra lateral (ancho fijo)
        self._sidebar = Sidebar(self)
        self._sidebar.setFixedWidth(200)
        self._sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )
        main_layout.addWidget(self._sidebar)

        # Separador vertical
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        sep.setFixedWidth(1)
        main_layout.addWidget(sep)

        # Contenedor: barra superior (tema) + stacked widget
        content = QWidget()
        content.setMinimumWidth(400)
        content.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)

        # Barra superior: idioma + tema
        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        self._lang_label = QLabel(tr("app.language"))
        self._lang_label.setFont(QFont("", 9))
        top_bar.addWidget(self._lang_label)
        self._lang_combo = QComboBox()
        self._lang_combo.setMinimumWidth(120)
        for code in SUPPORTED:
            self._lang_combo.addItem(language_display_name(code), code)
        self._lang_combo.currentIndexChanged.connect(self._on_language_changed)
        top_bar.addWidget(self._lang_combo)
        self._theme_label = QLabel(tr("app.theme"))
        self._theme_label.setFont(QFont("", 9))
        top_bar.addWidget(self._theme_label)
        self._theme_slider = QSlider(Qt.Orientation.Horizontal)
        self._theme_slider.setObjectName("themeSlider")
        self._theme_slider.setMinimum(0)
        self._theme_slider.setMaximum(1)
        self._theme_slider.setValue(1)  # 1 = oscuro por defecto
        self._theme_slider.setFixedSize(48, 24)
        self._theme_slider.setStyleSheet(_theme_slider_stylesheet())
        self._theme_slider.valueChanged.connect(self._on_theme_slider_changed)
        top_bar.addWidget(self._theme_slider)
        content_layout.addLayout(top_bar)

        self._stack = QStackedWidget(self)
        self._stack.setMinimumWidth(380)
        self._stack.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )
        self._supergfxctl_page = SupergfxctlPage(
            pending_highlight_color=get_highlight_color(self._theme),
        )
        self._asusctl_container = AsusctlContainer(self)
        self._system76_page = System76PowerPage(self)
        self._stack.addWidget(self._supergfxctl_page)
        self._stack.addWidget(self._asusctl_container)
        self._stack.addWidget(self._system76_page)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setWidget(self._stack)
        scroll.setMinimumHeight(200)
        content_layout.addWidget(scroll, 1)

        main_layout.addWidget(content, 1)

    def _sync_lang_combo(self) -> None:
        """Sincroniza el combo de idioma con el idioma actual."""
        current = get_language()
        for i in range(self._lang_combo.count()):
            if self._lang_combo.itemData(i) == current:
                self._lang_combo.blockSignals(True)
                self._lang_combo.setCurrentIndex(i)
                self._lang_combo.blockSignals(False)
                break

    def _on_language_changed(self, index: int) -> None:
        code = self._lang_combo.itemData(index)
        if code and code in SUPPORTED:
            self._settings.setValue("language", code)
            set_language(code)

    def _refresh_all_ui(self) -> None:
        """Actualiza todos los textos de la UI al cambiar el idioma."""
        self.setWindowTitle(tr("app.title"))
        self._theme_label.setText(tr("app.theme"))
        self._lang_label.setText(tr("app.language"))
        for i in range(self._lang_combo.count()):
            code = self._lang_combo.itemData(i)
            self._lang_combo.setItemText(i, language_display_name(code))
        self._sidebar.refresh_ui()
        self._supergfxctl_page.refresh_ui()
        self._asusctl_container.refresh_ui()
        self._system76_page.refresh_ui()

    def _connect_sidebar(self) -> None:
        self._sidebar.on_section_changed(self._on_section_changed)
        self._on_section_changed(self._sidebar.current_id())

    def _on_section_changed(self, section_id: str) -> None:
        if section_id == SIDEBAR_ID_SUPERGFXCTL:
            self._stack.setCurrentWidget(self._supergfxctl_page)
        elif section_id == SIDEBAR_ID_ASUSCTL:
            self._stack.setCurrentWidget(self._asusctl_container)
        elif section_id == SIDEBAR_ID_SYSTEM76_POWER:
            self._stack.setCurrentWidget(self._system76_page)

    def _on_theme_slider_changed(self, value: int) -> None:
        app = QApplication.instance()
        self._theme = ThemeKind.DARK if value == 1 else ThemeKind.LIGHT
        apply_theme(app, self._theme)
        self._supergfxctl_page.set_pending_highlight_color(get_highlight_color(self._theme))
