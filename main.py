#!/usr/bin/env python3
"""Punto de entrada principal de AsusControl."""

import sys
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("AsusControl")
    app.setOrganizationName("AsusControl")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
