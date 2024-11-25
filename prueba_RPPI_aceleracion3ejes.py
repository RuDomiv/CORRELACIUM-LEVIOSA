from machine import Pin, I2C, Timer
import time

# Configuración del bus I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Puerto 0: GP0=SDA, GP1=SCL
ADXL345_ADDRESS = 0x53  # Dirección I2C del ADXL345

# Tamaño del buffer circular
BUFFER_SIZE = 100

# Buffers circulares para almacenar las últimas 100 muestras de cada eje
x_buffer = [0] * BUFFER_SIZE
y_buffer = [0] * BUFFER_SIZE
z_buffer = [0] * BUFFER_SIZE

# Función para escribir un byte en un registro específico del ADXL345
def write_register(register, value):
    i2c.writeto_mem(ADXL345_ADDRESS, register, bytearray([value]))

# Inicialización del ADXL345 con escala ±2g
def init_adxl345():
    write_register(0x2D, 0x08)  # Activar el modo de medición
    write_register(0x31, 0x08)  # Configurar rango a ±2g

# Leer dos bytes de un registro (para los ejes X, Y, Z)
def read_axis_data(register):
    data = i2c.readfrom_mem(ADXL345_ADDRESS, register, 2)
    value = (data[1] << 8) | data[0]  # Combinar los bytes
    if value & 0x8000:  # Ajustar si es un valor negativo
        value -= 65536
    return value

# Convertir valor bruto a aceleración en m/s² con ±2g de rango
def convert_to_acceleration(raw_value):
    return (raw_value * 19.6) / 512

# Inicializar el acelerómetro
init_adxl345()

# Función callback que se llamará cada 10 ms para una frecuencia de muestreo de 100 Hz
def sample_callback(timer):
    # Leer datos del acelerómetro
    x_raw = read_axis_data(0x32)  # Eje X
    y_raw = read_axis_data(0x34)  # Eje Y
    z_raw = read_axis_data(0x36)  # Eje Z

    # Convertir las lecturas a m/s²
    x_accel = convert_to_acceleration(x_raw)
    y_accel = convert_to_acceleration(y_raw)
    z_accel = convert_to_acceleration(z_raw)

    # Actualizar el buffer circular y asegurar que mantenga BUFFER_SIZE elementos
    if len(x_buffer) >= BUFFER_SIZE:
        x_buffer.pop(0)
    if len(y_buffer) >= BUFFER_SIZE:
        y_buffer.pop(0)
    if len(z_buffer) >= BUFFER_SIZE:
        z_buffer.pop(0)

    # Añadir la nueva lectura al final del buffer
    x_buffer.append(x_accel)
    y_buffer.append(y_accel)
    z_buffer.append(z_accel)

    # Mostrar las lecturas actuales de aceleración
    print(f'Aceleración - X: {x_accel:.2f} m/s², Y: {y_accel:.2f} m/s², Z: {z_accel:.2f} m/s²')

# Crear e iniciar un temporizador que llame al callback cada 10 ms para lograr 100 Hz
timer = Timer()
timer.init(period=10, mode=Timer.PERIODIC, callback=sample_callback)

# Bucle infinito para mantener el programa corriendo
while True:
    pass  # Mantener el programa vivo para que el temporizador siga funcionando
