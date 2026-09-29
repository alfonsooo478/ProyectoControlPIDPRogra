# Control PID de velocidad para un motor DC — Hito 1

Este proyecto contiene únicamente la arquitectura orientada a objetos pedida
para la primera entrega de la opción **Control Automático**.

## Archivos Python

```text
control_pid_motor_dc_hito1/
├── control_pid.py
└── main.py
```

- `control_pid.py` contiene todas las clases y la herencia.
- `main.py` crea los objetos y ejecuta un ejemplo sencillo.

No se utilizan librerías externas. Tampoco se incluyen `deque`, recursividad,
análisis Big-O, ruido, NumPy ni gráficos, porque corresponden a entregas
posteriores.

## Clases

- `ComponenteControl`: clase padre que guarda el identificador común.
- `ControladorPID`: calcula un voltaje a partir del error de velocidad.
- `PlantaMotor`: mantiene privada la velocidad y modela su cambio gradual.
- `Sensor`: mide la velocidad actual.
- `SistemaLazoCerrado`: contiene y coordina los tres componentes.

La velocidad del motor se guarda como `__velocidad_actual`. No existe un setter
para modificarla directamente; solo cambia mediante `aplicar_voltaje()`.

## Cómo ejecutarlo

Abre PowerShell y escribe:

```powershell
cd "C:\Users\alfon\OneDrive\Escritorio\PrograAvanzadaresumen\control_pid_motor_dc_hito1"
python main.py
```

No es necesario instalar paquetes.

## Material de presentación

La carpeta `presentacion` contiene el PDF y el PowerPoint editable. El diagrama
UML también está disponible en `docs/diagrama_clases.md`.

