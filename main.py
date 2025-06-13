# -*- coding: utf-8 -*-

import copy
import math
import os
import pygame
import random
import sys


def terminate():
    pygame.quit()
    sys.exit()
    quit()


def load_file(filename):
    fullname = os.path.join('data', filename)
    try:
        file = open(fullname, mode='r', encoding='utf-8')
        a = file.readlines()
        for string in range(len(a)):
            a[string] = a[string].replace("\n", "")
        file.close()
        return copy.deepcopy(a)
    except FileNotFoundError:
        return []


def load_level(filename):
    try:
        fullname = os.path.join('data', filename)
        map_file = open(fullname, mode="r", encoding="utf-8")
        level_map = map_file.readlines()
        map_file.close()
        max_width = 0
        for i in range(len(level_map)):
            level_map[i] = level_map[i].strip()
            max_width = max(max_width, len(level_map[i]))
        for i in range(len(level_map)):
            level_map[i] = level_map[i].ljust(max_width, '.')
        return copy.deepcopy(level_map)
    except FileNotFoundError:
        print(f"Файл с названием '{fullname}' не найден")
        terminate()


list_levels = load_file('list_levels.txt')
levelname = None
pygame.init()
size = width, height = 600, 600
image_size = image_width, image_height = 40, 40
tile_size = tile_width, tile_height = 50, 50
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("white"))
pygame.display.set_caption('Игра')
clock = pygame.time.Clock()
FPS = 50
MODE = 0

mode1_x, mode1_y, mode1_w, mode1_h = 100, 150, 100, 120
mode1_res = 0
help1_x, help1_y, help1_w, help1_h = mode1_x, mode1_y + mode1_h + 20, mode1_w, 20
help1_name = "help1.txt"

mode2_x, mode2_y, mode2_w, mode2_h = 250, 150, 100, 120
mode2_res = 0
help2_x, help2_y, help2_w, help2_h = mode2_x, mode2_y + mode2_h + 20, mode2_w, 20
help2_name = "help2.txt"

mode3_x, mode3_y, mode3_w, mode3_h = 400, 150, 100, 120
mode3_res = 0
help3_x, help3_y, help3_w, help3_h = mode3_x, mode3_y + mode3_h + 20, mode3_w, 20
help3_name = "help3.txt"


def load_image(name, w=None, h=None, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с названием '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        try:
            image = image.convert_alpha()
        except pygame.error:
            pass
    if w is not None:
        image = pygame.transform.scale(image, (w, image.get_rect().h))
    if h is not None:
        image = pygame.transform.scale(image, (image.get_rect().w, h))
    return image


def print_text(intro_text, text_x, text_y, surface=screen, color="black", text_size=30):
    font = pygame.font.Font(None, text_size)
    for line in intro_text:
        text_image = font.render(line, 1, pygame.Color(color))
        text_rect = text_image.get_rect()
        text_rect.x = text_x
        text_rect.top = text_y
        surface.blit(text_image, text_rect)
        text_y += text_rect.height


def start_screen(fon_filename):
    Help1 = pygame.Surface((width, height))
    Help1.fill((204, 204, 204))
    print_text(load_file(help1_name) + ["", "Нажмите левой кнопкой мыши",
                                        "чтобы закрыть помощь"], 50, 50, surface=Help1)
    is_help1 = False

    Help2 = pygame.Surface((width, height))
    Help2.fill((204, 204, 204))
    print_text(load_file(help2_name) + ["", "Нажмите левой кнопкой мыши",
                                        "чтобы закрыть помощь"], 50, 50, surface=Help2)
    is_help2 = False

    Help3 = pygame.Surface((width, height))
    Help3.fill((204, 204, 204))
    print_text(load_file(help3_name) + ["", "Нажмите левой кнопкой мыши",
                                        "чтобы закрыть помощь"], 50, 50, surface=Help3)
    is_help3 = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if is_help1:
                        is_help1 = False
                    elif is_help2:
                        is_help2 = False
                    elif is_help3:
                        is_help3 = False
                    else:
                        x, y = event.pos
                        if 0 <= x - help1_x < help1_w and 0 <= y - help1_y < help1_h:
                            is_help1 = True
                        elif 0 <= x - help2_x < help2_w and 0 <= y - help2_y < help2_h:
                            is_help2 = True
                        elif 0 <= x - help3_x < help3_w and 0 <= y - help3_y < help3_h:
                            is_help3 = True
                        elif 0 <= x - mode1_x < mode1_w and 0 <= y - mode1_y < mode1_h \
                                or 0 <= x - mode2_x < mode2_w and 0 <= y - mode2_y < mode2_h:
                            return event
        # screen.fill(pygame.Color("white"))
        fon = pygame.transform.scale(
            load_image(fon_filename), (width, height))
        screen.blit(fon, fon.get_rect())
        print_text(["Выберите режим игры"], 190, 50)

        pygame.draw.rect(screen, pygame.Color("red"),
                         (mode1_x, mode1_y, mode1_w, mode1_h), 0, 3)
        pygame.draw.rect(screen, pygame.Color("blue"),
                         (mode2_x, mode2_y, mode2_w, mode2_h), 0, 3)
        pygame.draw.rect(screen, pygame.Color("green"),
                         (mode3_x, mode3_y, mode3_w, mode3_h), 0, 3)
        print_text(["Режим:", "рекорд"], mode1_x +
                   10, mode1_y + mode1_h // 2 - 20)
        print_text(["Режим:", "уровни"], mode2_x +
                   10, mode2_y + mode2_h // 2 - 20)
        print_text(["Режим:", "погоня"], mode3_x +
                   10, mode3_y + mode3_h // 2 - 20)

        pygame.draw.rect(screen, pygame.Color("yellow"),
                         (help1_x, help1_y, help1_w, help1_h), 0, 3)
        pygame.draw.rect(screen, pygame.Color("yellow"),
                         (help2_x, help2_y, help2_w, help2_h), 0, 3)
        pygame.draw.rect(screen, pygame.Color("yellow"),
                         (help3_x, help3_y, help3_w, help3_h), 0, 3)
        print_text(["Помощь"], help1_x + 10, help1_y)
        print_text(["Помощь"], help2_x + 10, help2_y)
        print_text(["Помощь"], help3_x + 10, help3_y)
        print_text(
            [f"Лучший результат: {mode1_res}"], help1_x - 10, help1_y + help1_h + 20, text_size=20)
        print_text(
            [f"Лучший результат: {mode2_res}"], help2_x - 10, help2_y + help2_h + 20, text_size=20)
        print_text(
            [f"Лучший результат: {mode3_res}"], help3_x - 10, help3_y + help3_h + 20, text_size=20)
        if is_help1:
            screen.blit(Help1, Help1.get_rect())
        elif is_help2:
            screen.blit(Help2, Help2.get_rect())
        elif is_help3:
            screen.blit(Help3, Help3.get_rect())
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.tile_type = tile_type
        self.image = load_image(
            cell_tiles[tile_type], tile_width, tile_height)
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y

    def change_pos(self, dx, dy):
        self.rect.x += tile_width * dx
        self.rect.y += tile_height * dy


class Boom(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(boom_tile, 2 * tile_width, 2 * tile_height)
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x - tile_width // 2
        self.rect.y = tile_height * pos_y - tile_height // 2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(player_tile, image_width, image_height)
        self.rect = self.image.get_rect()
        self.rect.x = tile_width * pos_x + (tile_width - image_width) // 2
        self.rect.y = tile_height * pos_y + (tile_height - image_height) // 2
        self.state = 0

    def change_pos(self, dx, dy):
        self.rect.x += tile_width * dx
        if self.rect.x < 0 or width <= self.rect.x or pygame.sprite.spritecollideany(self, wall_group):
            self.rect.x -= tile_width * dx
        self.rect.y += tile_height * dy
        if self.rect.y < 0 or height <= self.rect.y or pygame.sprite.spritecollideany(self, wall_group):
            self.rect.y -= tile_height * dy

    def change_state(self, state):
        if self.state == 1:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.state == 2:
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.state == 3:
            self.image = pygame.transform.rotate(self.image, 270)
            self.image = pygame.transform.flip(self.image, False, True)
        if state == 1:
            self.image = pygame.transform.rotate(self.image, 270)
        elif state == 2:
            self.image = pygame.transform.flip(self.image, True, False)
        elif state == 3:
            self.image = pygame.transform.rotate(self.image, 270)
            self.image = pygame.transform.flip(self.image, False, True)
        self.state = state


def generate_level(level):
    player_x, player_y, N = None, None, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                empty_group.add(Tile('.', x, y))
                player = Player(x, y)
                player_x, player_y = x, y
            elif level[y][x] == '.':
                empty_group.add(Tile(level[y][x], x, y))
            elif level[y][x] == '#':
                wall_group.add(Tile(level[y][x], x, y))
            else:
                lemon_group.add(Tile(level[y][x], x, y))
                N += 1
    return player_x, player_y, N


def change_board(dx, dy):
    min_x, max_x = width + 1, -1
    min_y, max_y = height + 1, -1
    for sprite in empty_group:
        sprite.change_pos(-dx, -dy)
        min_x = min(min_x, sprite.rect.x)
        max_x = max(max_x, sprite.rect.x)
        min_y = min(min_y, sprite.rect.y)
        max_y = max(max_y, sprite.rect.y)
    for sprite in wall_group:
        sprite.change_pos(-dx, -dy)
        min_x = min(min_x, sprite.rect.x)
        max_x = max(max_x, sprite.rect.x)
        min_y = min(min_y, sprite.rect.y)
        max_y = max(max_y, sprite.rect.y)
    for sprite in lemon_group:
        sprite.change_pos(-dx, -dy)
        min_x = min(min_x, sprite.rect.x)
        max_x = max(max_x, sprite.rect.x)
        min_y = min(min_y, sprite.rect.y)
        max_y = max(max_y, sprite.rect.y)

    if pygame.sprite.spritecollideany(player, lemon_group):
        return 'l', pygame.sprite.spritecollide(player, lemon_group, False)
    elif pygame.sprite.spritecollideany(player, wall_group):
        return '#', pygame.sprite.spritecollide(player, wall_group, False)
    elif player.rect.x < min_x or max_x <= player.rect.x or \
            player.rect.y < min_y or max_y <= player.rect.y:
        return '@', None
    else:
        return '.', None


def control1(res, group):
    global empty_group, wall_group, lemon_group, player
    if res == 'l':
        lemon_x, lemon_y = None, None
        for sprite in group:
            lemon_x, lemon_y = sprite.rect.x, sprite.rect.y
            sprite.kill()
        lemon_coords = []
        for sprite in empty_group:
            lemon_coords.append((sprite.rect.x, sprite.rect.y))
        new_x, new_y = random.choice(lemon_coords)
        for sprite in empty_group:
            if sprite.rect.x == new_x and sprite.rect.y == new_y:
                sprite.kill()
        empty_group.add(
            Tile('.', lemon_x // tile_width, lemon_y // tile_height))
        lemon_group.add(Tile('l', new_x // tile_width, new_y // tile_height))
        return False
    elif res == '#':
        boom_x, boom_y = None, None
        for sprite in group:
            boom_x, boom_y = sprite.rect.x, sprite.rect.y
            # sprite.kill()
        playing = False
        boom = Boom(boom_x // tile_width,
                    boom_y // tile_height)
        screen.fill(pygame.Color("black"))
        empty_group.draw(screen)
        wall_group.draw(screen)
        lemon_group.draw(screen)
        screen.blit(boom.image, boom.rect)
        pygame.display.flip()
        clock.tick(FPS / 100)
        return True
    elif res == '@':
        y, ay = player.rect.y, 0.001
        vy = -math.sqrt(ay * (height - y))
        playing = False
        while player.rect.y < width:
            dt = clock.tick(FPS)
            vy += ay * dt
            y += vy * dt
            player.rect.y = y
            screen.fill(pygame.Color("black"))
            empty_group.draw(screen)
            wall_group.draw(screen)
            lemon_group.draw(screen)
            screen.blit(player.image, player.rect)
            pygame.display.flip()
        return True
    else:
        return False


def control2(res, group):
    global empty_group, wall_group, lemon_group, player
    if res == 'l':
        lemon_x, lemon_y = None, None
        for sprite in group:
            lemon_x, lemon_y = sprite.rect.x, sprite.rect.y
            sprite.kill()
        empty_group.add(
            Tile('.', lemon_x // tile_width, lemon_y // tile_height))
        return False
    elif res == '#':
        boom_x, boom_y = None, None
        for sprite in group:
            boom_x, boom_y = sprite.rect.x, sprite.rect.y
        playing = False
        boom = Boom(boom_x // tile_width,
                    boom_y // tile_height)
        screen.fill(pygame.Color("black"))
        empty_group.draw(screen)
        wall_group.draw(screen)
        lemon_group.draw(screen)
        screen.blit(boom.image, boom.rect)
        pygame.display.flip()
        clock.tick(FPS / 100)
        return True
    elif res == '@':
        y, ay = player.rect.y, 0.001
        vy = -math.sqrt(ay * (height - y))
        playing = False
        while player.rect.y < width:
            dt = clock.tick(FPS)
            vy += ay * dt
            y += vy * dt
            player.rect.y = y
            screen.fill(pygame.Color("black"))
            empty_group.draw(screen)
            wall_group.draw(screen)
            lemon_group.draw(screen)
            screen.blit(player.image, player.rect)
            pygame.display.flip()
        return True
    else:
        return False


def play_mode1():
    global empty_group, wall_group, lemon_group, player, mode1_res, MODE
    levelname = list_levels[-1]
    player_x, player_y, N = generate_level(load_level(levelname))
    player = Player(player_x, player_y)
    boom = None
    playing, is_stop = True, False
    restart = False
    t, n = 60000, 0
    break_ = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                running = False
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    is_stop = not is_stop
                elif not is_stop and event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.change_state(1)
                    res, group = change_board(0, -1)
                    if control1(res, group):
                        playing = False
                        is_stop = True
                        break
                    if res == 'l':
                        n += 1
                elif not is_stop and event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.change_state(0)
                    res, group = change_board(-1, 0)
                    if control1(res, group):
                        playing = False
                        is_stop = True
                        break
                    if res == 'l':
                        n += 1
                elif not is_stop and event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.change_state(3)
                    res, group = change_board(0, 1)
                    if control1(res, group):
                        playing = False
                        is_stop = True
                        break
                    if res == 'l':
                        n += 1
                elif not is_stop and event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.change_state(2)
                    res, group = change_board(1, 0)
                    if control1(res, group):
                        playing = False
                        is_stop = True
                        break
                    if res == 'l':
                        n += 1
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_stop:
                x, y = event.pos
                if 10 <= x < 170 and height - 50 <= y < height - 30:
                    playing = False
                    MODE = 0
                    break_ = True
                elif width // 2 <= x < width // 2 + 235 and height - 50 <= y < height - 30:
                    playing = False
                    restart = True
                    MODE = 1
                    break_ = True
        if break_:
            break
        if playing and is_stop:
            Help1 = pygame.Surface((width, height))
            Help1.fill((204, 204, 204))
            print_text(load_file(
                help1_name) + ["Нажмите ещё раз TAB", "чтобы закрыть помощь"], 50, 50, surface=Help1)
            pygame.draw.rect(Help1, pygame.Color("red"),
                             (10, height - 50, 160, 20))
            print_text(["Основное меню"], 12,
                       height - 50, surface=Help1)
            pygame.draw.rect(Help1, pygame.Color("green"),
                             (width // 2, height - 50, 235, 20))
            print_text(["Перезапустить уровень"], width
                       // 2, height - 50, surface=Help1)
            screen.blit(Help1, Help1.get_rect())
            pygame.display.flip()
            clock.tick(FPS)
        elif playing:
            screen.fill(pygame.Color("black"))
            empty_group.draw(screen)
            wall_group.draw(screen)
            lemon_group.draw(screen)
            screen.blit(player.image, player.rect)
            t -= clock.tick(FPS)
            print_text([f"Осталось: {round(t / 1000, 1)} сек, набрано: {n}, ",
                        f"предыдущий рекорд: {mode1_res}"], width // 3, 10, color="white")
            pygame.display.flip()
            if t < 0:
                playing = False
        elif not playing and is_stop:
            End_window = pygame.Surface((width, height))
            End_window.fill((204, 204, 204))
            print_text(["Игра окончена!", f"Ваш результат: {n}", "", "Желаете сыграть снова?"], 
                        50, 50, surface=End_window)
            pygame.draw.rect(End_window, pygame.Color("red"),
                             (10, height - 50, 160, 20))
            print_text(["Основное меню"], 12,
                       height - 50, surface=End_window)
            pygame.draw.rect(End_window, pygame.Color("green"),
                             (width // 2, height - 50, 235, 20))
            print_text(["Перезапустить уровень"], width
                       // 2, height - 50, surface=End_window)
            screen.blit(End_window, End_window.get_rect())
            pygame.display.flip()
            clock.tick(FPS)
    mode1_res = max(mode1_res, n)
    if restart:
        MODE = 1
    else:
        MODE = 0


# def play_mode2():
#     global empty_group, wall_group, lemon_group, player, mode2_res, MODE
#     cur = 0
#     while cur < len(list_levels):
#         levelname = list_levels[cur]
#         player_x, player_y, N = generate_level(load_level(levelname))
#         player = Player(player_x, player_y)
#         boom = None
#         playing, is_stop, ok = True, False, True
#         restart = False
#         exit_flag = False
#         t, n = 60000, 0
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     playing = False
#                     running = False
#                     terminate()
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_TAB:
#                         is_stop = not is_stop
#                     elif not is_stop and event.key == pygame.K_UP or event.key == pygame.K_w:
#                         player.change_state(1)
#                         res, group = change_board(0, -1)
#                         if control2(res, group):
#                             playing = False
#                             is_stop = True
#                             ok = False
#                             break
#                         if res == 'l':
#                             n += 1
#                     elif not is_stop and event.key == pygame.K_LEFT or event.key == pygame.K_a:
#                         player.change_state(0)
#                         res, group = change_board(-1, 0)
#                         if control1(res, group):
#                             playing = False
#                             is_stop = True
#                             ok = False
#                             break
#                         if res == 'l':
#                             n += 1
#                     elif not is_stop and event.key == pygame.K_DOWN or event.key == pygame.K_s:
#                         player.change_state(3)
#                         res, group = change_board(0, 1)
#                         if control2(res, group):
#                             playing = False
#                             is_stop = True
#                             ok = False
#                             break
#                         if res == 'l':
#                             n += 1
#                     elif not is_stop and event.key == pygame.K_RIGHT or event.key == pygame.K_d:
#                         player.change_state(2)
#                         res, group = change_board(1, 0)
#                         if control2(res, group):
#                             playing = False
#                             is_stop = True
#                             ok = False
#                             break
#                         if res == 'l':
#                             n += 1
#                 elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and is_stop:
#                     x, y = event.pos
#                     print(x, y)
#                     # if not playing and 10 <= x < 170 and height - 50 <= y < height - 30:
#                     #     d
#                     if 10 <= x < 170 and height - 50 <= y < height - 30:
#                         playing = False
#                         ok = True
#                         exit_flag = True
#                         break
#                     elif width // 2 <= x < width // 2 + 235 and height - 50 <= y < height - 30:
#                         playing = False
#                         restart = True
#                         ok = False
#                         break
#             if exit_flag:
#                 MODE = 0
#                 break
#             if n == N:
#                 playing = False
#             if playing and is_stop:
#                 Help2 = pygame.Surface((width, height))
#                 Help2.fill((204, 204, 204))
#                 print_text(load_file(help2_name) + ["Нажмите левой кнопкой мыши",
#                                                     "чтобы закрыть помощь"], 50, 50, surface=Help2)
#                 pygame.draw.rect(Help2, pygame.Color("red"),
#                                  (10, height - 50, 160, 20))
#                 print_text(["Основное меню"], 12,
#                            height - 50, surface=Help2)
#                 pygame.draw.rect(Help2, pygame.Color("green"),
#                                  (width // 2, height - 50, 235, 20))
#                 print_text(["Перезапустить уровень"], width //
#                            2, height - 50, surface=Help1)
#                 screen.blit(Help2, Help2.get_rect())
#                 pygame.display.flip()
#                 clock.tick(FPS)
#             elif playing:
#                 screen.fill(pygame.Color("black"))
#                 empty_group.draw(screen)
#                 wall_group.draw(screen)
#                 lemon_group.draw(screen)
#                 screen.blit(player.image, player.rect)
#                 t -= clock.tick(FPS)
#                 print_text([f"Осталось времени: {round(t / 1000, 1)} сек, набрано: {n}, ",
#                             f"осталось набрать : {N - n}"], width // 3, 10, color="white")
#                 pygame.display.flip()
#                 if t < 0:
#                     playing = False
#             if not playing and is_stop:
#                 End_window = pygame.Surface((width, height))
#                 End_window.fill((204, 204, 204))
#                 print_text(["Игра окончена!", f"Ваш результат: {n}", "", 
#                             "Для прохождения на следующий уровень", "купите подписку \"плюс\""], 
#                             50, 50, surface=End_window)
#                 pygame.draw.rect(End_window, pygame.Color("red"),
#                                  (10, height - 50, 160, 20))
#                 print_text(["Основное меню"], 12,
#                            height - 50, surface=End_window)
#                 # pygame.draw.rect(End_window, pygame.Color("green"),
#                 #                  (width // 2, height - 50, 235, 20))
#                 # print_text(["Перезапустить уровень"], width
#                 #            // 2, height - 50, surface=End_window)
#                 screen.blit(End_window, End_window.get_rect())
#                 pygame.display.flip()

#         if ok:
#             mode2_res = max(mode2_res, cur)
#         # if restart:
#         #     continue


if __name__ == '__main__':
    running = True
    cell_tiles = {"l": "lemon.png", ".": "grass.png", "#": "box.png"}
    player_tile = "player.png"
    boom_tile = "boom.png"

    while running:
        if MODE == 0:
            ev = start_screen("fon.png")
        if 0 <= ev.pos[0] - mode1_x < mode1_w and 0 <= ev.pos[1] - mode1_y < mode1_h:
            MODE = 1
        elif 0 <= ev.pos[0] - mode2_x < mode2_w and 0 <= ev.pos[1] - mode2_y < mode2_h:
            MODE = 2
        elif 0 <= ev.pos[0] - mode3_x < mode3_w and 0 <= ev.pos[1] - mode3_y < mode3_h:
            MODE = 3
        player = None
        empty_group = pygame.sprite.Group()
        wall_group = pygame.sprite.Group()
        lemon_group = pygame.sprite.Group()
        if MODE == 1:
            play_mode1()
        elif MODE == 2:
            Sub = pygame.Surface((width, height))
            Sub.fill((204, 204, 204))
            print_text(["Оформите нашу подписку \"плюс\"", "чтобы открыть этот режим"], 50, 50, surface=Sub)
            pygame.draw.rect(Sub, pygame.Color("red"),
                             (10, height - 50, 160, 20))
            print_text(["Основное меню"], 12,
                       height - 50, surface=Sub)
            screen.blit(Sub, Sub.get_rect())
            pygame.display.flip()
            clock.tick(FPS)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        playing = False
                        running = False
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        if 10 <= x < 170 and height - 50 <= y < height - 30:
                            break
                else:
                    continue
                break
            MODE = 0
        elif MODE == 3:
            Sub = pygame.Surface((width, height))
            Sub.fill((204, 204, 204))
            print_text(["Оформите нашу подписку \"плюс\"", "чтобы открыть этот режим"], 50, 50, surface=Sub)
            pygame.draw.rect(Sub, pygame.Color("red"),
                             (10, height - 50, 160, 20))
            print_text(["Основное меню"], 12,
                       height - 50, surface=Sub)
            screen.blit(Sub, Sub.get_rect())
            pygame.display.flip()
            clock.tick(FPS)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        playing = False
                        running = False
                        terminate()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        if 10 <= x < 170 and height - 50 <= y < height - 30:
                            break
                else:
                    continue
                break
            MODE = 0
        clock.tick(FPS)
    terminate()
