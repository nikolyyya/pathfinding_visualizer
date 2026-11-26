import pygame

import settings
import visualizer
from algorithms import astar_steps, bfs_steps, dijkstra_steps
from grid import Grid, build_graph

ALGORITHMS = {
    pygame.K_1: ("BFS", bfs_steps),
    pygame.K_2: ("Dijkstra", dijkstra_steps),
    pygame.K_3: ("A*", astar_steps),
}

READY = "Готово к запуску"
RUNNING = "Поиск идёт"
PAUSED = "Пауза"
FOUND = "Путь найден"
NOT_FOUND = "Path not found"


class Search:
    def __init__(self, grid):
        self.grid = grid
        self.algorithm = pygame.K_1
        self.speed = settings.DEFAULT_SPEED
        self.reset()

    def reset(self):
        self.generator = None
        self.open_nodes = set()
        self.closed_nodes = set()
        self.path_nodes = set()
        self.path_length = None
        self.path_cost = None
        self.steps = 0
        self.elapsed = 0
        self.status = READY

    def toggle(self):
        if self.status == RUNNING:
            self.status = PAUSED
        elif self.status in (READY, PAUSED):
            self.status = RUNNING
        self.elapsed = 0

    def step(self):
        if self.status in (FOUND, NOT_FOUND):
            return
        if self.generator is None:
            _, make_steps = ALGORITHMS[self.algorithm]
            graph = build_graph(self.grid, weighted=self.algorithm != pygame.K_1)
            self.generator = make_steps(graph, self.grid.start, self.grid.goal)
        if self.status == READY:
            self.status = PAUSED

        step = next(self.generator)
        if step["type"] == "not_found":
            self.status = NOT_FOUND
            self.generator = None
            return

        node = step["node"]
        self.steps += 1
        self.open_nodes.discard(node)
        self.closed_nodes.add(node)

        if step["type"] == "found":
            path = step["path"]
            self.path_nodes = set(path)
            self.path_length = len(path) - 1
            self.path_cost = sum(self.grid.cost(cell) for cell in path[1:])
            self.status = FOUND
            self.generator = None
        else:
            self.open_nodes.update(step["opened"])

    def update(self, dt):
        if self.status == RUNNING:
            self.elapsed += dt
            delay = settings.STEP_DELAYS[self.speed]
            if self.elapsed >= delay:
                self.elapsed -= delay
                self.step()

def handle_key(key, search):
    if key in ALGORITHMS:
        search.algorithm = key
        search.reset()
    elif key == pygame.K_SPACE:
        search.toggle()
    elif key == pygame.K_n:
        if search.status == RUNNING:
            search.toggle()
        search.step()
    elif key == pygame.K_r:
        search.reset()
    elif key == pygame.K_c:
        search.grid.clear()
        search.reset()
    elif key == pygame.K_UP:
        search.speed = min(search.speed + 1, len(settings.STEP_DELAYS) - 1)
    elif key == pygame.K_DOWN:
        search.speed = max(search.speed - 1, 0)


#клеткa под мышью и сбрасывает поиск при изменении карты.
def edit_at(position, button, area, search):
    if not area.collidepoint(position):
        return

    x, y = position
    node = ((y - area.top) // settings.CELL_SIZE, (x - area.left) // settings.CELL_SIZE)
    keys = pygame.key.get_pressed()
    if button == 3:
        state = "EMPTY"
    elif keys[pygame.K_s]:
        state = "START"
    elif keys[pygame.K_g]:
        state = "GOAL"
    elif keys[pygame.K_w]:
        state = "WEIGHTED"
    else:
        state = "WALL"

    if search.grid.edit(node, state):
        search.reset()

def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Поиск пути")
        clock = pygame.time.Clock()
        fonts = visualizer.create_fonts()
        zones = visualizer.create_zones()
        search = Search(Grid())

        while True:
            dt = clock.tick(settings.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    handle_key(event.key, search)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 3):
                    edit_at(event.pos, event.button, zones["grid"], search)
                elif event.type == pygame.MOUSEMOTION:
                    if event.buttons[0]:
                        edit_at(event.pos, 1, zones["grid"], search)
                    elif event.buttons[2]:
                        edit_at(event.pos, 3, zones["grid"], search)

            search.update(dt)
            algorithm_name, _ = ALGORITHMS[search.algorithm]
            visualizer.draw(screen, fonts, zones, search, algorithm_name)
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
