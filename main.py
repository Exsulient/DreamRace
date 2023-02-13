import pygame, math, sys
from pygame.locals import *
import time
import pygame_menu
from pygame_menu import themes
import sqlite3

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

name = ''

fuel_all_img = ('levels/fuel100.png', 'levels/fuel70.png', 'levels/fuel50.png', 'levels/fuel25.png', \
                'levels/fuel10.png')

lap = 1
car = 1
all_car = {'1': 'cars/porshe.png', '2': 'cars/acura.png', '3': 'cars/ferrari.png', '4': 'cars/lamborgini.png'}

connection = sqlite3.connect("dream_race_leaderboard.db")
cur = connection.cursor()

bg = pygame.image.load('levels/level1.png')
complite_lap = 0
checkpoint1 = False
checkpoint2 = False
checkpoint3 = False
checkpoint4 = False
checkpoint5 = False
checkpoint6 = False

best_lap = 0

number_1 = pygame.image.load('numbers/1.png')
number_2 = pygame.image.load('numbers/2.png')
number_3 = pygame.image.load('numbers/3.png')

barrier_list = {
    'barrier1': [987, 410],
    'barrier2': [987, 205],
    'barrier3': [987, 123],
    'barrier4': [987, 615],
    'barrier5': [987, 820],
    'barrier6': [987, 1],
    'barrier7': [3, 410],
    'barrier8': [3, 205],
    'barrier9': [3, 123],
    'barrier10': [3, 615],
    'barrier11': [3, 820],
    'barrier12': [3, 1],
}

barrier_turn_list = {
    'barrier1': [3, 1],
    'barrier2': [208, 1],
    'barrier3': [3, 1027],
    'barrier4': [208, 1027],
}

fences = [(100, 100), (200, 200), (300, 300)]
fences_turn = [(100, 200), (200, 300), (300, 400)]

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('fence/fence.png')
        self.rect = self.image.get_rect()
        self.turn = pygame.image.load('fence/fence_turn.png')
        self.rect_turn = self.turn.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(all_car[str(car)])
        self.rect = self.image.get_rect()
        self.k_up = self.k_down = self.k_left = self.k_right = 0
        self.speed = self.direction = 0
        self.position = (935, 520)
        self.TURN_SPEED = 1
        self.ACCELERATION = 1
        self.MAX_FORWARD_SPEED = 10
        self.MAX_REVERSE_SPEED = -10
        self.barrier = Barrier()

    def update(self):
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.MAX_FORWARD_SPEED: self.speed = self.MAX_FORWARD_SPEED
        if self.speed < self.MAX_REVERSE_SPEED: self.speed = self.MAX_REVERSE_SPEED
        self.direction += (self.k_right + self.k_left)
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = (x, y)
        if self.position[0] < 0 or self.position[0] > 1000 or self.position[1] < 0 or self.position[1] > 1000:
            self.MAX_FORWARD_SPEED = 0
        else:
            self.MAX_FORWARD_SPEED = 5


class Camera(Player):
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.barrier_list = {
            'barrier1': [987, 410],
            'barrier2': [987, 205],
            'barrier3': [987, 123],
            'barrier4': [987, 615],
            'barrier5': [987, 820],
            'barrier6': [987, 1],
            'barrier7': [3, 410],
            'barrier8': [3, 205],
            'barrier9': [3, 123],
            'barrier10': [3, 615],
            'barrier11': [3, 820],
            'barrier12': [3, 1],
        }
        self.barrier_turn_list = {
            'barrier1': [3, 1],
            'barrier2': [208, 1],
            'barrier3': [3, 1027],
            'barrier4': [208, 1027],
        }
        self.fontes_list = []
        self.fontes_turn_list = []
        self.klazma = pygame.Rect(self.dx + 500, self.dy + 500, 100, 100)
        self.line1 = pygame.Rect(self.dx + 800, self.dy + 870, 130, 30)
        self.line2 = pygame.Rect(self.dx + 740, self.dy + 870, 130, 30)
        self.line3 = pygame.Rect(self.dx + 500, self.dy + 500, 100, 100)
        self.line4 = pygame.Rect(self.dx + 500, self.dy + 500, 100, 100)
        self.line5 = pygame.Rect(self.dx + 520, self.dy + 0, 5, 190)
        self.line6 = pygame.Rect(self.dx + 600, self.dy + 140, 120, 10)
        self.line7 = pygame.Rect(self.dx + 600, self.dy + 140, 120, 10)
        self.line8 = pygame.Rect(self.dx + 740, self.dy + 270, 5, 300)
        self.line9 = pygame.Rect(self.dx + 670, self.dy + 260, 90, 50)
        self.line10 = pygame.Rect(self.dx + 490, self.dy + 360, 30, 120)
        self.line11 = pygame.Rect(self.dx + 350, self.dy + 360, 30, 100)
        self.line12 = pygame.Rect(self.dx + 250, self.dy + 360, 30, 120)
        self.line13 = pygame.Rect(self.dx + 100, self.dy + 360, 30, 120)
        self.line14 = pygame.Rect(self.dx + 100, self.dy + 360, 30, 120)
        self.checkpoint1 = pygame.Rect(self.dx + 800, self.dy + 870, 130, 30)
        self.checkpoint2 = pygame.Rect(self.dx + 740, self.dy + 870, 130, 30)
        self.checkpoint3 = pygame.Rect(self.dx + 500, self.dy + 500, 100, 100)
        self.checkpoint4 = pygame.Rect(self.dx + 500, self.dy + 500, 100, 100)
        self.checkpoint5 = pygame.Rect(self.dx + 520, self.dy + 0, 5, 190)
        self.checkpoint6 = pygame.Rect(self.dx + 600, self.dy + 140, 120, 10)
        self.finish = pygame.Rect(self.dx + 600, self.dy + 140, 120, 10)
        self.fuel = pygame.Rect(self.dx + 900, self.dy + 488, 40, 40)

    def apply(self):
        self.bg_x = self.dx
        self.bg_y = self.dy
        for el in self.barrier_list:
            self.barrier_list[el][0] = (self.dx + barrier_list[el][0])
            self.barrier_list[el][1] = (self.dy + barrier_list[el][1])
        for el in self.barrier_turn_list:
            self.barrier_turn_list[el][0] = (self.dx + barrier_turn_list[el][0])
            self.barrier_turn_list[el][1] = (self.dy + barrier_turn_list[el][1])

    def update(self, player):
        self.dx = -(player.position[0] + player.rect[2] // 2 - SCREEN_WIDTH // 2)
        self.dy = -(player.position[1] + player.rect[3] // 2 - SCREEN_HEIGHT // 2)
        self.klazma = pygame.Rect(self.dx + 740, self.dy + 870, 130, 30)
        self.line1 = pygame.Rect(self.dx + 880, self.dy + 130, 5, 600)
        self.line2 = pygame.Rect(self.dx + 815, self.dy + 690, 70, 150)
        self.line3 = pygame.Rect(self.dx + 720, self.dy + 140, 120, 10)
        self.line4 = pygame.Rect(self.dx + 520, self.dy + 0, 5, 190)
        self.line5 = pygame.Rect(self.dx + 740, self.dy + 270, 5, 300)
        self.line6 = pygame.Rect(self.dx + 500, self.dy + 650, 200, 100)
        self.line7 = pygame.Rect(self.dx + 300, self.dy + 730, 70, 100)
        self.line8 = pygame.Rect(self.dx + 700, self.dy + 280, 70, 50)
        self.line9 = pygame.Rect(self.dx + 490, self.dy + 360, 30, 120)
        self.line10 = pygame.Rect(self.dx + 350, self.dy + 360, 30, 100)
        self.line11 = pygame.Rect(self.dx + 250, self.dy + 360, 80, 220)
        self.line12 = pygame.Rect(self.dx + 130, self.dy + 150, 180, 140)
        self.line13 = pygame.Rect(self.dx + 55, self.dy + 480, 30, 180)
        self.line14 = pygame.Rect(self.dx + 115, self.dy + 830, 80, 70)
        self.checkpoint1 = pygame.Rect(self.dx + 750, self.dy + 70, 5, 47)
        self.checkpoint2 = pygame.Rect(self.dx + 791, self.dy + 350, 74, 5)
        self.checkpoint3 = pygame.Rect(self.dx + 415, self.dy + 575, 5, 75)
        self.checkpoint4 = pygame.Rect(self.dx + 30, self.dy + 200, 63, 5)
        self.checkpoint5 = pygame.Rect(self.dx + 15, self.dy + 890, 60, 5)
        self.checkpoint6 = pygame.Rect(self.dx + 720, self.dy + 950, 5, 47)
        self.finish = pygame.Rect(self.dx + 897, self.dy + 488, 47, 5)
        self.fuel = pygame.Rect(self.dx + 960, self.dy + 450, 20, 30)


def main():
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("DreamRace")
    font = pygame_menu.font.FONT_MUNRO

    def select_car(value, difficulty):
        global car
        car = difficulty

    def end_win(best_lap):
        win_end.clear()
        mainmenu._open(win_end)
        win_end.add.image('menu/win.png')
        win_end.add.button('Restart', start_the_game, font_name=font)
        win_end.add.text_input('Name: ', default=name, maxchar=20, font_name=font, onchange=player_name)
        win_end.add.label(f'Best lap: {best_lap}', font_name=font)
        win_end.add.button('Add lap time to the Leaderboard', save_lap_time, font_name=font)

    def player_name(nick):
        global name
        name = nick

    def save_lap_time():
        add_player = True
        leaderboard = cur.execute("""select id, name, time from leaderboard""").fetchall()
        player_info = (name, best_lap)
        for el in leaderboard:
            if el[1] == name:
                win_end.add.label('NickName already exists', font_name=font, font_color='red')
                win_end.add.button('Replace the time?', replace_time, font_name=font, font_color='red')
                add_player = False
                break

        if add_player:
            cur.execute("""INSERT INTO leaderboard(name, time)
                                        VALUES(?, ?);""", player_info)
            connection.commit()
            win_end.add.label('Result added', font_name=font, font_color='green')

    def replace_time():
        player_info = (best_lap, name)
        cur.execute("""update leaderboard set time = ? where name = ?""", player_info)

    def start_game():
        barrier = Barrier()
        player = Player()
        camera = Camera()
        active_sprite_list = pygame.sprite.Group()
        active_sprite_list.add(player)
        done = False
        clock = pygame.time.Clock()
        start = True
        lap_complit = False
        start_time = True
        font = pygame.font.Font('joystix monospace.otf', 50)
        font1 = pygame.font.Font('joystix monospace.otf', 90)
        startTime = time.time()
        n = 0
        minutes = 0
        seconds = 0
        millis = 0
        fuel_car = 100
        global lap
        global complite_lap
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if not hasattr(event, 'key'): continue
                down = event.type == KEYDOWN
                if event.key == K_RIGHT:
                    player.k_right = down * -4
                elif event.key == K_LEFT:
                    player.k_left = down * 4
                elif event.key == K_UP:
                    player.k_up = down * 0.1
                    fuel_car -= 1.5
                elif event.key == K_DOWN:
                    player.k_down = down * -0.1
                    fuel_car -= 1.5
                elif event.key == K_ESCAPE:
                    sys.exit(0)

            if start_time:
                time_r = int(time.time() - startTime)
                minutes = (time_r % 3600) // 60
                seconds = time_r % 60
                millis = int(((time.time() - startTime) - time_r) * 1000)

            rotated = pygame.transform.rotate(player.image, player.direction)
            rect = rotated.get_rect()
            rect.center = player.position

            for el in camera.barrier_list:
                screen.blit(barrier.image, (camera.barrier_list[el][0], camera.barrier_list[el][1]))
                pygame.draw.rect(screen, (255, 255, 255), camera.checkpoint1)
                pygame.draw.rect(screen, (255, 255, 255), camera.checkpoint2)
                pygame.draw.rect(screen, (255, 255, 255), camera.checkpoint3)
                pygame.draw.rect(screen, (255, 255, 255), camera.checkpoint4)
                pygame.draw.rect(screen, (255, 255, 255), camera.checkpoint5)
                pygame.draw.rect(screen, (255, 255, 255), camera.checkpoint6)
                if rect.colliderect(camera.barrier_list[el][0], camera.barrier_list[el][1], 8, 212):
                    player.speed = 0

            for el in camera.barrier_turn_list:
                screen.blit(barrier.turn, (camera.barrier_turn_list[el][0], camera.barrier_turn_list[el][1]))
            pygame.draw.rect(screen, (40, 41, 35), pygame.Rect(0, 0, 1920, 200))
            pygame.draw.rect(screen, (40, 41, 35), pygame.Rect(0, 880, 1920, 200))
            pygame.draw.rect(screen, (40, 41, 35), pygame.Rect(0, 0, 200, 1080))
            pygame.draw.rect(screen, (40, 41, 35), pygame.Rect(1520, 0, 400, 1080))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(200, 190, 1320, 10))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(200, 880, 1320, 10))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(190, 190, 10, 700))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(1520, 190, 10, 700))
            text = font.render(f"Checkpoint", True, (255, 255, 255))
            screen.blit(text, (1500, 40))
            text = font.render(f"{n} / 6", True, (255, 255, 255))
            screen.blit(text, (1580, 100))
            text = font.render(f"Lap", True, (255, 255, 255))
            screen.blit(text, (60, 35))
            text = font.render(f"{complite_lap} / {lap}", True, (255, 255, 255))
            screen.blit(text, (40, 100))
            text = font1.render(f"{int(player.speed * 30)} KM/H", True, (255, 255, 255))
            screen.blit(text, (650, 930))

            if fuel_car <= 100 and fuel_car >= 75:
                screen.blit(pygame.image.load(fuel_all_img[0]), (1575, 190))

            elif fuel_car < 75 and fuel_car >= 50:
                screen.blit(pygame.image.load(fuel_all_img[1]), (1575, 190))

            elif fuel_car < 50 and fuel_car >= 25:
                screen.blit(pygame.image.load(fuel_all_img[2]), (1575, 190))

            elif fuel_car < 25 and fuel_car >= 10:
                screen.blit(pygame.image.load(fuel_all_img[3]), (1575, 190))

            elif fuel_car < 10 and fuel_car >= 0:
                screen.blit(pygame.image.load(fuel_all_img[4]), (1575, 190))

            laptime = f"{minutes}:{seconds}:{millis}"
            text = font1.render(laptime, True, (255, 255, 255))
            screen.blit(text, (600, 50))
            if rect.colliderect(camera.barrier_turn_list[el][0], camera.barrier_turn_list[el][1], 848, 8):
                player.speed = 0

            if rect.colliderect(camera.klazma) or rect.colliderect(camera.line3) or rect.colliderect(camera.line9) \
                    or rect.colliderect(camera.line10) or rect.colliderect(camera.line13) or fuel_car < 0:
                player.speed = 0
                done = True
                complite_lap = 0
                end_bad()

            if rect.colliderect(camera.fuel):
                fuel_car = 100

            if rect.colliderect(camera.line1) or rect.colliderect(camera.line2) or rect.colliderect(camera.line4) \
                    or rect.colliderect(camera.line5) or rect.colliderect(camera.line6) or \
                    rect.colliderect(camera.line7) or rect.colliderect(camera.line8) or \
                    rect.colliderect(camera.line11) or rect.colliderect(camera.line12) or \
                    rect.colliderect(camera.line14):
                player.speed = -2

            if rect.colliderect(camera.checkpoint1):
                n = 1
                global checkpoint1
                checkpoint1 = True

            if rect.colliderect(camera.checkpoint2) and checkpoint1 == True:
                n = 2
                global checkpoint2
                checkpoint2 = True

            if rect.colliderect(camera.checkpoint3) and checkpoint2 == True:
                n = 3
                global checkpoint3
                checkpoint3 = True

            if rect.colliderect(camera.checkpoint4) and checkpoint3 == True:
                n = 4
                global checkpoint4
                checkpoint4 = True

            if rect.colliderect(camera.checkpoint5) and checkpoint4 == True:
                n = 5
                global checkpoint5
                checkpoint5 = True

            if rect.colliderect(camera.checkpoint6) and checkpoint5 == True:
                n = 6
                global checkpoint6
                checkpoint6 = True

            if rect.colliderect(camera.finish) and checkpoint6 == True:
                n = 0
                checkpoint1 = False
                checkpoint2 = False
                checkpoint3 = False
                checkpoint4 = False
                checkpoint5 = False
                checkpoint6 = False
                lap_complit = True

            if not rect.colliderect(camera.finish) and lap_complit == True:
                complite_lap += 1
                global best_lap
                if best_lap == 0:
                    best_lap = laptime
                    startTime = time.time()

                elif int(best_lap.replace(':', '')) > int(laptime.replace(':', '')):
                    best_lap = laptime
                    startTime = time.time()
                lap_complit = False

                if lap == complite_lap:
                    complite_lap = 0
                    done = True
                    end_win(best_lap)

            pygame.display.flip()
            camera.update(player)
            camera.apply()
            screen.fill((66, 173, 55))
            screen.blit(bg, (camera.bg_x, camera.bg_y))
            screen.blit(rotated, rect)
            active_sprite_list.update()
            if player.rect.right > SCREEN_WIDTH:
                player.rect.right = SCREEN_WIDTH
            if player.rect.left < 0:
                player.rect.left = 0

            if start:
                screen.blit(number_3, (450, 350))
                pygame.display.flip()
                time.sleep(2)

                screen.blit(number_2, (700, 350))
                pygame.display.flip()
                time.sleep(2)

                screen.blit(number_1, (950, 350))
                pygame.display.flip()
                time.sleep(2)
                start = False
                startTime = time.time()
                start_time = True

            clock.tick(30)

    def start_menu():
        mainmenu._open(start)

    def start_the_game():
        start_game()

    def end_bad():
        mainmenu._open(bad_end)

    def count_lap(all_lap):
        global lap
        if all_lap == '':
            lap = 1
        else:
            lap = int(all_lap)

    def leaderboard_menu():
        id = 1
        leader.clear()
        leaderboard = cur.execute("""select name, time from leaderboard""").fetchall()

        def custom_key(time):
            return time[1]

        leaderboard.sort(key=custom_key)
        mainmenu._open(leader)
        leader.add.image('menu/leaderboard.png')

        table = leader.add.table()
        table.add_row(['Rank', 'Name', 'Time'], cell_border_color='white', cell_padding=20, cell_font_color='white', \
                      cell_font=font)
        for el in leaderboard:
            name, time = el[0], el[1]
            table.add_row([id, name, time], cell_border_color='white', cell_padding=20, cell_font_color='white', \
                          cell_font=font)
            id += 1

    mainmenu = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HEIGHT, theme=themes.THEME_DARK)
    mainmenu.add.image('menu/dreamrace.png')
    mainmenu.add.image('menu/car.png')
    mainmenu.add.button('Play', start_menu, font_name=font)
    mainmenu.add.text_input('Name: ', default='', maxchar=20, font_name=font, onchange=player_name)
    mainmenu.add.button('Leader board', leaderboard_menu, font_name=font)
    mainmenu.add.button('Quit', pygame_menu.events.EXIT, font_name=font)

    leader = pygame_menu.Menu('', 1920, 1080, theme=themes.THEME_DARK)

    start = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HEIGHT, theme=themes.THEME_DARK)
    start.add.image('menu/changecar1.png')
    start.add.selector('Car :', [('Porshe', 1), ('Acura', 2), ('Ferrari', 3), ('Lamborgini', 4)], \
                       onchange=select_car, font_name=font)

    bad_end = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HEIGHT, theme=themes.THEME_DARK)
    bad_end.add.image('menu/dead.png')
    bad_end.add.button('Restart', start_the_game, font_name=font)
    win_end = pygame_menu.Menu('', SCREEN_WIDTH, SCREEN_HEIGHT, theme=themes.THEME_DARK)
    start.add.text_input('Lap: ', default='', maxchar=20, font_name=font, onchange=count_lap)
    start.add.button('Play', start_the_game, font_name=font)
    mainmenu.mainloop(screen)


pygame.quit()

if __name__ == '__main__':
    main()
