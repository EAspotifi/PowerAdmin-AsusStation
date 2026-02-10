# Guía: paquete .deb e instalación — AsusControl

Esta guía explica cómo **generar** el paquete `.deb` de AsusControl, cómo **instalarlo** en el sistema y cómo **publicar un release** en GitHub.

---

## Índice

- [Requisitos para generar el .deb](#requisitos-para-generar-el-deb)
- [Generar el paquete .deb](#generar-el-paquete-deb)
- [Instalar el .deb](#instalar-el-deb)
- [Publicar un release en GitHub](#publicar-un-release-en-github)

---

## Requisitos para generar el .deb

- **Sistema**: Linux (Debian, Ubuntu o Pop!_OS recomendado; necesitas `dpkg-deb`).
- **Python**: 3.10 o superior.
- **Dependencias de build**:
  - PyInstaller: `pip install -r requirements-build.txt`
  - Dependencias del proyecto: `pip install -r requirements.txt`

Desde la raíz del repositorio:

```bash
pip install -r requirements.txt
pip install -r requirements-build.txt
```

---

## Generar el paquete .deb

El script `build-deb.sh` hace lo siguiente:

1. Si no existe el binario, construye el ejecutable con PyInstaller (`AsusControl.spec`).
2. Crea la estructura del paquete (binario en `/usr/bin`, entrada en el menú de aplicaciones).
3. Genera el archivo `.deb` en `dist/`.

### Uso

Desde la **raíz del proyecto** (donde está `build-deb.sh`):

```bash
# Versión por defecto 1.0.0
./build-deb.sh

# Especificar versión (recomendado para releases)
VERSION=1.0.0 ./build-deb.sh
VERSION=1.1.0 ./build-deb.sh
```

### Salida

- **Archivo generado**: `dist/poweradmin-asusstation_<VERSION>_amd64.deb`  
  Ejemplo: `dist/poweradmin-asusstation_1.0.0_amd64.deb`

El paquete instala:

- Ejecutable: `/usr/bin/PowerAdmin-AsusStation`
- Entrada en el menú de aplicaciones: **AsusControl**

---

## Instalar el .deb

### Opción A: Instalar un .deb que acabas de generar

```bash
sudo dpkg -i dist/poweradmin-asusstation_1.0.0_amd64.deb
```

Si aparece algún error de dependencias:

```bash
sudo apt-get install -f
```

### Opción B: Instalar un .deb descargado de un release

1. Descarga desde [Releases](https://github.com/EAspotifi/PowerAdmin-AsusStation/releases) el archivo `poweradmin-asusstation_<versión>_amd64.deb`.
2. En la terminal, en la carpeta donde está el `.deb`:

```bash
sudo dpkg -i poweradmin-asusstation_1.0.0_amd64.deb
sudo apt-get install -f   # si lo pide dpkg
```

### Ejecutar AsusControl después de instalar

- **Menú de aplicaciones**: busca **"AsusControl"**.
- **Terminal**: `PowerAdmin-AsusStation`

Si alguna herramienta (supergfxctl, asusctl, system76-power) no está instalada, la app mostrará **"No disponible"** en esa sección y no intentará instalarla. En la barra superior puedes activar la opción **"Auto-instalar paquetes faltantes"** (se guarda en la configuración).

### Desinstalar

```bash
sudo apt remove poweradmin-asusstation
```

---

## Publicar un release en GitHub

Cada vez que creas y subes un **tag** con formato `v*` (por ejemplo `v1.0.0`), GitHub Actions construye automáticamente los artefactos y crea (o actualiza) el **release** con:

- `poweradmin-asusstation_<versión>_amd64.deb`
- `PowerAdmin-AsusStation-<versión>-linux-x86_64.tar.gz` (ejecutable para quien no use .deb)

### Pasos para publicar un release

1. **Asegúrate de que los cambios están en la rama principal** (por ejemplo `main` o `master`):

   ```bash
   git status
   git add .
   git commit -m "Descripción de los cambios"
   git push origin main
   ```

2. **Crea un tag con la versión** (usa el número de versión que quieras, por ejemplo `1.0.0`):

   ```bash
   git tag v1.0.0
   ```

   Para una versión ya publicada, no reutilices el mismo tag. Para la siguiente release usa por ejemplo `v1.1.0`.

3. **Sube el tag a GitHub**:

   ```bash
   git push origin v1.0.0
   ```

4. **En GitHub**:
   - Ve al repositorio → pestaña **Releases** (o a la URL de releases del repo).
   - En unos minutos, el **workflow de GitHub Actions** habrá generado el build y habrá creado (o actualizado) el release con ese tag.
   - En el release verás adjuntos el `.deb` y el `.tar.gz` para que los usuarios los descarguen.

### Resumen rápido

```bash
git add .
git commit -m "Preparar release 1.0.0"
git push origin main

git tag v1.0.0
git push origin v1.0.0
```

Después, el release aparecerá en **Releases** con los archivos listos para descargar. Los usuarios pueden instalar AsusControl con el `.deb` tal como se describe en [Instalar el .deb](#instalar-el-deb).
