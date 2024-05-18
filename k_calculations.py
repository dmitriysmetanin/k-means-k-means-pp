from sklearn.cluster import KMeans

def get_inertias(data):
    # Вычисляем суммы квадратов расстояний точек до центров кластеров
    if len(data) > 10:
        clusters_range = 10
    else:
        clusters_range = len(data)

    inertias = []

    for cluster_count in range(1, clusters_range + 1):
        kmeans = KMeans(n_clusters=cluster_count, random_state=0).fit(data)
        inertia = kmeans.inertia_
        inertias.append(inertia)

    return inertias

def get_best_k(data):
    inertias = get_inertias(data)

    for index, inertia in enumerate(inertias[:-1]):
        inertia_current = inertias[index]
        inertia_next = inertias[index+1]
        if inertia_next == 0: return index+1
        iner_generated = abs(inertia_current - inertia_next) / (max(inertias) - min(inertias))
        print(
            index+1,
              inertia_current,
              inertia_next,
            iner_generated
              )
        if iner_generated < 0.01:
            return index+1

    return len(inertias)