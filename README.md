# AsusControl

Aplicación de escritorio en Python con PyQt6 para administrar **supergfxctl**, **asusctl** y **system76-power** en portátiles ASUS y System76/Pop!_OS (modos de gráficos, perfiles de energía, batería). Pensada para empaquetar como ejecutable en Ubuntu, Fedora y Debian.

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

### Instalación desde el código fuente

**1. Clonar e ingresar al proyecto**

```bash
git clone https://github.com/<tu-usuario>/AsusControl.git
cd AsusControl
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

Si descargaste un release (por ejemplo `AsusControl-1.0.0-linux-x86_64.tar.gz`):

```bash
tar xzf AsusControl-1.0.0-linux-x86_64.tar.gz
./AsusControl
```

Para tener el ejecutable en el PATH:

```bash
mv AsusControl ~/.local/bin/
# o: sudo mv AsusControl /usr/local/bin/
```

Luego puedes ejecutar desde cualquier terminal: `AsusControl`.

---

## Qué necesita el proyecto para funcionar

1. **Entorno Python**: Python 3.10+ con el venv activado y `pip install -r requirements.txt` ejecutado.
2. **Display**: sesión gráfica (X11 o Wayland). No está pensada para servidor headless.
3. **Permisos**: las herramientas (`supergfxctl`, `asusctl`, `system76-power`) pueden requerir usuario en ciertos grupos o `sudo` según la distro; la app solo las invoca por CLI.
4. **Opcional en X11**: `libxcb-cursor0` para el plugin Qt xcb si aparece el error relacionado con «xcb-cursor».

No se necesitan variables de entorno obligatorias; opcionalmente en Wayland puedes forzar: `QT_QPA_PLATFORM=wayland python main.py`.

---

## Desarrollo

### Estructura del proyecto

El código sigue una arquitectura **Clean** con **vertical slices** y nombres que dejan claro el propósito de cada parte (**screaming architecture**).

```
AsusControl/
├── main.py                 # Punto de entrada; aplica tema y lanza MainWindow
├── requirements.txt        # PyQt6
├── README.md
├── .gitignore
└── src/
    ├── app/                # Shell de la aplicación
    │   ├── main_window.py  # Ventana principal, barra lateral, scroll, tema
    │   ├── sidebar.py      # Menú lateral (Supergfxctl, Asusctl, System76-power)
    │   └── theme.py        # Tema claro/oscuro (QSS), sin dependencias extra
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

- **app/**: composición global, barra lateral, tema y scroll del contenido.
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
