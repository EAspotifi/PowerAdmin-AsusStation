#!/usr/bin/env python3
"""Punto de entrada principal de AsusControl."""

import sys
from PyQt6.QtWidgets import QApplication

from src.app.main_window import MainWindow
from src.app.theme import ThemeKind, apply_theme


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("AsusControl")
    app.setOrganizationName("AsusControl")

    apply_theme(app, ThemeKind.DARK)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
