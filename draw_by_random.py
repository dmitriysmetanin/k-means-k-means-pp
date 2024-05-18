import random
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import pygame

CLUSTERS_COUNT = 3
POINTS_COUNT = 50
AX = 200
AY = 200
GIF_FRAMES_PER_SECOND = 1

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r / 255, g / 255, b / 255, 1)


colors = [get_random_color() for _ in range(CLUSTERS_COUNT)]
if CLUSTERS_COUNT == 3:
    colors = [(1, 0, 0, 1),
              (0, 1, 0, 1),
              (0,0,1), 1]
elif CLUSTERS_COUNT == 4:
    colors.append((75/255, 75/255, 75/255,1))


class Cluster():
    def __init__(self, centroid, color):
        self.centroid: list = centroid
        self.color = color

    def get_new_centroid(self, points):
        size = len(self.centroid)
        new_centroid = []
        for _ in range(size):
            new_centroid.append(0)
        c = 0
        for point in points:
            if point.cluster == self:
                c += 1
                for index, value in enumerate(point.coordinates):
                    new_centroid[index] += value
        for index in range(len(new_centroid)):
            new_centroid[index] = new_centroid[index] / c

        return new_centroid


class Point:
    def __init__(self, coordinates):
        self.cluster: Cluster = Cluster(centroid=None, color=[0, 0, 0, 1])
        self.coordinates: list = coordinates

    def calculate_distance_to_cluster(self, cluster: Cluster = None):
        if cluster is None: cluster = self.cluster

        if len(cluster.centroid) != len(self.coordinates):
            raise ValueError("Точка и кластер описаны в пространствах разных размерностей")
        else:
            return sum(
                [(cluster.centroid[i] - self.coordinates[i]) ** 2 for i in range(len(self.coordinates))]
            ) ** 0.5

    def get_new_cluster(self, clusters: list[Cluster]):
        distances = [self.calculate_distance_to_cluster(cluster=cluster) for cluster in clusters]
        return clusters[distances.index(min(distances))]


# Pre-testing data
if CLUSTERS_COUNT > len(points):
    print(f"Невозможно разбить {len(points)} точек на {CLUSTERS_COUNT} кластеров")
    exit()

# Initializing points
points = [Point(coordinates=point) for point in points]

# Initializing clusters
clusters = [Cluster(centroid=points[i].coordinates,
                    color=colors[i]) for i in range(CLUSTERS_COUNT)]

# Adding clusters to points
for p in points:
    p.cluster = p.get_new_cluster(clusters=clusters)

# Solving problem of clusters with no points inside
for index, cluster in enumerate(clusters):
    points[index].cluster = cluster

fig, ax = plt.subplots(figsize=(10, 6))
frames = []

points_colors = [p.cluster.color for p in points]
line = ax.scatter([p.coordinates[0] for p in points], [p.coordinates[1] for p in points], color=points_colors)
frames.append([line])

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

animation = ArtistAnimation(
    fig,
    frames,
    interval=1000/GIF_FRAMES_PER_SECOND,
    repeat=True
)

animation.save(filename="animation_random_generated.gif", writer="pillow")
