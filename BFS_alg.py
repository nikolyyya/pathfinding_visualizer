from collections import deque

from search_utils import restore_path, search_result

def bfs_steps(graph, start, goal):
    queue = deque([start])
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()
        if current == goal:
            path = restore_path(came_from, start, goal)
            yield {"type": "found", "node": current, "path": path, "cost": len(path) - 1}
            return

        opened = []
        for neighbor in graph[current]:
            if neighbor in visited:
                continue

            visited.add(neighbor)
            came_from[neighbor] = current
            queue.append(neighbor)
            opened.append(neighbor)

        yield {"type": "visit", "node": current, "opened": opened}

    yield {"type": "not_found"}


def bfs(graph, start, goal):
    path, _ = search_result(bfs_steps(graph, start, goal))
    return path


if __name__ == "__main__":
    from test_graph import BFS_graph

    print(bfs(BFS_graph, start="A", goal="G"))
