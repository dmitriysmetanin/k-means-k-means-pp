import random

def calculate_distance(point1, point2):
    if len(point1) != len(point2):
        raise ValueError("Точка и кластер описаны в пространствах разных размерностей")
    else:
        return sum(
            [(point1[i] - point2[i]) ** 2 for i in range(len(point2))]
        ) ** 0.5

def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r / 255, g / 255, b / 255, 1)