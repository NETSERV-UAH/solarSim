import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from noise import snoise2

# Parámetros del mapa
width = 800  # Ancho del mapa
height = 600  # Altura del mapa
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

# Crear una representación 3D del mapa
fig, ax = plt.subplots(subplot_kw={'projection': '3d'}, figsize=(10, 8))
X = np.arange(0, width, 1)
Y = np.arange(0, height, 1)
X, Y = np.meshgrid(X, Y)
Z = irradiance_map

# Configurar el mapa de colores en 3D
surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                       linewidth=0, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.set_title('Mapa de Ruido de Perlin Ponderado con Irradiancia Solar (3D)')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Irradiancia Solar (W/m^2)')

# Mostrar el mapa en 3D
plt.show()
