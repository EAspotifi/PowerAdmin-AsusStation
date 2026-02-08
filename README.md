# AsusControl

Aplicación de escritorio en Python con PyQt6 para administrar **supergfxctl** y **asusctl** en portátiles ASUS (modos de gráficos, etc.). Pensada para empaquetar como ejecutable en Ubuntu, Fedora y Debian.

## Funcionalidad

- **Supergfxctl**: modos de gráficos (botones por modo, modo actual, cambio pendiente).
- **Asusctl**: al elegir Asusctl se despliega un submenú con **Información**, **Perfiles de rendimiento** y **Batería**; cada opción carga su pantalla.
- Barra lateral para cambiar entre Supergfxctl y Asusctl.
- Tema claro y oscuro (sin librerías externas, solo PyQt6).

## Requisitos

- Python 3.10+
- PyQt6
- supergfxctl (y servicio supergfxd) para la sección de modos de gráficos

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Arquitectura (Clean + Vertical Slice + Screaming)

Cada “feature” es un **vertical slice**: agrupa UI, casos de uso e infraestructura. Los nombres dejan claro qué hace cada parte.

```
src/
├── app/                        # Shell de la aplicación
│   ├── main_window.py          # Ventana principal, sidebar, stacked content
│   ├── sidebar.py              # Barra lateral (Supergfxctl | Asusctl)
│   └── theme.py                # Tema claro/oscuro (QSS, sin deps externas)
├── features/
│   ├── supergfxctl/            # Slice: modos de gráficos
│   │   ├── page.py             # UI de la página
│   │   └── cli.py              # Infraestructura: llamadas a supergfxctl
│   └── asusctl/                # Slice: asusctl (submenú + páginas)
│       ├── cli.py              # Infraestructura: asusctl info, battery, profile
│       ├── container.py        # Contenedor: submenú + stack de páginas
│       ├── use_cases/          # Casos de uso (orquestan lógica)
│       │   ├── info.py
│       │   ├── battery.py
│       │   └── profiles.py
│       └── pages/              # Una página por subsección
│           ├── info_page.py
│           ├── battery_page.py
│           └── profiles_page.py
└── __init__.py
```

- **app/**: composición de la app, navegación y tema.
- **features/*/use_cases/**: casos de uso que delegan en cli y devuelven datos a la UI.
- **features/*/pages/**: pantallas por subsección (Asusctl tiene 3).
- **features/*/cli.py**: adaptadores a herramientas externas (CLI).

Así se facilita añadir nuevas features, cambiar una sin tocar otras y preparar el empaquetado para Linux.

## Estructura del proyecto

```
AsusControl/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── src/
    ├── app/
    │   ├── main_window.py
    │   ├── sidebar.py
    │   └── theme.py
    └── features/
        ├── supergfxctl/
        │   ├── page.py
        │   └── cli.py
        └── asusctl/
            ├── cli.py
            ├── container.py
            ├── use_cases/
            │   ├── info.py
            │   ├── battery.py
            │   └── profiles.py
            └── pages/
                ├── info_page.py
                ├── battery_page.py
                └── profiles_page.py
```
