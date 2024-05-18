import sys
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation

from generating_points import get_points_by_random
from classes import Cluster, Point
from general_functions import calculate_distance, get_random_color

POINTS_COUNT = int(input("---- Введите количество точек ---->"))
AX = 200
AY = 200
GIF_FRAMES_PER_SECOND = 5

points = get_points_by_random(POINTS_COUNT, AX, AY)

"""
Кол-во кластеров указано вручную, так как при случайном распределении
точек случайной генерации идеальное кол-ва кластеров найти невозможно,
оно будет стремиться к исходному кол-ву точек, что бессмысленно
"""
CLUSTERS_COUNT = 10

# Генерируем цвета для кластеров
colors = [get_random_color() for _ in range(CLUSTERS_COUNT)]
if CLUSTERS_COUNT == 3:
    colors = [(1, 0, 0, 1),
              (0, 1, 0, 1),
              (0, 0, 1), 1]
elif CLUSTERS_COUNT == 4:
    colors.append((75 / 255, 75 / 255, 75 / 255, 1))

# Пре-проверка количества кластеров
if CLUSTERS_COUNT > len(points):
    print(f"Невозможно разбить {len(points)} точек на {CLUSTERS_COUNT} кластеров")
    exit()

# Вычисляем координаты начальных центроидов
# Случайно генерируем координаты первого центроида
centroids = []
first_centroid = points[0]
centroids.append(first_centroid)
# Вычисляем координаты оставшихся CLUSTERS_COUNT-1 центроидов
for c_id in range(CLUSTERS_COUNT - 1):
    dist = []
    for i in range(len(points)):
        point = points[i]
        d = sys.maxsize

        # Вычисляем расстояние от текущей точки до каждого из инициализованных ранее центроидов
        for j in range(len(centroids)):
            temp_dist = calculate_distance(point, centroids[j])
            d = min(d, temp_dist)
        dist.append((d, point))
    next_centroid = sorted(dist, key=lambda x: x[0], reverse=True)[0][1]
    centroids.append(next_centroid)

# Инициализируем точки
points = [Point(coordinates=point) for point in points]

# Инициализируем кластеры
clusters = [Cluster(centroid=centroids[i],
                    color=colors[i]) for i in range(CLUSTERS_COUNT)]

# Присваиваем каждой точке по кластеру
for p in points:
    p.cluster = p.get_new_cluster(clusters=clusters)

# Решаем проблему наличия кластеров, для которых нет ни одной точки
for index, cluster in enumerate(clusters):
    points[index].cluster = cluster

# Анимация: сохранение кадра до кластеризации
fig, ax = plt.subplots(figsize=(10, 6))
frames = []
points_colors = [p.cluster.color for p in points]
line = ax.scatter([p.coordinates[0] for p in points], [p.coordinates[1] for p in points], color=points_colors)
frames.append([line])

# Кластеризация
while True:
    points_colors = [p.cluster.color for p in points]
    line = ax.scatter([p.coordinates[0] for p in points], [p.coordinates[1] for p in points], color=points_colors)
    frames.append([line])

    changed = False
    for cluster in clusters:
        new_centroid = cluster.get_new_centroid(points=points)
        if new_centroid != cluster.centroid:
            cluster.centroid = new_centroid

    for p in points:
        new_cluster = p.get_new_cluster(clusters=clusters)
        if new_cluster != p.cluster:
            changed = True
            p.cluster = new_cluster

    if not changed:
        break

# Анимация: сохранение в файл
animation = ArtistAnimation(
    fig,
    frames,
    interval=1000 / GIF_FRAMES_PER_SECOND,
    repeat=True
)
animation.save(filename="animations/animation_random_generated.gif", writer="pillow")
