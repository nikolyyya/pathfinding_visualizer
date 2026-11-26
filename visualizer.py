import pygame

import settings

LEGEND = {
    "EMPTY": "Пустая",
    "WALL": "Стена",
    "START": "Старт",
    "GOAL": "Цель",
    "OPEN": "В очереди",
    "CLOSED": "Обработана",
    "PATH": "Путь",
    "WEIGHTED": "Стоимость 5",
}


def create_fonts():
    font_path = pygame.font.match_font("dejavusans,arial")
    return {
        "big": pygame.font.Font(font_path, settings.FONT_BIG_SIZE),
        "small": pygame.font.Font(font_path, settings.FONT_SMALL_SIZE),
        "tiny": pygame.font.Font(font_path, settings.FONT_TINY_SIZE),
    }


def create_zones():
    grid = pygame.Rect(24, 68, settings.COLS * settings.CELL_SIZE, settings.ROWS * settings.CELL_SIZE)
    panel_left = grid.right + 24
    return {
        "grid": grid,
        "panel": pygame.Rect(panel_left, grid.top, settings.WIDTH - panel_left - 24, grid.height),
    }


def draw_text(screen, font, text, position, color=settings.TEXT_COLOR):
    screen.blit(font.render(text, True, color), position)


def draw_grid(screen, font, area, search):
    grid = search.grid
    size = settings.CELL_SIZE
    markers = {
        "S": font.render("S", True, (255, 255, 255)),
        "G": font.render("G", True, (255, 255, 255)),
        "5": font.render("5", True, settings.TEXT_COLOR),
    }
    pygame.draw.rect(screen, settings.GRID_COLOR, area)
    for row, cells in enumerate(grid.cells):
        for col, base in enumerate(cells):
            node = (row, col)
            state = base
            marker = "5" if base == "WEIGHTED" else None
            if node == grid.start:
                state, marker = "START", "S"
            elif node == grid.goal:
                state, marker = "GOAL", "G"
            elif node in search.path_nodes:
                state = "PATH"
            elif node in search.closed_nodes:
                state = "CLOSED"
            elif node in search.open_nodes:
                state = "OPEN"

            rect = pygame.Rect(area.left + col * size, area.top + row * size, size - 1, size - 1)
            pygame.draw.rect(screen, settings.CELL_COLORS[state], rect)
            if marker:
                image = markers[marker]
                screen.blit(image, image.get_rect(center=rect.center))

    pygame.draw.rect(screen, settings.BORDER_COLOR, area, 1)


def draw_panel(screen, fonts, panel, search, algorithm_name):
    pygame.draw.rect(screen, settings.PANEL_COLOR, panel)
    pygame.draw.rect(screen, settings.BORDER_COLOR, panel, 1)
    x = panel.left + 17
    y = panel.top
    draw_text(screen, fonts["tiny"], "Алгоритм", (x, y + 16), settings.MUTED_COLOR)
    draw_text(screen, fonts["big"], algorithm_name, (x, y + 34))
    pygame.draw.line(screen, settings.BORDER_COLOR, (x, y + 80), (panel.right - 17, y + 80))

    stats = (
        ("Посещено клеток", len(search.closed_nodes)),
        ("Длина пути", search.path_length),
        ("Стоимость пути", search.path_cost),
        ("Шаги", search.steps),
    )
    for index, (label, value) in enumerate(stats):
        line_y = y + 97 + index * 26
        draw_text(screen, fonts["tiny"], label, (x, line_y))
        value_text = "—" if value is None else str(value)
        image = fonts["tiny"].render(value_text, True, settings.TEXT_COLOR)
        screen.blit(image, image.get_rect(topright=(panel.right - 17, line_y)))

    draw_text(screen, fonts["tiny"], "Состояние", (x, y + 207), settings.MUTED_COLOR)
    draw_text(screen, fonts["small"], search.status, (x, y + 226))
    pygame.draw.line(screen, settings.BORDER_COLOR, (x, y + 264), (panel.right - 17, y + 264))

    draw_text(screen, fonts["small"], "Управление", (x, y + 279))
    controls = (
        "1 / 2 / 3 — алгоритм",
        "Пробел — старт / пауза",
        "N — один шаг",
        "R — сброс результата",
        "C — очистить карту",
        f"↑ / ↓ — скорость {search.speed + 1}/{len(settings.STEP_DELAYS)}",
        "Esc — выход",
    )
    for index, text in enumerate(controls):
        draw_text(screen, fonts["tiny"], text, (x, y + 310 + index * 21))

    draw_text(screen, fonts["small"], "Редактирование", (x, y + 465))
    mouse = (
        "ЛКМ — стена",
        "ПКМ — убрать стену / вес",
        "S/G + ЛКМ — старт / цель",
        "W + ЛКМ — вес 5",
    )
    for index, text in enumerate(mouse):
        draw_text(screen, fonts["tiny"], text, (x, y + 496 + index * 21))


def draw_legend(screen, font, y):
    column_width = (settings.WIDTH - 48) // len(LEGEND)
    for index, (state, label) in enumerate(LEGEND.items()):
        x = 24 + index * column_width
        swatch = pygame.Rect(x, y, 17, 17)
        pygame.draw.rect(screen, settings.CELL_COLORS[state], swatch)
        pygame.draw.rect(screen, settings.BORDER_COLOR, swatch, 1)
        draw_text(screen, font, label, (x + 24, y))


def draw(screen, fonts, zones, search, algorithm_name):
    screen.fill(settings.BG_COLOR)
    draw_text(screen, fonts["big"], "Визуализация поиска пути", (24, 17))
    draw_grid(screen, fonts["tiny"], zones["grid"], search)
    draw_panel(screen, fonts, zones["panel"], search, algorithm_name)
    draw_legend(screen, fonts["tiny"], zones["grid"].bottom + 28)
