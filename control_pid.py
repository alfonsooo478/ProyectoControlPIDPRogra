"""Clases del Hito 1 para controlar la velocidad de un motor DC."""


class ComponenteControl:
    """Representa un componente con un identificador.

    Atributos:
        identificador (str): Nombre o código del componente.
    """

    def __init__(self, identificador: str) -> None:
        """Inicializa el componente.

        Args:
            identificador (str): Nombre o código del componente.
        """
        self.identificador = identificador


class ControladorPID(ComponenteControl):
    """Calcula el voltaje necesario para controlar el motor.

    Atributos:
        kp (float): Ganancia proporcional.
        ki (float): Ganancia integral.
        kd (float): Ganancia derivativa.
        voltaje_maximo (float): Límite de salida en Volts.
        error_acumulado (float): Suma temporal de los errores.
        error_anterior (float): Error de la iteración anterior.
    """

    def __init__(  self, identificador: str, kp: float, ki: float, kd: float, voltaje_maximo: float) -> None:
        """Inicializa las ganancias y la memoria del controlador.

        Args:
            identificador (str): Código del controlador.
            kp (float): Ganancia proporcional.
            ki (float): Ganancia integral.
            kd (float): Ganancia derivativa.
            voltaje_maximo (float): Límite de salida en Volts.
        """
        super().__init__(identificador)
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.voltaje_maximo = voltaje_maximo
        self.error_acumulado = 0.0
        self.error_anterior = 0.0

    def calcular_accion(
        self,
        velocidad_deseada: float,
        velocidad_medida: float,
        paso_tiempo: float,
    ) -> float:
        """Calcula el voltaje a partir del error de velocidad.

        Args:
            velocidad_deseada (float): Referencia en RPM.
            velocidad_medida (float): Lectura del sensor en RPM.
            paso_tiempo (float): Intervalo de simulación en segundos.

        Returns:
            float: Voltaje limitado que se aplicará al motor.
        """
        error = velocidad_deseada - velocidad_medida
        self.error_acumulado += error * paso_tiempo
        derivada = (error - self.error_anterior) / paso_tiempo

        voltaje = (
            self.kp * error
            + self.ki * self.error_acumulado
            + self.kd * derivada
        )

        if voltaje > self.voltaje_maximo:
            voltaje = self.voltaje_maximo
        elif voltaje < -self.voltaje_maximo:
            voltaje = -self.voltaje_maximo

        self.error_anterior = error
        return voltaje


class PlantaMotor(ComponenteControl):
    """Representa un motor cuya velocidad cambia progresivamente.

    La velocidad actual es privada y no tiene un método setter. Solamente puede
    cambiar cuando se aplica un voltaje durante un intervalo de tiempo.

    Atributos:
        velocidad_maxima (float): Velocidad máxima en RPM.
        voltaje_maximo (float): Voltaje máximo en Volts.
        constante_tiempo (float): Medida simplificada de la inercia en segundos.
        __velocidad_actual (float): Velocidad privada del rotor en RPM.
    """

    def __init__(
        self,
        identificador: str,
        velocidad_maxima: float,
        voltaje_maximo: float,
        constante_tiempo: float,
    ) -> None:
        """Inicializa el motor detenido.

        Args:
            identificador (str): Código del motor.
            velocidad_maxima (float): Velocidad máxima en RPM.
            voltaje_maximo (float): Voltaje máximo en Volts.
            constante_tiempo (float): Inercia simplificada en segundos.
        """
        super().__init__(identificador)
        self.velocidad_maxima = velocidad_maxima
        self.voltaje_maximo = voltaje_maximo
        self.constante_tiempo = constante_tiempo
        self.__velocidad_actual = 0.0

    def get_velocidad_actual(self) -> float:
        """Obtiene la velocidad actual del motor.

        Returns:
            float: Velocidad del rotor en RPM.
        """
        return self.__velocidad_actual

    def aplicar_voltaje(
        self, voltaje: float, paso_tiempo: float
    ) -> float:
        """Aplica un voltaje y actualiza gradualmente la velocidad.

        Args:
            voltaje (float): Acción de control en Volts.
            paso_tiempo (float): Intervalo de simulación en segundos.

        Returns:
            float: Nueva velocidad del motor en RPM.
        """
        if voltaje > self.voltaje_maximo:
            voltaje = self.voltaje_maximo
        elif voltaje < -self.voltaje_maximo:
            voltaje = -self.voltaje_maximo

        velocidad_objetivo = (
            voltaje / self.voltaje_maximo * self.velocidad_maxima
        )
        factor_inercia = paso_tiempo / self.constante_tiempo

        if factor_inercia > 0.5:
            factor_inercia = 0.5

        cambio = factor_inercia * (
            velocidad_objetivo - self.__velocidad_actual
        )
        self.__velocidad_actual += cambio
        return self.__velocidad_actual


class Sensor(ComponenteControl):
    """Representa el sensor que mide la velocidad del motor.

    Atributos:
        ultima_medicion (float): Lectura más reciente en RPM.
    """

    def __init__(self, identificador: str) -> None:
        """Inicializa el sensor sin mediciones.

        Args:
            identificador (str): Código del sensor.
        """
        super().__init__(identificador)
        self.ultima_medicion = 0.0

    def medir(self, velocidad_real: float) -> float:
        """Mide la velocidad real del motor.

        Args:
            velocidad_real (float): Velocidad del motor en RPM.

        Returns:
            float: Velocidad medida en RPM.
        """
        self.ultima_medicion = velocidad_real
        return self.ultima_medicion


class SistemaLazoCerrado:
    """Contiene y coordina el controlador, el motor y el sensor.

    Atributos:
        controlador (ControladorPID): Controlador del sistema.
        motor (PlantaMotor): Planta que se desea controlar.
        sensor (Sensor): Sensor de velocidad.
        velocidad_deseada (float): Referencia de velocidad en RPM.
    """

    def __init__(
        self,
        controlador: ControladorPID,
        motor: PlantaMotor,
        sensor: Sensor,
    ) -> None:
        """Conecta los tres componentes del lazo.

        Args:
            controlador (ControladorPID): Controlador PID.
            motor (PlantaMotor): Motor DC.
            sensor (Sensor): Sensor de velocidad.
        """
        self.controlador = controlador
        self.motor = motor
        self.sensor = sensor
        self.velocidad_deseada = 0.0

    def set_velocidad_deseada(self, velocidad: float) -> None:
        """Define la velocidad que debe alcanzar el motor.

        Args:
            velocidad (float): Referencia en RPM.
        """
        self.velocidad_deseada = velocidad

    def ejecutar_paso(self, paso_tiempo: float) -> dict:
        """Ejecuta una iteración completa del lazo cerrado.

        Args:
            paso_tiempo (float): Intervalo de simulación en segundos.

        Returns:
            dict: Referencia, medición, voltaje y velocidad resultante.
        """
        velocidad_medida = self.sensor.medir(
            self.motor.get_velocidad_actual()
        )
        voltaje = self.controlador.calcular_accion(
            self.velocidad_deseada,
            velocidad_medida,
            paso_tiempo,
        )
        nueva_velocidad = self.motor.aplicar_voltaje(
            voltaje, paso_tiempo
        )

        return {
            "velocidad_deseada": self.velocidad_deseada,
            "velocidad_medida": velocidad_medida,
            "voltaje": voltaje,
            "velocidad_motor": nueva_velocidad,
        }

