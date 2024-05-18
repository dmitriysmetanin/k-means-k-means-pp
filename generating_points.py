import random
import pygame

def get_points_by_mouse(POINTS_COUNT, AX, AY):
    pygame.init()
    points = []
    screen = pygame.display.set_mode((640, 480))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                points.append([x / 640 * AX,
                               (480 - y) / 480 * AY])
                pygame.draw.circle(screen, (128, 128, 128, 1), (x, y), 5)
                pygame.display.update()
        if len(points) == POINTS_COUNT:
            break
    return points

def get_points_by_random(POINTS_COUNT, AX, AY):
    points = []
    for _ in range(POINTS_COUNT):
        points.append([
            random.randint(0, AX), random.randint(0, AY)
        ])

    return points