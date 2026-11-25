import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzyFireVizualizer:
    def __init__(self):
        # Инициализация переменных
        self.wind_speed = ctrl.Antecedent(np.arange(-31, 31, 1), 'Скорость ветра, м/с')
        self.humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'Влажность, %')
        self.burning_neighbors = ctrl.Antecedent(np.arange(0, 9, 1), 'Горящие соседи, шт.')
        self.temperature = ctrl.Antecedent(np.arange(-20, 51, 1), 'Температура, °C')
        self.fire_prob = ctrl.Consequent(np.arange(0, 101, 1), 'Вероятность возгорания, %')
        
        # Настройка функций принадлежности
        self._setup_membership_functions()
    
    def _setup_membership_functions(self):
        # Скорость ветра - 9 категорий
        self.wind_speed['Встречный шторм'] = fuzz.trapmf(self.wind_speed.universe, [-30, -30, -25, -22])
        self.wind_speed['Встречный сильный'] = fuzz.trapmf(self.wind_speed.universe, [-25, -22, -18, -15])
        self.wind_speed['Встречный умеренный'] = fuzz.trapmf(self.wind_speed.universe, [-18, -15, -12, -10])
        self.wind_speed['Встречный легкий'] = fuzz.trapmf(self.wind_speed.universe, [-12, -10, -5, -2])

        self.wind_speed['Слабый'] = fuzz.trapmf(self.wind_speed.universe, [-5, -2, 2, 5])

        self.wind_speed['Попутный слабый'] = fuzz.trapmf(self.wind_speed.universe, [2, 5, 10, 12])
        self.wind_speed['Попутный умеренный'] = fuzz.trapmf(self.wind_speed.universe, [10, 12, 15, 18])
        self.wind_speed['Попутный сильный'] = fuzz.trapmf(self.wind_speed.universe, [15, 18, 22, 25])
        self.wind_speed['Попутный шторм'] = fuzz.trapmf(self.wind_speed.universe, [22, 25, 30, 30])
        
        # Влажность - 4 категории
        self.humidity['Высокая'] = fuzz.trapmf(self.humidity.universe, [60, 70, 100, 100])
        self.humidity['Нормальная'] = fuzz.trapmf(self.humidity.universe, [40, 50, 60, 70])
        self.humidity['Низкая'] = fuzz.trapmf(self.humidity.universe, [20, 30, 40, 50])
        self.humidity['Очень низкая'] = fuzz.trapmf(self.humidity.universe, [0, 0, 20, 30])
        
        # Горящие соседи - 5 категорий
        self.burning_neighbors['Нет'] = fuzz.trimf(self.burning_neighbors.universe, [0, 0, 1])
        self.burning_neighbors['Немного'] = fuzz.trimf(self.burning_neighbors.universe, [0, 2, 4])
        self.burning_neighbors['Несколько'] = fuzz.trimf(self.burning_neighbors.universe, [2, 4, 6])
        self.burning_neighbors['Много'] = fuzz.trimf(self.burning_neighbors.universe, [4, 6, 8])
        self.burning_neighbors['Все'] = fuzz.trimf(self.burning_neighbors.universe, [6, 8, 8])
        
        # Температура - 4 категории
        self.temperature['Очень низкая'] = fuzz.trapmf(self.temperature.universe, [-20, -20, 0, 10])
        self.temperature['Низкая'] = fuzz.trapmf(self.temperature.universe, [5, 10, 15, 20])
        self.temperature['Нормальная'] = fuzz.trapmf(self.temperature.universe, [15, 20, 30, 35])
        self.temperature['Высокая'] = fuzz.trapmf(self.temperature.universe, [30, 35, 50, 50])
        
        # Вероятность возгорания - 8 категорий
        self.fire_prob['Крайне низкая'] = fuzz.trapmf(self.fire_prob.universe, [0, 0, 5, 15])
        self.fire_prob['Очень низкая'] = fuzz.trapmf(self.fire_prob.universe, [5, 15, 20, 30])
        self.fire_prob['Низкая'] = fuzz.trapmf(self.fire_prob.universe, [20, 30, 35, 45])
        self.fire_prob['Ниже среднего'] = fuzz.trapmf(self.fire_prob.universe, [35, 45, 50, 60])
        self.fire_prob['Средняя'] = fuzz.trapmf(self.fire_prob.universe, [50, 60, 65, 75])
        self.fire_prob['Выше среднего'] = fuzz.trapmf(self.fire_prob.universe, [65, 75, 80, 90])
        self.fire_prob['Высокая'] = fuzz.trapmf(self.fire_prob.universe, [80, 85, 90, 95])
        self.fire_prob['Очень высокая'] = fuzz.trapmf(self.fire_prob.universe, [90, 95, 100, 100])
    
    def plot_and_save_membership_functions(self):
        # Создаем и сохраняем каждый график отдельно
        self._plot_single(self.wind_speed, 'wind_speed.png', 'Скорость ветра')
        self._plot_single(self.humidity, 'humidity.png', 'Влажность')
        self._plot_single(self.burning_neighbors, 'burning_neighbors.png', 'Горящие соседи')
        self._plot_single(self.temperature, 'temperature.png', 'Температура')
        self._plot_single(self.fire_prob, 'fire_probability.png', 'Вероятность возгорания')
        
        print("Все графики сохранены в отдельных файлах PNG")
    
    def _plot_single(self, variable, filename, title):
        plt.figure(figsize=(8, 5))
        variable.view()
    
        # Настройка шрифтов:
        plt.rcParams.update({
            'font.size': 14,           # Базовый размер шрифта
            'axes.titlesize': 14,      # Размер заголовка
            'axes.labelsize': 14,      # Размер подписей осей
            'xtick.labelsize': 14,     # Размер подписей по оси X (можно оставить 12, если 14 слишком большой)
            'ytick.labelsize': 14,     # Размер подписей по оси Y (аналогично)
            'legend.fontsize': 10      # Размер шрифта легенды (можно увеличить до 14, если нужно)
        })
    
        plt.title(title, pad=20)
        ax = plt.gca()
        ax.legend(loc='lower left')   # Легенда с настройками по умолчанию (размер уже задан в rcParams)
        ax.set_ylabel("Степень принадлежности нечеткому мн-ву")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

# Создаем экземпляр и сохраняем графики
visualizer = FuzzyFireVizualizer()
visualizer.plot_and_save_membership_functions()