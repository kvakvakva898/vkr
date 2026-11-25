import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Patch

# --- Параметры файлов ---
land_cover_path = "map1.tif"    # Карта растительности
burn_date_path = "bmap1.tif"   # Карта пожаров

# --- Загрузка данных ---
def load_tif(file_path: str) -> np.ndarray:
    with rasterio.open(file_path) as src:
        return src.read(1)

land_cover = load_tif(land_cover_path)
burn_data = load_tif(burn_date_path)
burn_mask = burn_data > 0  # Сгоревшие пиксели

# --- Классы растительности MODIS ---
class_names = {
    1: "Вечнозелёные хвойные леса",
    2: "Вечнозелёные широколиственные леса",
    3: "Лиственные хвойные леса",
    4: "Лиственные широколиственные леса",
    5: "Смешанные леса",
    6: "Закрытые кустарниковые заросли",
    7: "Открытые кустарниковые заросли",
    8: "Древесные саванны",
    9: "Саванны",
    10: "Луга",
    11: "Водно-болотные угодья",
    12: "Сельскохозяйственные угодья",
    13: "Городские территории",
    14: "Мозаика сельхозугодий и природной растительности",
    15: "Снег и лёд",
    16: "Пустынные территории",
    17: "Водные объекты"
}

# --- Цветовая карта для растительности ---
land_cover_cmap = colors.ListedColormap([
    '#05450a', '#086a10', '#54a708', '#78d203', '#009900',
    '#c6b044', '#dcd159', '#dade48', '#fbff13', '#b6ff05',
    '#27ff87', '#c24f44', '#a5a5a5', '#ff6d4c', '#69fff8',
    '#f9ffa4', '#1c0dff'
])
bounds = np.arange(0.5, 18.5, 1)
norm = colors.BoundaryNorm(bounds, land_cover_cmap.N)

# --- Создание RGB-изображения из карты растительности ---
rgb_image = land_cover_cmap(norm(land_cover))
rgb_image[burn_mask] = [0, 0, 0, 0.37]  # Чёрный цвет RGBA для сгоревших пикселей

# --- Визуализация ---
fig, ax = plt.subplots(figsize=(15, 10))
ax.imshow(rgb_image)

# Легенда
unique_classes = np.unique(land_cover[~burn_mask])
legend_elements = [
    Patch(facecolor=land_cover_cmap(i - 1), label=f"{i}. {class_names[i]}")
    for i in unique_classes if i in class_names
]
legend_elements.append(Patch(facecolor='black', label="Сгоревшие территории"))

ax.legend(
    handles=legend_elements,
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    title="Типы растительности"
)

plt.axis('off')
plt.tight_layout()
plt.savefig("bmap.png", dpi=300, bbox_inches='tight')
plt.show()