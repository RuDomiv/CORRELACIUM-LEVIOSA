from machine import Pin, I2C, Timer
import time
from ssd1306 import SSD1306_I2C

# Configuración del bus I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)  # Puerto 0: GP0=SDA, GP1=SCL
ADXL345_ADDRESS = 0x53  # Dirección I2C del ADXL345

# Configuración de la pantalla OLED
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Tamaño del buffer circular
BUFFER_SIZE = 100

# Matrices de referencia para los hechizos
# Hechizo Leviosa
x_ref_leviosa = [
    1.225, 1.723, 1.876, 2.373, 3.598, 2.182, 2.067, 1.914, 1.416, 0.880,
    0.077, -0.804, -1.110, -1.493, -1.608, -1.838, -1.608, -2.909, -2.641, -3.445,
    -3.407, -3.828, -3.981, -4.364, -4.747, -5.015, -5.091, -5.819, -6.623, -6.776,
    -7.235, -7.427, -7.580, -7.695, -8.001, -8.154, -8.498, -8.958, -9.264, -9.532,
    -9.379, -8.652, -7.848, -7.312, -7.312, -7.503, -7.771, -7.962, -8.269, -8.460,
    -8.613, -8.498, -8.230, -8.192, -8.154, -8.345, -8.537, -8.384, -7.541, -6.470,
    -5.627, -4.977, -4.249, -3.828, -3.139, -2.833, -2.450, -2.373, -2.335, -1.876,
    -1.723, -1.455, -1.148, -0.957, -0.612, -0.536, -0.345, -0.383, -0.459, -0.612,
    -0.766, -0.804, -1.225, -1.263, -1.263, -1.340, -1.455, -1.570, -1.608, -1.646,
    -1.531, -1.531, -1.378, -1.302, -1.072, -0.880, -0.689, -0.345, 0.038, 0.230,
]
y_ref_leviosa = [
    3.790, 3.790, 3.062, 2.795, 5.398, 3.139, 2.527, 2.488, 2.986, 3.905,
    3.866, 2.795, 3.062, 3.637, 3.139, 3.024, 2.756, 3.407, 2.335, 1.876,
    0.574, -1.072, -2.297, -3.484, -4.058, -4.938, -6.355, -5.972, -5.436, -4.938,
    -4.709, -5.130, -5.091, -4.862, -3.943, -2.680, -1.378, 0.077, 1.302, 3.484,
    5.053, 6.355, 6.623, 5.321, 5.321, 5.321, 5.742, 6.623, 7.771, 9.762,
    12.020, 14.164, 16.384, 17.035, 17.227, 16.423, 15.159, 14.355, 13.437, 13.322,
    13.666, 12.977, 12.212, 11.867, 10.680, 9.188, 7.848, 7.159, 6.508, 5.551,
    4.938, 4.747, 4.096, 3.522, 2.641, 1.876, 1.110, 0.191, -0.115, -0.268,
    -0.612, -1.263, -1.570, -2.220, -2.871, -3.292, -3.752, -4.134, -4.134, -4.020,
    -3.637, -3.598, -3.598, -3.752, -3.905, -3.981, -4.096, -4.020, -3.637, -3.024,
]
z_ref_leviosa = [
    9.226, 9.532, 9.034, 7.465, 9.609, 5.283, 3.101, 2.450, 2.756, 3.828,
    5.436, 3.981, 2.105, 2.718, 2.450, 1.416, 2.297, 3.943, 4.249, 5.436,
    5.513, 3.752, 2.297, 3.560, 3.752, 5.359, 8.230, 8.728, 11.025, 14.241,
    16.270, 17.418, 19.026, 19.562, 19.562, 19.562, 19.409, 18.184, 16.844, 16.461,
    17.456, 17.916, 19.370, 19.026, 16.346, 14.623, 14.623, 13.934, 13.628, 13.360,
    13.628, 15.236, 18.145, 19.562, 18.643, 15.389, 11.523, 8.613, 7.848, 7.273,
    6.661, 6.355, 6.316, 5.780, 5.857, 6.776, 5.359, 3.024, 1.493, 1.263,
    1.531, 1.340, 1.531, 1.302, 1.570, 1.761, 1.263, 0.995, 0.842, 1.148,
    2.335, 3.330, 3.713, 5.168, 6.661, 7.159, 7.197, 7.312, 7.848, 8.613,
    9.570, 10.489, 10.604, 10.604, 10.336, 9.953, 9.494, 9.838, 10.221, 10.834,
]

# Hechizo Expelliarmus
x_ref_Expelliarmus = [
    -0.727, 7.235, -1.148, -1.761, -1.723, -1.723, -0.612, -1.455, -1.110, -1.263,
    -1.034, -1.110, -1.148, -1.072, -1.187, -1.302, -1.531, -1.531, -1.378, -1.263,
    -0.842, -0.459, -0.153, -0.115, -0.191, -0.498, -0.842, -0.995, -1.225, -1.646,
    -2.105, -2.144, -1.684, -1.263, -1.263, -0.995, -0.957, -0.498, -0.306, -0.191,
    -0.077, 0.038, -0.153, -0.077, -0.268, -0.383, -0.842, -1.148, -1.723, -2.259,
    -2.527, -2.756, -2.756, -2.603, -2.488, -1.952, -0.689, -0.077, 0.421, 0.268,
    0.919, 0.498, -0.306, -0.612, -1.110, -1.570, -1.952, -2.144, -2.565, -1.799,
    -1.570, -0.574, 1.072, 2.833, 2.373, 1.646, 1.493, 1.148, 0.766, 0.191,
    0.077, -0.230, -0.230, 0.191, 0.153, 0.230, 0.268, 0.306, 0.612, 0.612,
    0.498, 0.421, 0.498, 0.383, 0.268, 0.153, 0.077, 0.000, 0.000, -0.077,
]
y_ref_Expelliarmus = [
    -4.249, 1.225, -6.202, -7.541, -9.264, -8.690, -11.216, -10.451, -10.910, -11.867,
    -10.872, -10.987, -10.719, -10.030, -8.805, -7.962, -7.886, -7.312, -6.048, -5.053,
    -3.369, -0.919, 1.263, 2.833, 3.905, 5.627, 7.618, 9.685, 12.403, 13.743,
    13.016, 12.212, 11.293, 9.877, 8.920, 8.920, 9.111, 9.800, 9.800, 9.570,
    8.192, 7.044, 5.551, 4.900, 4.441, 4.058, 3.981, 4.938, 5.283, 5.206,
    5.206, 4.249, 3.560, 4.632, 3.177, -0.038, -0.383, -1.799, -1.838, -1.455,
    -1.531, -2.680, -3.445, -5.934, -6.661, -6.967, -4.670, -2.335, -0.574, -0.957,
    -2.718, -4.977, -6.202, -4.211, -1.187, 0.000, 0.077, 1.455, 2.718, 3.369,
    3.828, 3.713, 3.866, 3.866, 3.943, 3.445, 2.450, 1.646, 0.995, 0.651,
    0.268, -0.919, -0.804, -0.345, 0.038, 0.115, -0.191, 0.115, 0.153, 0.306,
]
z_ref_Expelliarmus = [
    10.336, 2.220, 10.374, 11.293, 10.221, 11.293, 10.795, 12.709, 10.757, 8.881,
    7.541, 8.307, 9.073, 9.034, 8.843, 9.647, 10.489, 10.183, 9.723, 9.341,
    8.460, 8.001, 9.073, 9.800, 8.920, 7.197, 6.202, 5.666, 5.742, 7.005,
    8.690, 8.307, 6.967, 6.278, 5.819, 5.130, 5.130, 5.551, 6.891, 6.814,
    6.202, 5.627, 4.211, 3.062, 3.484, 3.522, 2.373, 0.919, 0.651, -0.077,
    -1.952, -3.560, -5.206, -6.355, -5.283, -3.943, -5.168, -6.278, -5.780, -6.240,
    -7.120, -4.173, -0.498, 1.952, 4.441, 8.728, 14.432, 19.562, 19.562, 19.562,
    19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562,
    19.562, 19.562, 17.150, 16.002, 15.351, 14.164, 14.164, 12.671, 12.173, 11.791,
    10.527, 9.341, 8.920, 9.226, 8.881, 8.460, 9.073, 9.647, 9.877, 9.723,
    9.417, 8.958,
]

# Hechizo Lumos
x_ref_Lumos = [
    -2.948, -3.139, -10.642, -3.062, -3.024, -2.756, -3.024, -3.024, -4.096, -4.594, -4.632, 
    -5.666, -6.278, -7.082, -7.848, -8.537, -9.609, -10.068, -10.566, -11.178, -11.255, -10.451, 
    -9.723, -8.920, -7.120, -6.278, -5.398, -5.398, -5.666, -6.393, -6.738, -6.546, -6.738, 
    -5.972, -4.977, -3.828, -2.948, -2.833, -2.067, -1.991, -1.378, -0.957, -0.727, -0.038, 
    0.345, 0.306, 0.498, 0.919, 0.995, 0.727, -0.153, -0.612, -1.110, -1.110, -1.416, -0.880, 
    -0.574, -0.880, -1.187, -1.493, -1.952, -2.450, -2.488, -2.871, -2.756, -2.527, -2.641, 
    -2.756, -3.216, -3.024, -4.211, -5.091, -6.508, -6.316, -6.584, -6.316, -5.972, -4.862, 
    -4.402, -3.522, -3.139, -3.330, -3.024, -2.565, -2.412, -2.756, -3.062, -2.718, -2.603, 
    -2.335, -2.220, -2.105, -1.723, -2.603, -1.876, -1.723, -1.914, -1.914, -1.914, -1.761
]

y_ref_Lumos = [
    5.895, 4.900, 4.900, 3.828, 4.096, 4.555, 3.713, 2.641, 2.641, 1.034, 0.383, 1.646, 3.101, 
    3.828, 4.288, 4.823, 4.670, 5.168, 6.508, 8.575, 11.370, 12.020, 11.676, 10.642, 9.877, 
    9.685, 7.541, 5.398, 4.862, 4.785, 4.594, 5.627, 6.393, 6.967, 6.661, 6.546, 3.828, 1.034, 
    0.306, -0.612, -1.416, -2.412, -3.024, -2.067, -1.302, -2.373, -3.866, -4.364, -4.479, 
    -4.747, -5.245, -4.670, -3.713, -3.866, -3.866, -4.173, -4.134, -4.211, -4.900, -4.670, 
    -4.555, -4.900, -4.134, -3.139, -2.335, -1.531, 0.077, 0.842, 2.603, 5.704, 6.087, 5.780, 
    6.776, 9.111, 11.905, 13.475, 13.207, 13.245, 12.480, 12.403, 12.862, 12.480, 12.556, 
    11.638, 9.915, 8.001, 7.005, 7.159, 6.393, 6.087, 5.513, 4.823, 3.828, 2.909, 3.177, 3.790, 
    2.565, 2.412, 2.909, 2.909
]

z_ref_Lumos = [
    13.016, 13.896, 17.341, 14.968, 16.346, 17.150, 18.145, 19.562, 19.562, 19.562, 19.562, 
    19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 17.188, 
    12.671, 7.159, 2.641, 1.493, 0.574, -0.536, -1.148, -2.833, -5.551, -6.852, -9.494, -10.451, 
    -9.723, -8.996, -8.881, -7.771, -6.929, -6.010, -4.747, -5.474, -6.929, -6.776, -6.125, 
    -6.278, -6.393, -6.087, -6.316, -6.355, -6.967, -7.312, -7.005, -6.278, -6.278, -5.474, 
    -4.747, -4.517, -3.828, -3.254, -2.909, -3.254, -3.101, -2.565, -2.220, -2.412, -1.455, 
    -0.383, 3.407, 8.652, 13.475, 16.691, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 
    19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.179, 15.848, 13.207, 11.714, 
    11.714, 11.829, 11.331, 10.451, 9.800, 10.680, 10.030, 8.805, 7.809, 7.656, 7.848
]

x_ref_ExpectoPatronus = [
    -2.718, -3.177, -3.407, -3.292, -3.369, -2.795, -2.756, -2.603, -2.412, -2.565,
    -2.718, -2.986, -2.909, -3.062, -3.445, -3.866, -4.441, -4.632, -4.632, -4.709,
    -4.938, -4.938, -5.321, -6.202, -7.503, -8.345, -8.996, -9.494, -9.800, -9.953,
    -10.068, -10.145, -9.953, -9.838, -9.953, -9.647, -9.188, -8.537, -8.728, -8.192,
    -7.733, -7.159, -6.202, -6.202, -5.704, -5.627, -5.168, -4.900, -4.632, -4.364,
    -4.020, -3.675, -3.101, -2.795, -2.488, -2.488, -2.527, -2.565, -2.565, -2.412,
    -2.373, -2.220, -1.761, -1.531, -1.378, -1.378, -1.646, -1.646, -1.608, -1.799,
    -1.991, -2.259, -2.488, -2.565, -2.871, -3.560, -3.560, -3.330, -3.024, -2.641,
    -2.603, -2.603, -2.948, -3.177, -3.522, -4.096, -4.517, -4.862, -5.015, -4.862,
    -5.398, -5.245, -5.206, -4.900, -4.632, -5.206, -5.742, -6.125, -6.163, -6.010,
]

y_ref_ExpectoPatronus = [
    11.102, 11.829, 10.719, 13.130, 13.360, 14.164, 13.743, 13.552, 13.016, 12.059,
    11.331, 9.877, 9.341, 8.728, 8.498, 8.116, 7.618, 7.388, 7.273, 7.273, 6.240,
    5.742, 5.359, 4.670, 3.177, 2.067, 1.072, 0.306, -0.421, -1.072, -1.684,
    -2.373, -2.909, -3.177, -3.790, -4.479, -4.862, -5.053, -6.163, -5.742, -6.891,
    -7.044, -7.044, -7.312, -7.159, -6.393, -5.895, -5.666, -5.245, -4.823, -4.249,
    -4.058, -3.866, -3.828, -3.330, -2.986, -3.024, -2.527, -1.493, -0.957, -0.995,
    -0.727, -0.115, 0.153, 0.651, 1.110, 1.110, 1.991, 2.718, 3.637, 4.977,
    6.316, 7.924, 9.149, 10.106, 11.140, 11.791, 11.867, 13.092, 16.116, 18.605,
    19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562,
    19.562, 18.988, 17.686, 16.805, 16.767, 16.308, 15.887, 14.470, 12.595, 10.757,
]

z_ref_ExpectoPatronus = [
    1.072, 2.680, 6.508, 5.780, 5.895, 7.541, 8.537, 9.149, 10.757, 12.633, 13.475,
    15.504, 17.380, 19.179, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562,
    19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562, 19.562,
    19.562, 19.562, 19.562, 18.030, 16.614, 15.045, 13.245, 11.752, 10.757, 8.881,
    8.230, 6.814, 5.780, 4.555, 3.713, 2.450, 1.570, 0.306, -0.919, -1.914, -2.105,
    -2.335, -2.718, -2.565, -2.373, -2.220, -2.603, -3.062, -3.254, -3.560, -4.288,
    -4.823, -4.709, -4.670, -4.632, -4.249, -4.249, -4.249, -4.326, -4.326, -4.096,
    -3.981, -3.484, -2.527, -1.914, -1.608, -0.421, 0.191, 0.230, 0.191, 0.077, -0.383,
    -0.345, 0.230, 1.608, 3.637, 5.742, 7.235, 8.652, 10.183, 11.216, 12.671, 13.896,
    14.547, 13.781, 12.786, 12.824, 14.470, 16.346, 17.801
]



# Umbrales que se ajustan según las pruebas
UMBRAL_TOTAL_LEVIOSA = 9750
UMBRAL_TOTAL_Expelliarmus = 9500
UMBRAL_TOTAL_Lumos = 9500
UMBRAL_TOTAL_ExpectoPatronus = 9000
   


# Definimos los hechizos y sus referencias
hechizos = [
    {
        'nombre': 'Leviosa',
        'x_ref': x_ref_leviosa,
        'y_ref': y_ref_leviosa,
        'z_ref': z_ref_leviosa,
        'umbral_total': UMBRAL_TOTAL_LEVIOSA
    },
    {
        'nombre': 'Expelliarmus',
        'x_ref': x_ref_Expelliarmus,
        'y_ref': y_ref_Expelliarmus,
        'z_ref': z_ref_Expelliarmus,
        'umbral_total': UMBRAL_TOTAL_Expelliarmus
    },
    {
        'nombre': 'Lumos',
        'x_ref': x_ref_Lumos,
        'y_ref': y_ref_Lumos,
        'z_ref': z_ref_Lumos,
        'umbral_total': UMBRAL_TOTAL_Lumos
    },
    {
        'nombre': 'ExpectoPatronus',
        'x_ref': x_ref_ExpectoPatronus,
        'y_ref': y_ref_ExpectoPatronus,
        'z_ref': z_ref_ExpectoPatronus,
        'umbral_total': UMBRAL_TOTAL_ExpectoPatronus
    }
]

# Buffers circulares para almacenar las muestras
x_buffer = []
y_buffer = []
z_buffer = []

# Función para escribir un byte en un registro específico del ADXL345
def write_register(register, value):
    i2c.writeto_mem(ADXL345_ADDRESS, register, bytearray([value]))

# Inicialización del ADXL345 con escala ±2g
def init_adxl345():
    write_register(0x2D, 0x08)  # Activar el modo de medición
    write_register(0x31, 0x08)  # Configurar rango a ±2g y resolución completa

# Leer dos bytes de un registro (para los ejes X, Y, Z)
def read_axis_data(register):
    data = i2c.readfrom_mem(ADXL345_ADDRESS, register, 2)
    value = (data[1] << 8) | data[0]  # Combinar los bytes
    if value & 0x8000:  # Ajustar si es un valor negativo
        value -= 65536
    return value

# Convertir valor bruto a aceleración en m/s² con ±2g de rango
def convert_to_acceleration(raw_value):
    return (raw_value * 9.8) / 256  # Cada LSB equivale a 0.03828 m/s²

# Función de correlación cruzada
def cross_correlation(buffer, ref_vector):
    correlation_sum = 0
    for i in range(BUFFER_SIZE):
        correlation_sum += buffer[i] * ref_vector[i]
    return correlation_sum


def detectar_hechizo(hechizos):
    hechizo_detectado = None
    mayor_correlacion = 0

    for hechizo in hechizos:
        total_corr = abs(hechizo['correlacion']['x']) + abs(hechizo['correlacion']['y']) + abs(hechizo['correlacion']['z'])
        if total_corr > hechizo['umbral_total'] and total_corr > mayor_correlacion:
            mayor_correlacion = total_corr
            hechizo_detectado = hechizo['nombre']

    if hechizo_detectado:
        print(f"¡Hechizo {hechizo_detectado} detectado!")
        mostrar_hechizo(hechizo_detectado)  # Muestra el hechizo en la pantalla OLED
    else:
        print("No se detectó ningún hechizo.")


# Función para mostrar el último hechizo en la pantalla OLED
def mostrar_hechizo(nombre_hechizo):
    oled.fill(0)  # Limpia la pantalla
    oled.text("Ultimo Hechizo:", 0, 0)
    oled.text(nombre_hechizo, 0, 20)
    oled.show()



# Inicializar el acelerómetro
init_adxl345()

# Mensaje inicial en la pantalla OLED
oled.fill(0)
oled.text("Iniciando...", 0, 0)
oled.text("Esperando", 0, 20)
oled.text("hechizos...", 0, 40)
oled.show()

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

    # Actualizar los buffers circulares
    x_buffer.append(x_accel)
    y_buffer.append(y_accel)
    z_buffer.append(z_accel)

    # Mantener el tamaño del buffer
    if len(x_buffer) > BUFFER_SIZE:
        x_buffer.pop(0)
    if len(y_buffer) > BUFFER_SIZE:
        y_buffer.pop(0)
    if len(z_buffer) > BUFFER_SIZE:
        z_buffer.pop(0)

    # Calcular la correlación cruzada cuando los buffers estén llenos
    if len(x_buffer) == BUFFER_SIZE:
        for hechizo in hechizos:
            x_corr = cross_correlation(x_buffer, hechizo['x_ref'])
            y_corr = cross_correlation(y_buffer, hechizo['y_ref'])
            z_corr = cross_correlation(z_buffer, hechizo['z_ref'])

            hechizo['correlacion'] = {'x': x_corr, 'y': y_corr, 'z': z_corr}

        detectar_hechizo(hechizos)

# Crear e iniciar un temporizador que llame al callback cada 10 ms para lograr 100 Hz
timer = Timer()
timer.init(period=10, mode=Timer.PERIODIC, callback=sample_callback)

# Bucle infinito para mantener el programa corriendo
while True:
    pass  # Añadimos un pequeño delay para liberar recursos



