"""Ventana principal: barra lateral, contenido por sección y selector de tema."""

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QSlider,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .sidebar import Sidebar, SIDEBAR_ID_SUPERGFXCTL, SIDEBAR_ID_ASUSCTL
from .theme import ThemeKind, apply_theme, get_highlight_color
from src.features.supergfxctl.page import SupergfxctlPage
from src.features.asusctl.page import AsusctlPage


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
        self._setup_ui()
        self._connect_sidebar()

    def _setup_ui(self) -> None:
        self.setWindowTitle("AsusControl")
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
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)

        # Esquina superior derecha: slide tema (claro ↔ oscuro)
        top_bar = QHBoxLayout()
        top_bar.addStretch(1)
        theme_label = QLabel("Tema")
        theme_label.setFont(QFont("", 9))
        top_bar.addWidget(theme_label)
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
        self._supergfxctl_page = SupergfxctlPage(
            pending_highlight_color=get_highlight_color(self._theme),
        )
        self._asusctl_page = AsusctlPage(self)
        self._stack.addWidget(self._supergfxctl_page)
        self._stack.addWidget(self._asusctl_page)
        content_layout.addWidget(self._stack, 1)

        main_layout.addWidget(content, 1)

    def _connect_sidebar(self) -> None:
        self._sidebar.on_section_changed(self._on_section_changed)
        self._on_section_changed(self._sidebar.current_id())

    def _on_section_changed(self, section_id: str) -> None:
        if section_id == SIDEBAR_ID_SUPERGFXCTL:
            self._stack.setCurrentWidget(self._supergfxctl_page)
        elif section_id == SIDEBAR_ID_ASUSCTL:
            self._stack.setCurrentWidget(self._asusctl_page)

    def _on_theme_slider_changed(self, value: int) -> None:
        app = QApplication.instance()
        self._theme = ThemeKind.DARK if value == 1 else ThemeKind.LIGHT
        apply_theme(app, self._theme)
        self._supergfxctl_page.set_pending_highlight_color(get_highlight_color(self._theme))
