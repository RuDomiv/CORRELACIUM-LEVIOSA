from machine import Pin, I2C, Timer
import time

# Configuración del bus I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # GP0=SDA, GP1=SCL
ADXL345_ADDRESS = 0x53  # Dirección I2C del ADXL345

# Tamaño del buffer
BUFFER_SIZE = 100

# Inicializar las listas de datos con ceros
x_ref = [0.0] * BUFFER_SIZE
y_ref = [0.0] * BUFFER_SIZE
z_ref = [0.0] * BUFFER_SIZE

# Estado de recolección de datos
collecting_data = False
sample_count = 0

# Definir el pulsador en el pin GP2
button_pin = Pin(2, Pin.IN, Pin.PULL_UP)  # Configurar GP2 como entrada con pull-up interno
button_pressed = False

# Función para escribir un byte en un registro específico del ADXL345
def write_register(register, value):
    try:
        i2c.writeto_mem(ADXL345_ADDRESS, register, bytearray([value]))
    except Exception as e:
        print(f"Error al escribir en el registro {register:#04x}: {e}")

# Inicialización del ADXL345 con escala ±2g
def init_adxl345():
    print("Inicializando el ADXL345...")
    write_register(0x2D, 0x08)  # Activar el modo de medición
    write_register(0x31, 0x08)  # Configurar rango a ±2g

# Leer dos bytes de un registro (para los ejes X, Y, Z)
def read_axis_data(register):
    try:
        data = i2c.readfrom_mem(ADXL345_ADDRESS, register, 2)
        value = (data[1] << 8) | data[0]  # Combinar los bytes
        if value & 0x8000:  # Ajustar si es un valor negativo
            value -= 65536
        return value
    except Exception as e:
        print(f"Error al leer del registro {register:#04x}: {e}")
        return 0  # Retorna 0 en caso de error

# Convertir valor bruto a aceleración en m/s² con ±2g de rango
def convert_to_acceleration(raw_value):
    return (raw_value * 19.6) / 512

# Función para guardar los datos en un archivo .txt
def save_data_to_file():
    global x_ref, y_ref, z_ref
    try:
        with open('accelerometer_data.txt', 'w') as f:
            # Escribir x_ref
            f.write('x_ref = [\n')
            for i in range(BUFFER_SIZE):
                f.write(f"    {x_ref[i]:.3f},\n")
            f.write(']\n\n')

            # Escribir y_ref
            f.write('y_ref = [\n')
            for i in range(BUFFER_SIZE):
                f.write(f"    {y_ref[i]:.3f},\n")
            f.write(']\n\n')

            # Escribir z_ref
            f.write('z_ref = [\n')
            for i in range(BUFFER_SIZE):
                f.write(f"    {z_ref[i]:.3f},\n")
            f.write(']\n')

        print("Datos guardados en accelerometer_data.txt")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

# Inicializar el acelerómetro
init_adxl345()

# Función callback que se llamará cada 10 ms para una frecuencia de muestreo de 100 Hz
def sample_callback(timer):
    global collecting_data, sample_count, x_ref, y_ref, z_ref
    if collecting_data:
        try:
            # Leer datos del acelerómetro
            x_raw = read_axis_data(0x32)  # Eje X
            y_raw = read_axis_data(0x34)  # Eje Y
            z_raw = read_axis_data(0x36)  # Eje Z

            # Convertir las lecturas a m/s²
            x_accel = convert_to_acceleration(x_raw)
            y_accel = convert_to_acceleration(y_raw)
            z_accel = convert_to_acceleration(z_raw)

            # Guardar la lectura en el arreglo correspondiente con tres decimales
            if sample_count < BUFFER_SIZE:
                x_ref[sample_count] = round(x_accel, 3)
                y_ref[sample_count] = round(y_accel, 3)
                z_ref[sample_count] = round(z_accel, 3)
                sample_count += 1

                if sample_count % 10 == 0:
                    print(f"Muestras tomadas: {sample_count}/{BUFFER_SIZE}")

            if sample_count >= BUFFER_SIZE:
                collecting_data = False
                print("Recolección de datos completa.")
                save_data_to_file()

        except Exception as e:
            print(f"Error en sample_callback: {e}")

# Crear e iniciar un temporizador que llame al callback cada 10 ms para lograr 100 Hz
timer = Timer()
timer.init(period=10, mode=Timer.PERIODIC, callback=sample_callback)

print("Programa iniciado. Esperando pulsación del botón...")

# Bucle infinito para mantener el programa corriendo y detectar el pulsador
try:
    while True:
        button_state = button_pin.value()
        if button_state == 0 and not button_pressed:
            button_pressed = True
            if not collecting_data:
                collecting_data = True
                sample_count = 0
                # Reiniciar los arreglos de datos con ceros
                x_ref = [0.0] * BUFFER_SIZE
                y_ref = [0.0] * BUFFER_SIZE
                z_ref = [0.0] * BUFFER_SIZE
                print("Pulsador presionado, iniciando recolección de datos.")
        elif button_state == 1 and button_pressed:
            button_pressed = False
        # Descomenta la siguiente línea si deseas ver el estado del botón continuamente
        # print(f"Estado del botón: {button_state}")
        time.sleep(0.01)  # Pequeña pausa para evitar un bucle demasiado rápido
except Exception as e:
    print(f"Error en el bucle principal: {e}")
