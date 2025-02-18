import pygame

# Размер окна
size = width, height = 1250, 600


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Состояние ячеек: 1 - пустая, 0 - занятая
        self.board = [[1] * width for _ in range(height)]
        self.board2 = [[1] * width for _ in range(height)]
        self.left = 50
        self.top = 50
        self.cell_size = 50

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
            self.board[y][x] = 1 - self.board[y][x]
            print(x, y)
        elif board_name == "board2":
            # Переключаем состояние ячейки на второй сетке
            self.board2[y][x] = 1 - self.board2[y][x]
            print(x + 10, y)

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            board_name, x, y = cell_coords
            self.on_click(board_name, x, y)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                # Рисуем первую сетку
                rect1 = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect1, 1)

                # Рисуем вторую сетку (со сдвигом вправо)
                rect2 = pygame.Rect(
                    self.left + x * self.cell_size + 13 * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect2, 1)



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Две сетки с кликами")
    board = Board(10, 10)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                board.get_click(pos)

        screen.fill((0, 0, 0))  # Очистка экрана черным цветом
        board.render(screen)   # Отрисовка сетки и состояния ячеек
        pygame.display.flip()  # Обновление экрана

    pygame.quit()