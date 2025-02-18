import pygame
size = width, height = 500, 500
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_x = (x - self.left) // self.cell_size
        cell_y = (y - self.top) // self.cell_size
        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            return cell_x, cell_y
        else:
            return None
    def on_click(self, cell_coords):
        x, y = cell_coords
        print(x, y)
    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords:
            self.on_click(cell_coords)
    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(
                    self.left + x * self.cell_size,
                    self.top + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    board = Board(20, 20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()