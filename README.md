# Control PID de velocidad para un motor DC — Hito 1

Proyecto de **EL4203 — Programación Avanzada** basado en la opción B de la
pauta: **Control Automático (Lazo PID de Motor DC)**.

El objetivo de esta primera entrega es representar mediante programación
orientada a objetos los componentes físicos de un lazo de control de velocidad:
un controlador PID, un motor DC, un sensor y una clase que coordina el sistema.
El modelo es intencionalmente sencillo, porque el Hito 1 evalúa principalmente
clases, herencia, composición y encapsulamiento.

## Estado del proyecto

Actualmente el proyecto permite:

- crear un controlador PID con ganancias proporcional, integral y derivativa;
- representar un motor DC con velocidad interna privada e inercia simplificada;
- medir la velocidad mediante un sensor ideal;
- conectar los componentes dentro de un sistema de lazo cerrado;
- definir una velocidad de referencia;
- ejecutar una simulación básica de 500 pasos; y
- mostrar la referencia, la velocidad final y el voltaje aplicado.

No se utilizan librerías externas. Las extensiones exigidas para los Hitos 2 y
3 se describen en [Trabajo futuro](#trabajo-futuro), pero todavía no forman
parte del código.

## Requisitos del Hito 1 cubiertos

Según la pauta del proyecto, la opción de control PID exige para el Hito 1:

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

```text
control_pid_motor_dc_hito1/
├── .gitignore
├── control_pid.py
├── main.py
├── README.md
├── informe_hito1.tex
├── informe_hito1.pdf
├── Control PID de velocidad.pdf
├── Guia_estudio_y_guion_PID_Hito1.html
├── Guia_estudio_y_guion_PID_Hito1.pdf
├── docs/
│   └── diagrama_clases.md
└── presentacion/
    ├── Presentacion_Control_PID_Hito1.pptx
    ├── output.pptx
    └── narrative_plan.md
```

Además, pueden aparecer las carpetas `__pycache__/` y `tmp/`. Ambas contienen
archivos generados automáticamente y no son necesarias para ejecutar el
programa. `__pycache__/` ya está incluida en `.gitignore`.

### Archivos principales

- `control_pid.py`: contiene todas las clases, sus atributos, métodos,
  docstrings y relaciones de herencia.
- `main.py`: configura los objetos y ejecuta el ejemplo de cinco segundos.
- `docs/diagrama_clases.md`: contiene el diagrama UML en formato Mermaid.
- `informe_hito1.tex`: informe editable en LaTeX, con marco teórico,
  arquitectura, métodos, resultados, espacios para diagramas y trabajo futuro.
- `informe_hito1.pdf`: vista compilada del informe LaTeX.
- `Control PID de velocidad.pdf`: presentación utilizada para la defensa.
- `Guia_estudio_y_guion_PID_Hito1.pdf`: explicación del código y guion de
  apoyo para la presentación.
- `presentacion/`: contiene la presentación editable y su planificación.

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

## Flujo de control

```text
Referencia de velocidad
         ↓
Medición del sensor
         ↓
Cálculo del error y acción PID
         ↓
Limitación del voltaje
         ↓
Actualización progresiva del motor
         └──────── vuelve a la medición
```

La simulación es de lazo cerrado porque la velocidad obtenida vuelve a medirse
y se utiliza en la siguiente acción de control.

## Parámetros del ejemplo

| Parámetro | Valor |
|---|---:|
| Velocidad máxima del motor | 3000 RPM |
| Voltaje máximo | 24 V |
| Constante de tiempo | 0.5 s |
| Ganancia proporcional `kp` | 0.02 |
| Ganancia integral `ki` | 0.03 |
| Ganancia derivativa `kd` | 0.001 |
| Referencia | 1500 RPM |
| Paso de simulación | 0.01 s |
| Cantidad de pasos | 500 |
| Tiempo total simulado | 5 s |

## Cómo ejecutar

Se requiere Python 3. No es necesario instalar paquetes adicionales.

Desde PowerShell:

```powershell
cd "C:\Users\alfon\OneDrive\Escritorio\PrograAvanzadaresumen\control_pid_motor_dc_hito1"
python main.py
```

Salida actual:

```text
Simulación terminada
Referencia: 1500.00 RPM
Velocidad: 1499.93 RPM
Voltaje: 12.00 V
```

La velocidad final queda muy cerca de la referencia. El voltaje se aproxima a
12 V porque, en este modelo lineal, 1500 RPM corresponde a la mitad de la
velocidad máxima de 3000 RPM y, por tanto, aproximadamente a la mitad de 24 V.

## Diagramas y presentación

El UML editable se encuentra en `docs/diagrama_clases.md`. Puede abrirse en un
editor compatible con Mermaid, como Mermaid Live Editor, copiando únicamente
el contenido que comienza con `classDiagram`.

Para la defensa oral debe utilizarse el UML y el diagrama de flujo, evitando
mostrar capturas o bloques de código Python, tal como indica la pauta.

## Limitaciones actuales

Este Hito 1 usa un modelo académico simplificado:

- el sensor es ideal y todavía no incorpora ruido;
- el motor se representa mediante una dinámica de primer orden simplificada;
- no existe todavía un buffer histórico de tamaño fijo;
- no se ha implementado una función recursiva;
- no se incluye análisis Big-O;
- no hay vectorización con NumPy; y
- no se generan todavía gráficos bajo formato IEEE.

Estas limitaciones son coherentes con el alcance de la primera entrega.

## Trabajo futuro

### Hito 2 — Algoritmia, TDA y Big-O

- incorporar una cola FIFO de tamaño fijo mediante `collections.deque` para el
  historial de errores;
- implementar una función recursiva pertinente, por ejemplo un suavizado o una
  media ponderada del historial;
- comparar formalmente `deque.popleft()`, de costo O(1), con `list.pop(0)`, de
  costo O(n);
- documentar el análisis de complejidad; y
- desarrollar las mejoras en ramas independientes y fusionarlas posteriormente.

### Hito 3 — NumPy y gráficos IEEE

- vectorizar con NumPy la simulación de perturbaciones y ruido gaussiano;
- evitar ciclos explícitos en los cálculos numéricos centrales;
- generar la respuesta al escalón con referencia y velocidad real;
- exportar el gráfico en PDF o PNG con grilla, unidades, leyenda y caption
  inferior, sin título superior;
- revisar el cumplimiento de PEP8; y
- preparar una ejecución en vivo sin dependencias rotas.

## Repositorio GitHub

Enlace del repositorio:

**Pendiente de reemplazar:** `https://github.com/USUARIO/REPOSITORIO`

Antes de entregar, reemplazar el texto anterior por la dirección real del
repositorio y comprobar que el docente tenga acceso.

## Autor

- Alfonso Gómez
