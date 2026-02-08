#!/usr/bin/env python3
"""Punto de entrada principal de AsusControl."""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from src.app.main_window import MainWindow
from src.app.theme import ThemeKind, apply_theme


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("AsusControl")
    app.setOrganizationName("AsusControl")

    apply_theme(app, ThemeKind.DARK)

    window = MainWindow()
    window.show()

    # Evita superposición al iniciar: tras el primer frame, forzar recálculo del layout
    QTimer.singleShot(0, lambda: _refresh_layout_after_show(app, window))

    sys.exit(app.exec())


def _refresh_layout_after_show(app: QApplication, window: MainWindow) -> None:
    apply_theme(app, ThemeKind.DARK)
    central = window.centralWidget()
    if central:
        central.updateGeometry()
        central.update()
    window.updateGeometry()


if __name__ == "__main__":
    main()
