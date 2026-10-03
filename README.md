# Control PID de velocidad para un motor DC — Hito 1

## Estado del proyecto

Actualmente el proyecto permite:

- crear un controlador PID con ganancias proporcional, integral y derivativa;
- representar un motor DC con velocidad interna privada e inercia simplificada;
- medir la velocidad mediante un sensor ideal;
- conectar los componentes dentro de un sistema de lazo cerrado;
- definir una velocidad de referencia;
- ejecutar una simulación 
- mostrar la referencia, la velocidad final y el voltaje aplicado.

No se utilizan librerías externas. 

## Requisitos del Hito 1 


| Requisito | Implementación actual |
|---|---|
| Clases independientes | `ControladorPID`, `PlantaMotor` y `Sensor` |
| Herencia | Las tres clases heredan de `ComponenteControl` |
| Encapsulamiento | La velocidad del motor se guarda en `__velocidad_actual` |
| Cambio progresivo de velocidad | Solo se modifica mediante `aplicar_voltaje()` |
| Composición | `SistemaLazoCerrado` contiene un controlador, un motor y un sensor |
| Diagrama UML | Disponible en `docs/diagrama_clases.md` |
| Esqueleto funcional | `main.py` ejecuta una simulación completa y sencilla |

## Estructura de la carpeta

control_pid_motor_dc_hito1/
├── control_pid.py
├── main.py
├── README.md



### Archivos principales

- `control_pid.py`: contiene todas las clases, sus atributos, métodos,
  docstrings y relaciones de herencia.
- `main.py`: configura los objetos y ejecuta el ejemplo de cinco segundos.

## Arquitectura orientada a objetos

### `ComponenteControl`

Clase base que almacena el atributo común `identificador`. Su uso evita repetir
la misma inicialización en el controlador, el motor y el sensor.

### `ControladorPID`

Calcula el voltaje de control a partir de:

- el error actual entre referencia y medición;
- la acumulación temporal del error; y
- la variación del error respecto del paso anterior.

El método `calcular_accion()` limita el resultado al intervalo definido por
`voltaje_maximo`.

### `PlantaMotor`

Representa un modelo simplificado del motor DC. La velocidad se almacena en el
atributo privado `__velocidad_actual`, por lo que no se puede cambiar mediante
un setter público. El método `aplicar_voltaje()` actualiza la velocidad de forma
gradual considerando el voltaje, la velocidad máxima, el paso de tiempo y una
constante de tiempo que representa la inercia.

### `Sensor`

Representa un sensor ideal de velocidad. El método `medir()` recibe la velocidad
real del motor, guarda la lectura más reciente y la devuelve. El ruido de
medición corresponde a una etapa posterior del proyecto.

### `SistemaLazoCerrado`

Compone y coordina los tres elementos anteriores. Su método `ejecutar_paso()`
realiza una iteración completa:

1. mide la velocidad del motor;
2. calcula el voltaje con el PID;
3. aplica el voltaje al motor; y
4. devuelve el estado del sistema en un diccionario.


## Cómo ejecutar

Se requiere Python 3. No es necesario instalar paquetes adicionales.

Desde PowerShell:
primero ejecutar el archivo control_pid.py para luego ejecutar 
python main.py

Puede ser desde VisualCode y así simplemente colocar run en el archivo



## Limitaciones actuales

Este Hito 1 usa un modelo académico simplificado:

- el sensor es ideal y todavía no incorpora ruido;
- no se ha implementado una función recursiva;
- no se incluye análisis Big-O;
- no hay vectorización con NumPy; y
- no se generan todavía gráficos bajo formato IEEE.


