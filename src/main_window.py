"""Ventana principal de la aplicación AsusControl."""

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QMessageBox,
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from .supergfxctl import (
    get_supported_modes,
    get_current_mode,
    get_pending_mode,
    get_pending_action,
    set_mode,
)


class MainWindow(QMainWindow):
    """Ventana principal para administrar modos de gráficos con supergfxctl."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_ui()
        self._load_modes()

    def _setup_ui(self) -> None:
        self.setWindowTitle("AsusControl - Modos de gráficos")
        self.setMinimumSize(400, 300)
        self.resize(500, 450)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(12)

        # Título
        title = QLabel("Modos de gráficos (supergfxctl)")
        title.setFont(QFont("", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Modo actual
        self._current_label = QLabel("Modo actual: --")
        self._current_label.setFont(QFont("", 11))
        layout.addWidget(self._current_label)

        # Cambio pendiente
        self._pending_label = QLabel("Cambio pendiente: --")
        self._pending_label.setFont(QFont("", 10))
        self._pending_label.setStyleSheet("color: #c75000;")
        layout.addWidget(self._pending_label)

        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Botones de modos (contenedor con scroll si hay muchos)
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

        # Botón actualizar
        self._refresh_btn = QPushButton("Actualizar modos")
        self._refresh_btn.clicked.connect(self._load_modes)
        layout.addWidget(self._refresh_btn)

    def _load_modes(self) -> None:
        """Carga los modos soportados y actualiza el modo actual."""
        self._refresh_btn.setEnabled(False)

        # Limpiar botones anteriores
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
            self._pending_label.setVisible(True)
        else:
            self._pending_label.setText("Cambio pendiente: ninguno")
            self._pending_label.setVisible(True)

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
                    btn.setStyleSheet("font-weight: bold;")
                btn.clicked.connect(lambda checked, m=mode: self._on_mode_clicked(m))
                row, col = divmod(i, cols)
                self._modes_layout.addWidget(btn, row, col)

        self._refresh_btn.setEnabled(True)

    def _on_mode_clicked(self, mode: str) -> None:
        """Maneja el clic en un botón de modo."""
        ok, err = set_mode(mode)
        if ok:
            QMessageBox.information(
                self,
                "Modo cambiado",
                f"Se está cambiando a modo '{mode}'.\n\n"
                "Algunos cambios requieren cerrar sesión o reiniciar.\n"
                "Verifica el estado con supergfxctl -g.",
            )
            self._load_modes()
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo cambiar el modo:\n{err}",
            )
