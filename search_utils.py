#путь от старата до цели
def restore_path(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


# перебор шагов генератора
def search_result(steps):
    for step in steps:
        if step["type"] == "found":
            return step["path"], step["cost"]
    return None, None
