import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Patch

def load_land_cover_tif(file_path: str) -> np.ndarray:
    """Загружает TIFF-файл карты растительности."""
    with rasterio.open(file_path) as src:
        data = src.read(1)  # Читаем первый канал
        return data

def visualize_land_cover(data: np.ndarray, title: str = "Карта растительности"):
    """Визуализирует данные земного покрова с легендой."""
    # Классификация MODIS Land Cover Type 1 (IGBP)
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

    # Цвета для каждой категории
    cmap = colors.ListedColormap([
        '#05450a',   # 1. Evergreen Needleleaf Forests
        '#086a10',   # 2. Evergreen Broadleaf Forests
        '#54a708',   # 3. Deciduous Needleleaf Forests
        '#78d203',   # 4. Deciduous Broadleaf Forests
        '#009900',   # 5. Mixed Forests
        '#c6b044',   # 6. Closed Shrublands
        '#dcd159',   # 7. Open Shrublands
        '#dade48',   # 8. Woody Savannas
        '#fbff13',   # 9. Savannas
        '#b6ff05',   # 10. Grasslands
        '#27ff87',   # 11. Permanent Wetlands
        '#c24f44',   # 12. Croplands
        '#a5a5a5',   # 13. Urban
        '#ff6d4c',   # 14. Cropland/Natural Mosaic
        '#69fff8',   # 15. Snow/Ice
        '#f9ffa4',   # 16. Barren
        '#1c0dff'    # 17. Water Bodies
    ])

    # Нормализация для отображения
    bounds = np.arange(0.5, 18.5, 1)
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # Визуализация
    fig, ax = plt.subplots(figsize=(15, 10))
    img = ax.imshow(data, cmap=cmap, norm=norm)

    # Создание легенды
    legend_elements = [
        Patch(facecolor=cmap(i-1), label=f"{i}. {class_names[i]}") 
        for i in class_names if i in np.unique(data)
    ]
    
    ax.legend(
        handles=legend_elements,
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        title="Типы растительности"
    )

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("map.png", dpi=300, bbox_inches='tight')

    plt.show()


# Укажите путь к вашему TIFF-файлу
tif_file = "map1.tif"  # Замените на ваш файл
    
# Загрузка и визуализация
land_cover_data = load_land_cover_tif(tif_file)
visualize_land_cover(land_cover_data)