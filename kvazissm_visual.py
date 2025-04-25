import pygame
from pygame.locals import *
import sys
import time
from pygame.transform import scale

from calculating_advanced import Body
import calculating_advanced


def visualization(qbod, qvis, qvis_date):
    now_date = "00:00:00/01/01/2000"  # Текущая дата

    # Инициализация PyGame
    pygame.init()

    # Настройки экрана
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Визуализация модели")
    DISPLAY_TICK = 60
    clock = pygame.time.Clock()
    vismode = 'xy'
    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    # Переменные отображения данных
    now_date = "00:00:00/01/01/2000"  # Текущая дата
    end_date = ""
    calc_speed = 365 * 24 * 3600
    step = 3600
    file = 'info.txt'
    bod_data = []
    # Шрифты
    font_small = pygame.font.SysFont("Arial", 16)
    font_medium = pygame.font.SysFont("Arial", 24)

    # Масштабирование координат
    SCALE = 1.2e-9  # Масштаб для преобразования метров в пиксели
    PL_REDUCT_SCALE = SCALE * 15  # Для видимости планет
    CAM_DISTANSE = 9e9 * SCALE
    bodies = calculating_advanced.bodies
    running = True
    while running:
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:
                running = False
        if not qbod.empty():  # Приём данных
            bod_data = qbod.get()
            bodies.clear()
            for body_data in bod_data:
                bodies.append(Body(*body_data))
        if not qvis_date.empty():
            now_date = qvis_date.get()
        if not qvis.empty():
            command, data = qvis.get()
            if command == "update_end_date":
                end_date = data
            elif command == "update_speed":
                calc_speed = data
            elif command == "update_step":
                step = data
            elif command == "update_file":
                file = data
        parameters = [f'Текущая дата: {now_date}', f'Конечная дата: {end_date}', f'Скорость расчёта: {calc_speed}', f'Шаг: {step}', f'Файл данных: {file}']
        # Обновление координат и данных
        img_bodies = bodies[0:len(bodies)]
        if vismode == 'xy':
            for body in img_bodies:
                # print(img_bodies == bodies)
                body.x = (body.x * SCALE) + (SCREEN_WIDTH // 2)
                body.y = (-1 * body.y * SCALE) + (SCREEN_HEIGHT // 2)
                body.z *= SCALE
                if body.name != 'Sun':
                    body.radius *= SCALE * 1500  # * body.z / CAM_DISTANSE
                else:
                    body.radius *= SCALE * 60
        elif vismode == 'yz':
            for body in img_bodies:
                body.y = (body.y * SCALE) + (SCREEN_WIDTH // 2)
                body.z = (-1 * body.z * SCALE) + (SCREEN_HEIGHT // 2)
                body.y *= SCALE
                if body.name != 'Sun':
                    body.radius *= SCALE * 15 * body.x / CAM_DISTANSE
                else:
                    body.radius *= SCALE / 15
        screen.fill(WHITE)  # Очистка экрана
        # Отрисовка
        if vismode == 'xy':
            for body in img_bodies:
                pygame.draw.circle(screen, RED, (body.x, body.y), body.radius)
                text_surface = font_medium.render(body.name, True, BLACK)  # Создаем текстовый маркер
                text_rect = text_surface.get_rect()
                text_rect.center = (body.x, body.y - body.radius - 10)
                screen.blit(text_surface, text_rect)
        elif vismode == 'yz':
            for body in img_bodies:
                pygame.draw.circle(screen, RED, (body.y, body.z), body.radius)
                text_surface = font_medium.render(body.name, True, BLACK)  # Создаем текстовый маркер
                text_rect = text_surface.get_rect()
                text_rect.center = (body.y, body.z - body.radius - 10)
                screen.blit(text_surface, text_rect)
        if bod_data:
            bodies.clear()
            for body_data in bod_data:
                bodies.append(Body(*body_data))
        else:
            calculating_advanced.downloader()
            bodies = calculating_advanced.bodies
        sch = 0
        for p in parameters:
            text_date = font_small.render(p, True, BLACK)
            text_date_rect = text_date.get_rect()
            text_date_rect.topleft = (0, sch*text_date_rect.height)
            screen.blit(text_date, text_date_rect)
            sch += 2
        for bod in bodies:
            text_name = font_small.render(f'Имя объекта: {bod.name}', True, WHITE, BLUE)
            text_name_rect = text_name.get_rect()
            text_name_rect.topleft = (0, sch * text_name_rect.height)
            screen.blit(text_name, text_name_rect)
            sch += 1
            text_mass = font_small.render(f'Масса: {bod.mass}', True, BLACK)
            text_mass_rect = text_mass.get_rect()
            text_mass_rect.topleft = (0, sch * text_mass_rect.height)
            screen.blit(text_mass, text_mass_rect)
            sch += 1
            text_rad = font_small.render(f'Радиус: {bod.radius}', True, BLACK)
            text_rad_rect = text_rad.get_rect()
            text_rad_rect.topleft = (0, sch * text_rad_rect.height)
            screen.blit(text_rad, text_rad_rect)
            sch += 2
            text_x = font_small.render(f'x: {bod.x} Vx: {bod.Vx} ax: {bod.ax}', True, BLACK)
            text_x_rect = text_x.get_rect()
            text_x_rect.topleft = (0, sch * text_x_rect.height)
            screen.blit(text_x, text_x_rect)
            sch += 1
            text_y = font_small.render(f'y: {bod.y} Vy: {bod.Vy} ay: {bod.ay}', True, BLACK)
            text_y_rect = text_y.get_rect()
            text_y_rect.topleft = (0, sch * text_y_rect.height)
            screen.blit(text_y, text_y_rect)
            sch += 3
            text_z = font_small.render(f'z: {bod.z} Vz: {bod.Vz} az: {bod.az}', True, BLACK)
            text_z_rect = text_z.get_rect()
            text_z_rect.topleft = (0, sch * text_z_rect.height)
            screen.blit(text_z, text_z_rect)
            sch += 2
        pygame.display.flip()  # Обновление экрана
        # Ограничение частоты обновления
        clock.tick(DISPLAY_TICK)
    pygame.quit()
    sys.exit()
