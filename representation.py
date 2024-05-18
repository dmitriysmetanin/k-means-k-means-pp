import matplotlib.pyplot as plt


def plot_inertias(inertias):
    # Формируем график
    plt.plot(range(1, len(inertias) + 1), inertias, '-o')
    plt.xlabel('Кол-во кластеров')
    plt.ylabel('Сумма квадратов расстояний до центров кластеров')

    # Выводим график
    plt.show()
