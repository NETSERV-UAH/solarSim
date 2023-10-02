import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2

# Parámetros del mapa
width = 1000  # Ancho del mapa
height = 1000  # Altura del mapa
scale = 100.0  # Escala del ruido
octaves = 6  # Número de octavas para el ruido de Perlin
persistence = 0.5  # Persistencia del ruido de Perlin
lacunarity = 2.0  # Lacunaridad del ruido de Perlin

# Generar el mapa de ruido de Perlin
world = np.zeros((height, width))
for y in range(height):
    for x in range(width):
        n = snoise2(x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=0)
        world[y][x] = n

# Función para asignar irradiancia solar en función del ruido de Perlin


def assign_irradiance(value):
    if value < -0.5:
        return 1000  # Irradiancia baja para áreas con ruido muy negativo
    elif value < 0.0:
        return 1500  # Irradiancia moderada para áreas con ruido negativo
    elif value < 0.5:
        return 2000  # Irradiancia alta para áreas con ruido positivo
    else:
        return 2500  # Irradiancia muy alta para áreas con ruido muy positivo


# Asignar valores de irradiancia solar al mapa de ruido de Perlin
irradiance_map = np.vectorize(assign_irradiance)(world)

# Crear la visualización del mapa ponderado
plt.figure(figsize=(10, 8))
plt.imshow(irradiance_map, cmap='viridis', extent=[0, width, 0, height])
plt.colorbar(label='Irradiancia Solar (W/m^2)')
plt.title('Mapa de Ruido de Perlin Ponderado con Irradiancia Solar')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
