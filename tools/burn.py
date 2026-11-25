import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Укажите путь к GeoTIFF BurnDate слоя
burn_date_path = "bmap2.tif"
output_png = "burned_area_map.png"

# Цветовая карта
cmap = plt.cm.get_cmap("hot", 256)

# Загрузка растра
with rasterio.open(burn_date_path) as src:
    burn_data = src.read(1)  # 2D-массив с BurnDate
    profile = src.profile
    transform = src.transform

print(burn_data.shape[:2])
# Маска сгоревших пикселей (BurnDate > 0)
burn_mask = burn_data > 0
burn_data_masked = np.ma.masked_where(~burn_mask, burn_data)

# Подсчет сгоревших пикселей
num_burned_pixels = np.sum(burn_mask)
print(f"Сгоревших пикселей: {num_burned_pixels}")

# Поиск самого раннего пикселя
if num_burned_pixels > 0:
    min_burn_day = np.min(burn_data[burn_mask])
    min_coords = np.argwhere(burn_data == min_burn_day)[0]  # первая пара (строка, столбец)
    row, col = min_coords
    print(f"Самый ранний пожар: день {min_burn_day}, координаты: ({row}, {col})")
else:
    print("Нет сгоревших пикселей в этом файле.")

# Отрисовка
plt.figure(figsize=(10, 8))
img = plt.imshow(burn_data_masked, cmap=cmap, vmin=1, vmax=366)
plt.title("MODIS Burn Date (MCD64A1)")
plt.colorbar(img, label="Day of Year Burned")
plt.axis('off')

# Сохранение PNG
plt.savefig(output_png, bbox_inches='tight', dpi=300)
plt.show()