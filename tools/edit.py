import rasterio
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from rasterio.features import geometry_mask

# Путь к исходному и выходному файлу
input_tif = "bmap1.tif"
output_tif = "bmap1_clean.tif"

# Загружаем растр
with rasterio.open(input_tif) as src:
    burn_data = src.read(1)
    transform = src.transform
    meta = src.meta.copy()

# Визуализация + ручной ввод полигона
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title("Нарисуй полигоны — области, которые нужно удалить\n(двойной клик = завершение)")
image = ax.imshow(burn_data, cmap='hot', vmin=1, vmax=366)

# Хранилище полигонов
polygons = []

def onclick(event):
    if event.dblclick:
        # Завершаем текущий полигон
        global poly
        if len(poly) >= 3:
            polygons.append(Polygon(poly))
            ax.plot(*zip(*poly), color='cyan', linewidth=2)
            fig.canvas.draw()
        poly = []
    else:
        # Добавляем точку
        x, y = int(event.xdata), int(event.ydata)
        poly.append((x, y))
        ax.plot(x, y, 'bo')
        fig.canvas.draw()

poly = []
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
fig.canvas.mpl_disconnect(cid)

# Преобразуем пиксельные координаты в географические
shapes = []
for poly in polygons:
    geo_coords = [rasterio.transform.xy(transform, y, x, offset='center') for x, y in poly.exterior.coords]
    shapes.append(Polygon(geo_coords))

# Создаем маску — True там, где нужно стереть
mask = geometry_mask(shapes, invert=True, transform=transform,
                     out_shape=burn_data.shape)

# Обнуляем значения внутри выделенных вручную полигонов
burn_data[mask] = 0

# Сохраняем результат
with rasterio.open(output_tif, 'w', **meta) as dst:
    dst.write(burn_data, 1)

print(f"✅ Сохранено: {output_tif}")