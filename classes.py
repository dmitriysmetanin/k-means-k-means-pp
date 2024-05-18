from general_functions import calculate_distance

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
        return calculate_distance(self.coordinates, cluster.centroid)

    def get_new_cluster(self, clusters: list[Cluster]):
        distances = [self.calculate_distance_to_cluster(cluster=cluster) for cluster in clusters]
        return clusters[distances.index(min(distances))]