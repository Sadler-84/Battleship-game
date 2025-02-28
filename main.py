import pygame
import sys
import os
import random

pygame.init()

# Размер окна
size = width, height = 1350, 900
clock = pygame.time.Clock()


game_phase = "placement"  # "placement" - расстановка кораблей, "battle" - фаза боя
player_turn = True  # True - ход игрока, False - ход компьютера

cursor_img = pygame.transform.scale(pygame.image.load("data/arrow.png"), (32, 32))
pygame.mouse.set_visible(False) # теперь есть новый курсор


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Матрицы board – для игрока, board2 – для компьютера
        self.board = [[1] * width for _ in range(height)]
        self.board2 = [[1] * width for _ in range(height)]
        self.left = 100
        self.top = 100
        self.cell_size = 50
        self.font_size1 = int(self.cell_size / 1.5)
        self.font_size2 = int(self.cell_size * 2)
        self.font = pygame.font.SysFont('notosans', self.font_size1) #шрифт для букв и цифр вокруг таблиуы
        self.font2 = pygame.font.SysFont(None, self.font_size2)
        self.pause = False

    def load_image(self, name, colorkey=None, size=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if size is not None:
            image = pygame.transform.scale(image, size)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size

        # Для второй сетки (сдвиг вправо)
        sdvig = 13 * self.cell_size
        cell_x2 = (x - self.left - sdvig) // self.cell_size
        cell_y2 = (y - self.top) // self.cell_size

        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return "board1", cell_x, cell_y
        elif 0 <= cell_x2 < self.width and 0 <= cell_y2 < self.height:
            return "board2", cell_x2, cell_y2
        else:
            return None

    def on_click(self, board_name, x, y):
        if board_name == "board1":
            # При расстановке кораблей игрока переключаем состояние ячейки
            self.board[y][x] = 0 if self.board[y][x] == 1 else 1
            print(f"Клик по первой сетке: {x}, {y}")
        elif board_name == "board2":
            # Для расстановки компьютера (если потребуется)
            self.board2[y][x] = 0 if self.board2[y][x] == 1 else 1
            print(f"Клик по второй сетке: {x + 10}, {y}")

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            board_name, x, y = cell_coords
            self.on_click(board_name, x, y)

    def render(self, screen):
        letters = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И"]

        # Отрисовка обеих сеток и подписей
        for y in range(self.height):
            for x in range(self.width):
                # Первая сетка (игрока)
                rect1 = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (0, 0, 0), rect1, 1)

                # Вторая сетка (компьютера)
                rect2 = pygame.Rect(
                    self.left + x * self.cell_size + 13 * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (0, 0, 0), rect2, 1)

            if y < len(letters):
                num_ver = self.font.render(str(y + 1), True, (0, 0, 0))
                letters_hor = self.font.render(letters[y], True, (0, 0, 0))
                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_width = letters_hor.get_width()

                # Подписи для первой сетки
                screen.blit(num_ver,
                            (self.left - (self.cell_size // 2 + num_ver_width // 2),
                             self.top + y * self.cell_size + (self.cell_size // 2 - num_ver_height // 2))
                            )
                screen.blit(letters_hor,
                            (self.left + y * self.cell_size + self.cell_size // 2 - letters_hor_width // 2,
                             self.top - num_ver_height)
                            )

                # Подписи для второй сетки
                screen.blit(num_ver,
                            (self.left - (self.cell_size // 2 + num_ver_width // 2) + self.cell_size * 13,
                             self.top + y * self.cell_size + (self.cell_size // 2 - num_ver_height // 2))
                            )
                screen.blit(letters_hor,
                            (self.left + y * self.cell_size +
                             self.cell_size // 2 - letters_hor_width // 2 +
                             self.cell_size * 13,
                             self.top - num_ver_height)
                            )
        # Отрисовка выстрелов на сетке компьютера
        for y in range(self.height):
            for x in range(self.width):
                rect2 = pygame.Rect(
                    self.left + x * self.cell_size + 13 * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.board2[y][x] == 2:
                    self.draw_cross(screen, rect2)
                elif self.board2[y][x] == 3:
                    self.draw_dot(screen, rect2)

    def draw_cross(self, screen, rect):
        color = (255, 0, 0)
        pygame.draw.line(screen, color, rect.topleft, rect.bottomright, 3)
        pygame.draw.line(screen, color, rect.topright, rect.bottomleft, 3)

    def draw_dot(self, screen, rect):
        color = (0, 0, 255)
        center = rect.center
        radius = self.cell_size // 8
        pygame.draw.circle(screen, color, center, radius)

    def draw_player_ships(self, screen):
        # Отрисовка кораблей игрока по board
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                val = self.board[y][x]
                if val == 0:  # корабль (не поражён)
                    pygame.draw.rect(screen, (0, 150, 0), rect)
                elif val == 2:  # попадание
                    self.draw_cross(screen, rect)
                elif val == 3:  # промах
                    self.draw_dot(screen, rect)

    def get_ship_size_from_matrix(self, matrix, x, y):
        # узнаём размер корабля из матрицы
        visited = set()
        stack = [(x, y)]
        count = 0
        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            if matrix[cy][cx] in (0, 2):  # 0 - целый корабль, 2 - поражённая клетка
                count += 1
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx = cx + dx
                    ny = cy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if matrix[ny][nx] in (0, 2) and (nx, ny) not in visited:
                            stack.append((nx, ny))
        return count

    def process_player_shot(self, board_name, x, y):
        # обработка клика(выстрела игрока)
        if board_name != "board2":
            return False
        current = self.board2[y][x]
        if current in (2, 3):
            return False
        if current == 0:
            self.board2[y][x] = 2  # отмечаем попадание крестом
            ship_size = self.get_ship_size_from_matrix(self.board2, x, y)
            if ship_size == 1:
                # Только для одиночного корабля вокруг ставим точки
                for ny in range(y - 1, y + 2):
                    for nx in range(x - 1, x + 2):
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.board2[ny][nx] not in (2, 3):
                                self.board2[ny][nx] = 3
            return True
        elif current in (1, -1):
            self.board2[y][x] = 3
            return True

    def process_computer_shot(self, x, y):
        #обработак выстрела компьютера
        if self.board[y][x] in (2, 3):
            return False
        if self.board[y][x] == 0:
            self.board[y][x] = 2
            ship_size = self.get_ship_size_from_matrix(self.board, x, y)
            if ship_size == 1:
                for ny in range(y - 1, y + 2):
                    for nx in range(x - 1, x + 2):
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.board[ny][nx] not in (2, 3):
                                self.board[ny][nx] = 3
            return True
        elif self.board[y][x] in (1, -1):
            self.board[y][x] = 3
            return True

    def count_remaining_ships(self, board_matrix):
        # кол-во кораблей
        visited = set()
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) not in visited and board_matrix[y][x] in (0, 2):
                    stack = [(x, y)]
                    alive = False
                    while stack:
                        cx, cy = stack.pop()
                        if (cx, cy) in visited:
                            continue
                        visited.add((cx, cy))
                        if board_matrix[cy][cx] == 0:
                            alive = True
                        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if board_matrix[ny][nx] in (0, 2) and (nx, ny) not in visited:
                                    stack.append((nx, ny))
                    if alive:
                        count += 1
        return count


class Ships:
    def __init__(self, board):
        self.board = board
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.current_ship_index = 0
        self.hor_ver = True  # True - горизонтально, False - вертикально
        self.current_ship = None
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.placed_ships = []
        self.create_next_ship()

    def create_next_ship(self):
        if self.current_ship_index < len(self.ships):
            self.ship_size = self.ships[self.current_ship_index]
            x = self.board.left * 2
            y = self.board.height * self.board.cell_size + self.board.top + 50
            if self.hor_ver:
                self.current_ship = pygame.Rect(
                    x, y, self.ship_size * self.board.cell_size, self.board.cell_size
                )
            else:
                self.current_ship = pygame.Rect(
                    x, y, self.board.cell_size, self.ship_size * self.board.cell_size
                )
        else:
            self.current_ship = None

    def draw_ships(self, screen):
        for ship in self.placed_ships:
            pygame.draw.rect(screen, (0, 150, 0), ship)
        if self.current_ship:
            pygame.draw.rect(screen, (70, 70, 70), self.current_ship)

    def handle_event(self, event):
        if self.current_ship is None:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.current_ship.collidepoint(event.pos):
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.current_ship.x - mouse_x
                self.offset_y = self.current_ship.y - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                is_snapped = self.snap_to_grid()
                if is_snapped:
                    self.placed_ships.append(self.current_ship.copy())
                    self.mark_neighbors()
                    self.current_ship_index += 1
                    self.create_next_ship()
                else:
                    self.reset_ship_position()
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.current_ship.x = mouse_x + self.offset_x
                self.current_ship.y = mouse_y + self.offset_y

    def snap_to_grid(self):
        grid_x = round(
            (self.current_ship.x - self.board.left) / self.board.cell_size) * self.board.cell_size + self.board.left
        grid_y = round(
            (self.current_ship.y - self.board.top) / self.board.cell_size) * self.board.cell_size + self.board.top
        if grid_x < self.board.left or grid_y < self.board.top:
            return False
        if grid_x + self.ship_size > self.board.left + self.board.width * self.board.cell_size or \
                grid_y + self.ship_size > self.board.top + self.board.height * self.board.cell_size:
            return False
        if self.hor_ver:
            if grid_x + self.current_ship.width > self.board.left + self.board.width * self.board.cell_size:
                return False
        else:
            if grid_y + self.current_ship.height > self.board.top + self.board.height * self.board.cell_size:
                return False
        self.current_ship.x = grid_x
        self.current_ship.y = grid_y
        first_cell_x = int((grid_x - self.board.left) / self.board.cell_size)
        first_cell_y = int((grid_y - self.board.top) / self.board.cell_size)
        ship_size = self.ships[self.current_ship_index]
        if not self.is_valid_placement(first_cell_x, first_cell_y, ship_size):
            return False
        self.place_ship(first_cell_x, first_cell_y, ship_size)
        return True

    def is_valid_placement(self, start_x, start_y, ship_size):
        if start_x < 0 or start_y < 0:
            return False
        if self.hor_ver:
            if start_x + ship_size > self.board.width:
                return False
            for i in range(ship_size):
                if self.board.board[start_y][start_x + i] != 1:
                    return False
        else:
            if start_y + ship_size > self.board.height:
                return False
            for i in range(ship_size):
                if self.board.board[start_y + i][start_x] != 1:
                    return False
        return True

    def place_ship(self, start_x, start_y, ship_size):
        if self.hor_ver:
            for i in range(ship_size):
                self.board.board[start_y][start_x + i] = 0
        else:
            for i in range(ship_size):
                self.board.board[start_y + i][start_x] = 0

    def mark_neighbors(self):
        start_x = (self.current_ship.x - self.board.left) // self.board.cell_size
        start_y = (self.current_ship.y - self.board.top) // self.board.cell_size
        ship_size = self.ships[self.current_ship_index]
        if self.hor_ver:
            x_range = range(start_x - 1, start_x + ship_size + 1)
            y_range = range(start_y - 1, start_y + 2)
        else:
            x_range = range(start_x - 1, start_x + 2)
            y_range = range(start_y - 1, start_y + ship_size + 1)
        for y in y_range:
            for x in x_range:
                if 0 <= x < self.board.width and 0 <= y < self.board.height:
                    if self.board.board[y][x] == 1:
                        self.board.board[y][x] = -1

    def reset_ship_position(self):
        ship_size = self.ships[self.current_ship_index]
        x = self.board.left * 2
        y = self.board.height * self.board.cell_size + self.board.top + 50
        if self.hor_ver:
            self.current_ship = pygame.Rect(
                x, y, ship_size * self.board.cell_size, self.board.cell_size
            )
        else:
            self.current_ship = pygame.Rect(
                x, y, self.board.cell_size, ship_size * self.board.cell_size
            )

    def toggle_orientation(self):
        if self.current_ship is not None:
            ship_size = self.ships[self.current_ship_index]
            x = self.current_ship.x
            y = self.current_ship.y
            self.hor_ver = not self.hor_ver
            if self.hor_ver:
                self.current_ship = pygame.Rect(
                    x, y, ship_size * self.board.cell_size, self.board.cell_size
                )
            else:
                self.current_ship = pygame.Rect(
                    x, y, self.board.cell_size, ship_size * self.board.cell_size
                )

    def render(self, screen):
        for ship in self.placed_ships:
            pygame.draw.rect(screen, (0, 150, 0), ship)
        if self.current_ship:
            pygame.draw.rect(screen, (70, 70, 70), self.current_ship)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, color, hover_color, action=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.font = pygame.font.Font(None, 30)
        self.text_surf = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.image.fill(self.hover_color)
            else:
                self.image.fill(self.color)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action is not None:
                self.action()


class ComputerShips:
    def __init__(self, board):
        self.board = board
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.ship_index = 0

    def is_valid_placement(self, start_x, start_y, ship_size, hor_ver):
        if start_x < 0 or start_y < 0:
            return False
        if hor_ver == 0:
            if start_x + ship_size > self.board.width:
                return False
            for i in range(ship_size):
                if self.board.board2[start_y][start_x + i] != 1:
                    return False
        else:
            if start_y + ship_size > self.board.height:
                return False
            for i in range(ship_size):
                if self.board.board2[start_y + i][start_x] != 1:
                    return False
        return True

    def place_ship(self, start_x, start_y, ship_size, hor_ver):
        if hor_ver == 0:
            for i in range(ship_size):
                self.board.board2[start_y][start_x + i] = 0
        else:
            for i in range(ship_size):
                self.board.board2[start_y + i][start_x] = 0

    def mark_neighbors(self, start_x, start_y, ship_size, hor_ver):
        if hor_ver == 0:
            x_range = range(start_x - 1, start_x + ship_size + 1)
            y_range = range(start_y - 1, start_y + 2)
        else:
            x_range = range(start_x - 1, start_x + 2)
            y_range = range(start_y - 1, start_y + ship_size + 1)
        for y in y_range:
            for x in x_range:
                if 0 <= x < self.board.width and 0 <= y < self.board.height:
                    if self.board.board2[y][x] == 1:
                        self.board.board2[y][x] = -1

    def make_random_ship(self):
        if self.ship_index >= len(self.ships):
            return False
        ship_size = self.ships[self.ship_index]
        hor_ver = random.randint(0, 1)
        if hor_ver == 0:
            x = random.randint(0, self.board.width - ship_size)
            y = random.randint(0, self.board.height - 1)
        else:
            x = random.randint(0, self.board.width - 1)
            y = random.randint(0, self.board.height - ship_size)
        if self.is_valid_placement(x, y, ship_size, hor_ver):
            self.place_ship(x, y, ship_size, hor_ver)
            self.mark_neighbors(x, y, ship_size, hor_ver)
            self.ship_index += 1
            return True
        else:
            return False

    def place_all_ships(self):
        attempts = 0
        while self.ship_index < len(self.ships) and attempts < 1000:
            if not self.make_random_ship():
                attempts += 1
            else:
                attempts = 0


def computer_move(board):
    valid = False
    while not valid:
        x = random.randint(0, board.width - 1)
        y = random.randint(0, board.height - 1)
        if board.board[y][x] not in (2, 3):
            valid = True
    board.process_computer_shot(x, y)
    print(f"Компьютер стреляет в ({x}, {y})")


# Основной блок программы
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Морской бой")
    board = Board(10, 10)
    ships = Ships(board)
    computer_ships_obj = ComputerShips(board)
    computer_ships_obj.place_all_ships()  # Расставляем корабли компьютера

    all_sprites = pygame.sprite.Group()
    pause_img = board.load_image("pause.png", size=(50, 50), colorkey=-1)
    pause_sprite = pygame.sprite.Sprite(all_sprites)
    pause_sprite.image = pause_img
    pause_sprite.rect = pause_sprite.image.get_rect()
    pause_sprite.rect.x = 0
    pause_sprite.rect.y = 0
    all_sprites.add(pause_sprite)

    turn_img = board.load_image("turn.png", size=(50, 50), colorkey=-1)
    turn_sprite = pygame.sprite.Sprite(all_sprites)
    turn_sprite.image = turn_img
    turn_sprite.rect = turn_sprite.image.get_rect()
    turn_sprite.rect.x = board.left
    turn_sprite.rect.y = 650
    all_sprites.add(turn_sprite)

    # Загружаем изображение Game Over (будет показано при завершении игры)
    gameover_img = board.load_image("gameover.png", size=(1350, 900), colorkey=-1)

    # Флаги окончания игры
    game_over = False
    winner = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                # Фаза расстановки кораблей
                if game_phase == "placement":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            board.pause = not board.pause
                            print("Пауза:", board.pause)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = event.pos
                        if pause_sprite.rect.collidepoint(pos):
                            board.pause = not board.pause
                            print("Пауза:", board.pause)
                        elif turn_sprite.rect.collidepoint(pos):
                            if not board.pause:
                                ships.toggle_orientation()
                                print("Поворот: ", ships.hor_ver)
                        else:
                            if not board.pause:
                                board.get_click(pos)
                    if not board.pause:
                        ships.handle_event(event)

                # Фаза боя
                elif game_phase == "battle":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            board.pause = not board.pause
                            print("Пауза:", board.pause)
                    # Если ход игрока и клик по второй сетке
                    if player_turn and event.type == pygame.MOUSEBUTTONDOWN and not board.pause:
                        pos = event.pos
                        cell = board.get_cell(pos)
                        if cell and cell[0] == "board2":
                            _, cx, cy = cell
                            if board.process_player_shot("board2", cx, cy):
                                print(f"Игрок стреляет в ({cx}, {cy})")
                                player_turn = False  # передаём ход компьютеру

        # Переход из фазы расстановки в фазу боя
        if game_phase == "placement" and ships.current_ship is None:
            game_phase = "battle"
            print("Переход в фазу боя. Ход игрока.")

        # Если фаза боя и сейчас ход компьютера, то делаем ход (с небольшой задержкой)
        if game_phase == "battle" and not player_turn and not board.pause and not game_over:
            pygame.time.delay(500)  # задержка для наглядности
            computer_move(board)
            player_turn = True

        # Расчёт оставшихся кораблей (только в фазе боя)
        if game_phase == "battle":
            player_ship_count = board.count_remaining_ships(board.board)
            computer_ship_count = board.count_remaining_ships(board.board2)
            # Проверка окончания игры
            if not game_over:
                if player_ship_count == 0:
                    game_over = True
                    winner = "Компьютер"
                elif computer_ship_count == 0:
                    game_over = True
                    winner = "Игрок"
        else:
            # Если не в фазе боя, зададим значения по умолчанию
            player_ship_count = len(ships.ships) - ships.current_ship_index
            computer_ship_count = len(computer_ships_obj.ships) - computer_ships_obj.ship_index

        # Отрисовка
        if not board.pause:
            screen.fill((200, 200, 200))
            board.render(screen)
            # Отображение информации о ходе и количестве кораблей
            status_text = board.font.render(f"Ход: {'Игрок' if player_turn else 'Компьютер'}", True, (0, 0, 0))
            screen.blit(status_text, (width // 2 - status_text.get_width() // 2, 10))
            ships_text = board.font.render(
                f"Корабли игрока: {player_ship_count}    Корабли компьютера: {computer_ship_count}", True, (0, 0, 0))
            screen.blit(ships_text, (width // 2 - ships_text.get_width() // 2, 40))

            if game_phase == "battle":
                board.draw_player_ships(screen)
            elif game_phase == "placement":
                ships.draw_ships(screen)
                ships.render(screen)
            all_sprites.draw(screen)
        else:
            rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (100, 100, 100, 15), (0, 0, width, height))
            screen.blit(rect_surface, (0, 0))
            pause_text = board.font2.render("Пауза", False, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(width // 2, height // 2 - 200))
            screen.blit(pause_text, pause_rect)
            screen.blit(pause_img, (0, 0))

        # Если игра окончена, выводим картинку и текст с победителем
        if game_over:
            screen.blit(gameover_img, (10, 100))
            winner_text = board.font2.render("Победил: " + winner, True, (255, 255, 255))
            screen.blit(winner_text, (gameover_img.get_width() + 20, 150))

        if pygame.mouse.get_focused():
            cursor_pos = pygame.mouse.get_pos()
            screen.blit(cursor_img, (cursor_pos[0], cursor_pos[1]))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
