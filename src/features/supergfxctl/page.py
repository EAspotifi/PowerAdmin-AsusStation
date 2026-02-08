"""UI del slice Supergfxctl: página de modos de gráficos."""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QMessageBox,
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .cli import (
    get_supported_modes,
    get_current_mode,
    get_pending_mode,
    get_pending_action,
    set_mode,
)


class SupergfxctlPage(QWidget):
    """Página que muestra modo actual, pendiente y botones para cambiar modo (supergfxctl)."""

    def __init__(self, pending_highlight_color: str = "#c75000", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._pending_highlight_color = pending_highlight_color
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("Modos de gráficos (supergfxctl)")
        title.setObjectName("pageTitle")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        self._current_label = QLabel("Modo actual: --")
        self._current_label.setFont(QFont("", 11))
        layout.addWidget(self._current_label)

        self._pending_label = QLabel("Cambio pendiente: --")
        self._pending_label.setFont(QFont("", 10))
        self._pending_label.setStyleSheet(f"color: {self._pending_highlight_color};")
        layout.addWidget(self._pending_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        modes_label = QLabel("Selecciona un modo:")
        modes_label.setFont(QFont("", 10))
        layout.addWidget(modes_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._modes_container = QWidget()
        self._modes_layout = QGridLayout(self._modes_container)
        self._modes_layout.setSpacing(8)
        scroll.setWidget(self._modes_container)
        layout.addWidget(scroll, 1)

        self._refresh_btn = QPushButton("Actualizar modos")
        self._refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(self._refresh_btn)

    def set_pending_highlight_color(self, color: str) -> None:
        """Actualiza el color de la etiqueta de cambio pendiente (p. ej. al cambiar tema)."""
        self._pending_highlight_color = color
        self._pending_label.setStyleSheet(f"color: {color};")

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.refresh()

    def refresh(self) -> None:
        """Carga modos, modo actual y pendiente desde supergfxctl."""
        self._refresh_btn.setEnabled(False)
        while self._modes_layout.count():
            item = self._modes_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        modes = get_supported_modes()
        current = get_current_mode()
        pending_mode = get_pending_mode()
        pending_action = get_pending_action()

        self._current_label.setText(f"Modo actual: {current or '--'}")
        if pending_mode:
            msg = f"Cambio pendiente: {pending_mode}"
            if pending_action:
                msg += f" ({pending_action})"
            self._pending_label.setText(msg)
        else:
            self._pending_label.setText("Cambio pendiente: ninguno")

        if not modes:
            label = QLabel("No se encontraron modos o supergfxctl no está disponible.")
            label.setWordWrap(True)
            self._modes_layout.addWidget(label, 0, 0)
        else:
            cols = 2
            for i, mode in enumerate(modes):
                btn = QPushButton(mode)
                btn.setMinimumHeight(44)
                btn.setMinimumWidth(140)
                if mode == current:
                    btn.setStyleSheet(btn.styleSheet() + " font-weight: bold;")
                btn.clicked.connect(lambda checked, m=mode: self._on_mode_clicked(m))
                row, col = divmod(i, cols)
                self._modes_layout.addWidget(btn, row, col)

        self._refresh_btn.setEnabled(True)

    def _on_mode_clicked(self, mode: str) -> None:
        ok, err = set_mode(mode)
        if ok:
            QMessageBox.information(
                self,
                "Modo cambiado",
                f"Se está cambiando a modo '{mode}'.\n\n"
                "Algunos cambios requieren cerrar sesión o reiniciar.",
            )
            self.refresh()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo cambiar el modo:\n{err}")
