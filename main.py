import pygame
import sys
import os

# Размер окна
size = width, height = 1400, 800

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
        self.font_size = int(self.cell_size / 1.5)
        self.font = pygame.font.SysFont('notosans', self.font_size)
        self.pause = False  # Добавляем переменную pause в класс Board

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
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
                #pygame.draw.rect(screen, (0, 0, 255), ())


class Ships:
    def __init__(self, board):
        self.board = board
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.current_ship_index = 0
        self.hor_ver = 0  # 0 - горизонтально, 1 - вертикально
        self.current_ship = None
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.placed_ships = []
        self.create_next_ship()

    def create_next_ship(self):
        if self.current_ship_index < len(self.ships):
            ship_size = self.ships[self.current_ship_index]
            x = self.board.left
            y = self.board.height * self.board.cell_size + self.board.top + 20
            self.current_ship = pygame.Rect(x, y, ship_size * self.board.cell_size, self.board.cell_size)
        else:
            self.current_ship = None

    def draw_ships(self, screen):
        for ship in self.placed_ships:
            x = ship[0] // 50 - 2 # это точка в таблице board на которой стоит первая часть корабля
            y = ship[1] // 50 - 2 # это высота первой часть корабля
            # if self.hor_ver == 0:
            #     lenth = ship[2] // 50 - x + 1 # длинна размещённого корабля
            #     for i in range(lenth):
            #         board[y][x + i] = 1
            pygame.draw.rect(screen, (0, 255, 0), ship)  # Синий цвет для размещенных кораблей
        if self.current_ship:
            pygame.draw.rect(screen, (0, 0, 0), self.current_ship)  # Черный цвет для текущего корабля

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

    def snap_to_grid(self):
        grid_x = round(
            (self.current_ship.x - self.board.left) / self.board.cell_size) * self.board.cell_size + self.board.left
        grid_y = round(
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

    def reset_ship_position(self):
        self.current_ship.x = self.board.left
        self.current_ship.y = self.board.height * self.board.cell_size + self.board.top + 20


# Основной блок программы
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Морской бой")
    board = Board(10, 10)
    ships = Ships(board)

    # Загрузка изображения
    pause_img = board.load_image("pause.png")
    pause1 = pygame.transform.scale(pause_img, (50, 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Проверяем, был ли клик на кнопке паузы
                if 0 <= pos[0] <= 50 and 0 <= pos[1] <= 50:
                    board.pause = not board.pause  # Меняем состояние паузы
                    print("Пауза:", board.pause)
                else:
                    board.get_click(pos)
            ships.handle_event(event)

        screen.fill((200, 200, 200))
        board.render(screen)
        ships.draw_ships(screen)
        screen.blit(pause1, (0, 0))
        pygame.display.flip()  # Обновление экрана

    pygame.quit()