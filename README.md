# AsusControl

Aplicación de escritorio en Python con PyQt6 para administrar **supergfxctl**, **asusctl** y **system76-power** en portátiles ASUS y System76/Pop!_OS (modos de gráficos, perfiles de energía, batería). Pensada para empaquetar como ejecutable en Ubuntu, Fedora y Debian.

Para **generar e instalar el paquete .deb** y **publicar un release**, consulta la [Guía del paquete .deb y releases](GUIA-DEB-Y-RELEASES.md).

## Índice

- [Guía .deb y releases](GUIA-DEB-Y-RELEASES.md) — generar .deb, instalación y publicar un release
- [Instalación y ejecución](#instalación-y-ejecución)
  - [Requisitos previos](#requisitos-previos)
  - [Instalación con paquete .deb (recomendada)](#instalación-con-paquete-deb-recomendada)
  - [Instalación desde el código fuente](#instalación-desde-el-código-fuente)
  - [Ejecución](#ejecución)
  - [Instalación desde un release (ejecutable)](#instalación-desde-un-release-ejecutable)
- [Qué necesita el proyecto para funcionar](#qué-necesita-el-proyecto-para-funcionar)
- [Desarrollo](#desarrollo)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Funciones por módulo](#funciones-por-módulo)
  - [Normas para colaboraciones](#normas-para-colaboraciones)

---

## Instalación y ejecución

### Requisitos previos

| Requisito      | Versión / Notas |
|----------------|------------------|
| **Python**     | 3.10 o superior  |
| **PyQt6**      | ≥ 6.6.0          |
| **Sistema**    | Linux (X11 o Wayland) |

**Herramientas opcionales** (la app funciona sin ellas; cada sección usa la que exista):

| Sección          | Herramienta        |
|------------------|--------------------|
| **Supergfxctl**  | `supergfxctl` + servicio `supergfxd` |
| **Asusctl**      | `asusctl`          |
| **System76-power** | `system76-power` |

En **X11**, si la ventana no arranca por el plugin Qt:  
`sudo apt install libxcb-cursor0` (Debian/Ubuntu).

---

### Instalación con paquete .deb (recomendada)

En **Debian, Ubuntu y Pop!_OS** la forma más sencilla es instalar el paquete `.deb` desde [Releases](https://github.com/EAspotifi/PowerAdmin-AsusStation/releases):

1. Descarga `poweradmin-asusstation_1.0.0_amd64.deb` (o la versión que aparezca en el release).
2. Instala con:

```bash
sudo dpkg -i poweradmin-asusstation_1.0.0_amd64.deb
```

Si `dpkg` avisa de dependencias sin instalar:

```bash
sudo apt-get install -f
```

3. Listo. Puedes ejecutar **AsusControl** de dos formas:
   - **Desde el menú de aplicaciones**: busca **"AsusControl"**.
   - **Desde la terminal**: `PowerAdmin-AsusStation`.

El paquete instala el ejecutable en `/usr/bin` y una entrada en el menú de aplicaciones; no necesitas permisos manuales ni mover archivos.

---

### Instalación desde el código fuente

**1. Clonar e ingresar al proyecto**

```bash
git clone https://github.com/<tu-usuario>/PowerAdmin-AsusStation.git
cd PowerAdmin-AsusStation
```

**2. Crear y activar el entorno virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

*(En Windows: `.venv\Scripts\activate`)*

**3. Instalar dependencias**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. (Opcional) Instalar herramientas del sistema**

- **Supergfxctl**: [supergfxctl](https://gitlab.com/asus-linux/supergfxctl) + servicio `supergfxd`, usuario en grupo `users`/`wheel`/`adm`.
- **Asusctl**: [asusctl](https://gitlab.com/asus-linux/asusctl).
- **System76-power**: suele venir en Pop!_OS.

---

### Ejecución

Con el entorno virtual **activado**:

```bash
python main.py
```

Sin activar el venv (desde la raíz del proyecto):

```bash
.venv/bin/python main.py
```

---

### Instalación desde un release (ejecutable)

En cada [release](https://github.com/EAspotifi/PowerAdmin-AsusStation/releases) encontrarás:
- **`poweradmin-asusstation_1.0.0_amd64.deb`** — recomendado en Debian/Ubuntu/Pop!_OS (ver [Instalación con paquete .deb](#instalación-con-paquete-deb-recomendada)).
- **`PowerAdmin-AsusStation-1.0.0-linux-x86_64.tar.gz`** — un **solo archivo ejecutable** (no es el código fuente).

Si usas el tarball:

```bash
tar xzf PowerAdmin-AsusStation-1.0.0-linux-x86_64.tar.gz
chmod +x PowerAdmin-AsusStation-1.0.0
./PowerAdmin-AsusStation-1.0.0
```

Para tenerlo en el PATH:

```bash
mv PowerAdmin-AsusStation-1.0.0 ~/.local/bin/
# Asegúrate de que ~/.local/bin está en tu PATH
PowerAdmin-AsusStation-1.0.0
```

**Nota:** Si al extraer ves una **carpeta** con `main.py`, `src/`, etc., es el **código fuente** (por ejemplo, si descargaste el ZIP del repositorio). En ese caso ejecuta con `python main.py` desde esa carpeta, o descarga el archivo del release que sea el ejecutable (`.tar.gz` del release) o el `.deb`.

---

## Qué necesita el proyecto para funcionar

1. **Entorno Python**: Python 3.10+ con el venv activado y `pip install -r requirements.txt` ejecutado.
2. **Display**: sesión gráfica (X11 o Wayland). No está pensada para servidor headless.
3. **Permisos**: las herramientas (`supergfxctl`, `asusctl`, `system76-power`) pueden requerir usuario en ciertos grupos o `sudo` según la distro; la app solo las invoca por CLI.
4. **Opcional en X11**: `libxcb-cursor0` para el plugin Qt xcb si aparece el error relacionado con «xcb-cursor».
5. **Herramientas no instaladas**: si alguna herramienta (supergfxctl, asusctl, system76-power) no está en el sistema, la app muestra **"No disponible"** y no intenta instalarla. En la barra superior hay una opción de configuración **"Auto-instalar paquetes faltantes"** (al final); su estado se guarda en la configuración y queda disponible para uso futuro.

No se necesitan variables de entorno obligatorias; opcionalmente en Wayland puedes forzar: `QT_QPA_PLATFORM=wayland python main.py`.

---

## Desarrollo

### Estructura del proyecto

El código sigue una arquitectura **Clean** con **vertical slices** y nombres que dejan claro el propósito de cada parte (**screaming architecture**).

```
PowerAdmin-AsusStation/
├── main.py                 # Punto de entrada; aplica tema y lanza MainWindow
├── requirements.txt        # PyQt6
├── README.md
├── .gitignore
├── languages/              # Traducciones (i18n)
│   ├── es.json
│   └── en.json
└── src/
    ├── app/                # Shell de la aplicación
    │   ├── main_window.py  # Ventana principal, barra lateral, scroll, tema e idioma
    │   ├── sidebar.py      # Menú lateral (Supergfxctl, Asusctl, System76-power)
    │   ├── theme.py        # Tema claro/oscuro (QSS), sin dependencias extra
    │   └── i18n.py         # Carga de idiomas desde JSON y traducción por claves
    │
    └── features/           # Un slice por “feature”
        ├── supergfxctl/    # Modos de gráficos (supergfxctl)
        │   ├── cli.py      # Llamadas a supergfxctl (-s, -g, -m, -P, -p)
        │   └── page.py     # UI de la página
        │
        ├── asusctl/        # Información, perfiles y batería (asusctl)
        │   ├── cli.py      # Llamadas a asusctl (info, battery, profile)
        │   ├── container.py# Contenedor: submenú (Información, Perfiles, Batería) + stack
        │   ├── use_cases/  # Casos de uso (orquestan lógica, llaman a cli)
        │   │   ├── info.py
        │   │   ├── battery.py
        │   │   └── profiles.py
        │   └── pages/      # Una página por subsección
        │       ├── info_page.py
        │       ├── battery_page.py
        │       └── profiles_page.py
        │
        └── system76_power/ # Perfiles de energía y modo de gráficos (system76-power)
            ├── cli.py      # Llamadas a system76-power (profile, graphics)
            └── page.py     # UI de la página
```

#### Funciones por módulo

| Módulo | Función / responsabilidad |
|--------|----------------------------|
| **main.py** | `main()` — crea `QApplication`, aplica tema oscuro, muestra `MainWindow` y refresca layout tras el primer frame. |
| **app/main_window.py** | `MainWindow` — shell: título, barra lateral, `QStackedWidget` con las tres secciones (Supergfxctl, Asusctl, System76-power), selector de idioma, slider de tema (claro/oscuro) y opción **Auto-instalar paquetes faltantes** al final de la barra. Guarda en `QSettings`: `language`, `auto_install`. Si una herramienta no está instalada, la UI muestra "No disponible". |
| **app/sidebar.py** | `Sidebar` — lista con ítems Supergfxctl, Asusctl, System76-power; `current_id()`, `on_section_changed(callback)`, `refresh_ui()`. Constantes: `SIDEBAR_ID_*`. |
| **app/theme.py** | `ThemeKind` (LIGHT/DARK), `get_stylesheet()`, `apply_theme()`, `get_highlight_color()` — QSS y paleta para tema claro/oscuro. |
| **app/i18n.py** | `tr(key, **kwargs)` — traduce por clave; `get_language()`, `set_language()`, `on_language_changed(callback)`; `language_display_name(code)`; `SUPPORTED`, `DEFAULT`. Carga JSON desde `languages/`. |
| **supergfxctl/cli.py** | `get_supported_modes()`, `get_current_mode()`, `get_pending_mode()`, `get_pending_action()`, `set_mode(mode)` — ejecutan `supergfxctl -s/-g/-P/-p/-m`. Si el binario no existe, devuelven "No disponible". |
| **supergfxctl/page.py** | `SupergfxctlPage` — muestra modo actual y pendiente, grid de botones por modo, refrescar; `set_pending_highlight_color()`, `refresh()`, `refresh_ui()`. |
| **asusctl/cli.py** | `get_info()`, `get_battery_info()`, `set_battery_limit(percent)`, `profile_list()`, `profile_get()`, `profile_set(profile)`, `profile_set_battery(profile)` — llamadas a `asusctl`. Si no está instalado, devuelven "No disponible". |
| **asusctl/container.py** | `AsusctlContainer` — submenú (Información, Perfiles, Batería) + `QStackedWidget` con `InfoPage`, `ProfilesPage`, `BatteryPage`; `refresh_ui()`. |
| **asusctl/use_cases/info.py** | `get_system_info()` — delega en `get_info()`. |
| **asusctl/use_cases/battery.py** | `get_battery_info()`, `set_battery_limit(percent)`, `parse_current_limit_from_info(text)` — orquestan batería. |
| **asusctl/use_cases/profiles.py** | `get_profile_list()`, `get_profile_state()` → (texto, activo, ac, batería), `set_current_profile()`, `set_battery_profile()` — orquestan perfiles. |
| **asusctl/pages/info_page.py** | `InfoPage` — texto de `asusctl info`, botón refrescar. |
| **asusctl/pages/battery_page.py** | `BatteryPage` — info de batería, spinbox 20–100 % y botón para fijar límite de carga. |
| **asusctl/pages/profiles_page.py** | `ProfilesPage` — estado activo/AC/batería, botones “perfil actual” y “perfil en batería”. |
| **system76_power/cli.py** | `get_profile()`, `get_profile_list()`, `set_profile(profile)`, `get_graphics_mode()`, `get_graphics_modes_list()`, `set_graphics_mode(mode)` — ejecutan `system76-power profile/graphics`. Si no está instalado, devuelven "No disponible". |
| **system76_power/page.py** | `System76PowerPage` — perfil actual (Battery/Balanced/Performance), botones de perfil y de modo gráfico (integrated/hybrid/nvidia/compute), ayuda de modos, `refresh_ui()`. |

- **app/**: composición global, barra lateral, tema, i18n y scroll del contenido.
- **features/*/cli.py**: único punto que ejecuta comandos externos (CLI); fácil de mockear en tests.
- **features/*/use_cases/** (donde exista): orquestan la lógica y devuelven datos a la UI; no conocen PyQt.
- **features/*/page.py** o **pages/**: solo UI y llamadas a casos de uso o cli; sin lógica de negocio pesada.

### Normas para colaboraciones

1. **Mantener los vertical slices**  
   Cada feature en su carpeta bajo `features/`. No mezclar lógica de supergfxctl con asusctl o system76-power. Para una nueva herramienta (p. ej. otra CLI), añadir un nuevo slice: `features/nombre_tool/` con su `cli.py` y su(s) página(s).

2. **Nomenclatura y estilo**  
   - Código en inglés (nombres de módulos, clases, funciones, variables).  
   - Textos visibles al usuario en español.  
   - Estilo de código coherente con el existente (PEP 8 recomendado); el proyecto no incluye aún formateador/linter obligatorio en CI.

3. **Capas**  
   - **UI** (páginas, contenedores): solo construyen widgets y llaman a casos de uso o a `cli`.  
   - **Casos de uso** (si existen): orquestan y devuelven datos; no importar PyQt.  
   - **Infraestructura** (`cli.py`): solo subprocesos o llamadas a binarios del sistema.

4. **Nuevas funcionalidades**  
   - Si es una nueva herramienta del sistema: nuevo slice en `features/<nombre>/` con `cli.py` y página(s).  
   - Si es una nueva “pantalla” de una herramienta ya integrada (p. ej. asusctl): nueva página en `features/asusctl/pages/` y, si hace falta, nuevo caso de uso en `use_cases/`, y enlace desde el contenedor (submenú + stack).

5. **Commits y ramas**  
   - Mensajes de commit claros (qué cambia y por qué).  
   - Para cambios grandes, usar ramas (p. ej. `feature/nombre` o `fix/descripcion`) y proponer merge a la rama principal tras revisión.

6. **Documentación**  
   - Actualizar este README si se añaden requisitos, pasos de instalación o nuevas secciones de la app.  
   - Comentarios en código para lógica no obvia; docstrings en módulos y funciones públicas.

7. **Compatibilidad**  
   - Mantener soporte para Python 3.10+ y PyQt6 ≥ 6.6.0.  
   - Probar en al menos un entorno Linux (X11 o Wayland) si es posible.

Siguiendo esta estructura y normas se facilita el mantenimiento y que varias personas colaboren sin pisar funcionalidades ajenas.
