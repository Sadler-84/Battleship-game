import pygame
import sys
import os

# Размер окна
size = width, height = 1350, 900

clock = pygame.time.Clock()

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Состояние ячеек: 1 - пустая, 0 - занятая
        self.board = [[1] * width for _ in range(height)]
        self.board2 = [[1] * width for _ in range(height)]
        self.left = 100
        self.top = 100
        self.cell_size = 50
        self.font_size1 = int(self.cell_size / 1.5)
        self.font_size2 = int(self.cell_size * 2)
        self.font = pygame.font.SysFont('notosans', self.font_size1)
        self.font2 = pygame.font.SysFont(None, self.font_size2)
        self.pause = False  # Добавляем переменную pause в класс Board

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
            # Переключаем состояние ячейки (пустая/занятая)
            self.board[y][x] = 0 if self.board[y][x] == 1 else 1
            print(f"Клик по первой сетке: {x}, {y}")
        elif board_name == "board2":
            # Переключаем состояние ячейки (пустая/занятая)
            self.board2[y][x] = 0 if self.board2[y][x] == 1 else 1
            print(f"Клик по второй сетке: {x + 10}, {y}")

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            board_name, x, y = cell_coords
            self.on_click(board_name, x, y)

    def render(self, screen):
        letters = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И"]

        for y in range(self.height):
            for x in range(self.width):
                # Рисуем первую сетку
                rect1 = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (0, 0, 0), rect1, 1)

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

                # Цифры слева от таблицы 1
                screen.blit(num_ver,
                            (self.left - (self.cell_size // 2 + num_ver_width // 2),
                             self.top + y * self.cell_size + (self.cell_size // 2 - num_ver_height // 2))
                            )
                # Буквы над таблицей 1
                screen.blit(letters_hor,
                            (self.left + y * self.cell_size + self.cell_size // 2 - letters_hor_width // 2,
                             self.top - num_ver_height)
                            )

                # Цифры слева от таблицы 2
                screen.blit(num_ver,
                            (self.left - (self.cell_size // 2 + num_ver_width // 2) + self.cell_size * 13,
                             self.top + y * self.cell_size + (self.cell_size // 2 - num_ver_height // 2))
                            )
                # Буквы над таблицей 2
                screen.blit(letters_hor,
                            (self.left + y * self.cell_size +
                             self.cell_size // 2 - letters_hor_width // 2 +
                             self.cell_size * 13,
                             self.top - num_ver_height)
                            )


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
            ship_size = self.ships[self.current_ship_index]
            x = self.board.left * 2
            y = self.board.height * self.board.cell_size + self.board.top + 50

            # Создаем прямоугольник для корабля
            if self.hor_ver:
                self.current_ship = pygame.Rect(x, y, ship_size * self.board.cell_size, self.board.cell_size)
            else:
                self.current_ship = pygame.Rect(x, y, self.board.cell_size, ship_size * self.board.cell_size)
        else:
            self.current_ship = None

    def draw_ships(self, screen):
        for ship in self.placed_ships:
            pygame.draw.rect(screen, (0, 150, 0), ship)  # Зелёный цвет для размещенных кораблей
        if self.current_ship:
            pygame.draw.rect(screen, (70, 70, 70), self.current_ship)  # Серый цвет для текущего корабля

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
                self.snap_to_grid()
                if self.is_valid_placement():
                    self.placed_ships.append(self.current_ship.copy())
                    self.current_ship_index += 1
                    self.create_next_ship()
                else:
                    self.reset_ship_position()
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.current_ship.x = mouse_x + self.offset_x
                self.current_ship.y = mouse_y + self.offset_y

    def snap_to_grid(self):  # correcting ship place
        grid_x = round(  # left position in grid
            (self.current_ship.x - self.board.left) / self.board.cell_size) * self.board.cell_size + self.board.left
        grid_y = round(  # hight position for left part of ahip
            (self.current_ship.y - self.board.top) / self.board.cell_size) * self.board.cell_size + self.board.top
        self.current_ship.x = grid_x
        self.current_ship.y = grid_y

    def is_valid_placement(self):
        # Проверка, находится ли корабль в пределах игрового поля
        if (self.current_ship.left < self.board.left or
                self.current_ship.right > self.board.left + self.board.width * self.board.cell_size or
                self.current_ship.top < self.board.top or
                self.current_ship.bottom > self.board.top + self.board.height * self.board.cell_size):
            return False

        return True

    def reset_ship_position(self): # вернуть корабль на место(в начальное положение)
        ship_size = self.ships[self.current_ship_index]
        x = self.board.left * 2
        y = self.board.height * self.board.cell_size + self.board.top + 50

        if self.hor_ver:
            self.current_ship = pygame.Rect(x, y, ship_size * self.board.cell_size, self.board.cell_size)
        else:
            self.current_ship = pygame.Rect(x, y, self.board.cell_size, ship_size * self.board.cell_size)

    def toggle_orientation(self): # смена поворота корабля
        if self.current_ship is not None:
            ship_size = self.ships[self.current_ship_index]
            x = self.current_ship.x
            y = self.current_ship.y

            self.hor_ver = not self.hor_ver  # Переключаем ориентацию

            if self.hor_ver:
                self.current_ship = pygame.Rect(x, y, ship_size * self.board.cell_size, self.board.cell_size)
            else:
                self.current_ship = pygame.Rect(x, y, self.board.cell_size, ship_size * self.board.cell_size)


# Основной блок программы
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Морской бой")
    board = Board(10, 10)
    ships = Ships(board)

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
    turn_sprite.rect.x = (board.left)
    turn_sprite.rect.y = 650
    all_sprites.add(turn_sprite)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    board.pause = not board.pause
                    print("Пауза:", board.pause)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Проверяем, был ли клик на кнопке паузы
                if pause_sprite.rect.collidepoint(pos):
                    board.pause = not board.pause  # Меняем состояние паузы
                    print("Пауза:", board.pause)
                elif turn_sprite.rect.collidepoint(pos):
                    if board.pause is False:
                        ships.toggle_orientation()
                        print("Поворот: ", ships.hor_ver)
                else:
                    if board.pause is False:
                        board.get_click(pos)

            if not board.pause:
                ships.handle_event(event)

        if not board.pause:
            screen.fill((200, 200, 200))
            board.render(screen)
            ships.draw_ships(screen)
            all_sprites.draw(screen)
        else:
            rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (100, 100, 100, 15), (0, 0, width, height))
            screen.blit(rect_surface, (0, 0))
            pause_text = board.font2.render("Пауза", False, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(width // 2, height // 2 - 200))
            screen.blit(pause_text, pause_rect)

        pygame.display.flip()  # Обновление экрана

    pygame.quit()
