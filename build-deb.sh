#!/usr/bin/env bash
# Genera un paquete .deb de AsusControl.
# Uso: VERSION=1.0.0 ./build-deb.sh
# Salida: dist/poweradmin-asusstation_1.0.0_amd64.deb

set -e
cd "$(dirname "$0")"

VERSION="${VERSION:-1.0.0}"
PACKAGE_NAME="poweradmin-asusstation"
BINARY_NAME="PowerAdmin-AsusStation"
ARCH="amd64"

if ! command -v dpkg-deb &>/dev/null; then
  echo "dpkg-deb no encontrado. Necesitas estar en Debian/Ubuntu (o tener dpkg instalado)."
  exit 1
fi

# Construir binario solo si no existe (en CI ya está construido)
if [[ ! -f "dist/${BINARY_NAME}" ]]; then
  if ! command -v pyinstaller &>/dev/null; then
    echo "PyInstaller no encontrado. Instálalo con: pip install -r requirements-build.txt"
    exit 1
  fi
  echo "Construyendo binario con PyInstaller..."
  pyinstaller --noconfirm AsusControl.spec
fi

if [[ ! -f "dist/${BINARY_NAME}" ]]; then
  echo "Error: no se encontró dist/${BINARY_NAME}"
  exit 1
fi

ROOT="dist/${PACKAGE_NAME}_root"
rm -rf "$ROOT"
mkdir -p "$ROOT/DEBIAN"
mkdir -p "$ROOT/usr/bin"
mkdir -p "$ROOT/usr/share/applications"

# Binario en /usr/bin (nombre fijo para el comando del sistema)
install -m 755 "dist/${BINARY_NAME}" "$ROOT/usr/bin/${BINARY_NAME}"

# Entrada de escritorio (menú de aplicaciones)
install -m 644 packaging/poweradmin-asusstation.desktop "$ROOT/usr/share/applications/"

# DEBIAN/control
cat > "$ROOT/DEBIAN/control" << EOF
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: AsusControl <noreply@localhost>
Description: AsusControl - supergfxctl, asusctl y system76-power en portátiles ASUS y Pop!_OS
 Aplicación de escritorio en Python con PyQt6 para gestionar modos
 de gráficos, perfiles de energía y batería.
EOF

echo "Empaquetando .deb..."
dpkg-deb --root-owner-group --build "$ROOT" "dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
rm -rf "$ROOT"

echo ""
echo "Listo: dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo "Instalar con: sudo dpkg -i dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo "Después podrás ejecutar: PowerAdmin-AsusStation"
echo "O abrirlo desde el menú de aplicaciones como 'AsusControl'."
