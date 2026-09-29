"""Ejemplo sencillo de uso de las clases del Hito 1."""

from control_pid import ControladorPID, PlantaMotor, Sensor, SistemaLazoCerrado


motor = PlantaMotor("MOTOR-01", 3000.0, 24.0, 0.5)
sensor = Sensor("SENSOR-01")
controlador = ControladorPID("PID-01", 0.02, 0.03, 0.0001, 24.0)

sistema = SistemaLazoCerrado(controlador, motor, sensor)
sistema.set_velocidad_deseada(1500.0)

for _ in range(1000):
    estado = sistema.ejecutar_paso(0.01)

print("Simulación terminada")
print(f"Referencia: {estado['velocidad_deseada']:.2f} RPM")
print(f"Velocidad: {estado['velocidad_motor']:.2f} RPM")
print(f"Voltaje: {estado['voltaje']:.2f} V")


