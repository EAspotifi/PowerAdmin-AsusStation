# AsusControl

Aplicación de escritorio en Python con PyQt6 para administrar los modos de gráficos con **supergfxctl** en portátiles ASUS con GPU híbrida.

## Funcionalidad

- Obtiene los modos disponibles con `supergfxctl -s`
- Crea botones dinámicos por cada modo soportado
- Al seleccionar un modo, ejecuta `supergfxctl -m "modo"`
- Muestra el modo actual
- Botón para actualizar la lista de modos

## Requisitos

- Python 3.10+
- PyQt6
- supergfxctl instalado y el servicio `supergfxd` activo

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Estructura del proyecto

```
AsusControl/
├── main.py              # Punto de entrada
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── main_window.py   # Ventana principal con botones de modos
    └── supergfxctl.py   # Wrapper para comandos supergfxctl
```
