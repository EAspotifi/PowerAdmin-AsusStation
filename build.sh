#!/usr/bin/env bash
# Build de PowerAdmin-AsusStation con PyInstaller.
# Uso: ./build.sh
# Salida: dist/PowerAdmin-AsusStation (ejecutable)

set -e
cd "$(dirname "$0")"

if ! command -v pyinstaller &>/dev/null; then
  echo "PyInstaller no encontrado. Instálalo con:"
  echo "  pip install -r requirements-build.txt"
  exit 1
fi

echo "Construyendo PowerAdmin-AsusStation..."
pyinstaller --noconfirm AsusControl.spec

echo ""
echo "Listo. Ejecutable en: dist/PowerAdmin-AsusStation"
echo "Para crear un release: comprime el ejecutable (p. ej. como PowerAdmin-AsusStation-1.0.0) y súbelo a GitHub Releases."
