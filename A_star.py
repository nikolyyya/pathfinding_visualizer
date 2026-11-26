import heapq

from search_utils import restore_path, search_result


# Считает манхэттенское расстояние между двумя клетками.
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_steps(graph, start, goal):
    start_h = heuristic(start, goal)
    priority_queue = [(start_h, start_h, start)]
    g_score = {start: 0}
    came_from = {}

    while priority_queue:
        current_f, current_h, current = heapq.heappop(priority_queue)
        if current_f > g_score[current] + current_h:
            continue
        if current == goal:
            path = restore_path(came_from, start, goal)
            yield {"type": "found", "node": current, "path": path, "cost": g_score[current]}
            return

        opened = []
        for neighbor, edge_cost in graph[current]:
            new_g = g_score[current] + edge_cost
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                came_from[neighbor] = current
                h = heuristic(neighbor, goal)
                # При равном приоритете сначала берём клетку ближе к цели.
                heapq.heappush(priority_queue, (new_g + h, h, neighbor))
                opened.append(neighbor)

        yield {"type": "visit", "node": current, "opened": opened}

    yield {"type": "not_found"}

#со стоимостью
def astar(graph, start, goal):
    return search_result(astar_steps(graph, start, goal))


if __name__ == "__main__":
    from test_graph import A_star_graph

    path, cost = astar(A_star_graph, start=(0, 0), goal=(2, 2))
    print("Путь:", path)
    print("Стоимость:", cost)
