#!/usr/bin/env bash
# Build de AsusControl con PyInstaller.
# Uso: ./build.sh
# Salida: dist/AsusControl (ejecutable)

set -e
cd "$(dirname "$0")"

if ! command -v pyinstaller &>/dev/null; then
  echo "PyInstaller no encontrado. Instálalo con:"
  echo "  pip install -r requirements-build.txt"
  exit 1
fi

echo "Construyendo AsusControl..."
pyinstaller --noconfirm AsusControl.spec

echo ""
echo "Listo. Ejecutable en: dist/AsusControl"
echo "Para crear un release: comprime dist/AsusControl o el contenido de dist/ y súbelo a GitHub Releases."
