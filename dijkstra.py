import heapq

from search_utils import restore_path, search_result

def dijkstra_steps(graph, start, goal):
    priority_queue = [(0, start)]
    distances = {start: 0}
    came_from = {}

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        if current_distance > distances[current]:
            continue
        if current == goal:
            path = restore_path(came_from, start, goal)
            yield {"type": "found", "node": current, "path": path, "cost": current_distance}
            return

        opened = []
        for neighbor, edge_cost in graph[current]:
            new_distance = current_distance + edge_cost
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                came_from[neighbor] = current
                heapq.heappush(priority_queue, (new_distance, neighbor))
                opened.append(neighbor)

        yield {"type": "visit", "node": current, "opened": opened}

    yield {"type": "not_found"}


def dijkstra(graph, start, goal):
    return search_result(dijkstra_steps(graph, start, goal))


if __name__ == "__main__":
    from test_graph import dijkstra_graph

    path, cost = dijkstra(dijkstra_graph, start="A", goal="E")
    print("Путь:", path)
    print("Стоимость:", cost)
