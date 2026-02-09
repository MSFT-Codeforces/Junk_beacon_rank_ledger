"""
Compute a permutation of ranks satisfying directed difference constraints
on a connected graph, or print -1 if impossible.
"""

import sys
from collections import deque


def read_all_integers() -> list[int]:
    """Read all integers from standard input efficiently.

    Returns:
        A list of integers in the order they appear in the input.
    """
    data = sys.stdin.buffer.read()
    numbers: list[int] = []

    current_value = 0
    current_sign = 1
    in_number = False

    for byte_value in data:
        if 48 <= byte_value <= 57:
            current_value = current_value * 10 + (byte_value - 48)
            in_number = True
            continue

        if byte_value == 45:
            current_sign = -1
            continue

        if in_number:
            numbers.append(current_sign * current_value)
            current_value = 0
            current_sign = 1
            in_number = False

    if in_number:
        numbers.append(current_sign * current_value)

    return numbers


def compute_shadow_values(
    vertex_count: int,
    adjacency_list: list[list[tuple[int, int]]],
) -> tuple[bool, list[int]]:
    """Compute shadow values satisfying all difference constraints.

    The adjacency list contains entries (v, delta) meaning s[v] = s[u] + delta.

    Args:
        vertex_count: Number of vertices n.
        adjacency_list: Graph representation with directed delta constraints.

    Returns:
        A pair (is_consistent, shadow_values).
        If is_consistent is False, shadow_values is empty.
        Otherwise shadow_values has length n+1 (index 0 unused).
    """
    shadow_values = [0] * (vertex_count + 1)
    visited = [False] * (vertex_count + 1)

    visited[1] = True
    shadow_values[1] = 0
    bfs_queue = deque([1])

    while bfs_queue:
        current_vertex = bfs_queue.popleft()
        current_shadow = shadow_values[current_vertex]

        for neighbor_vertex, delta in adjacency_list[current_vertex]:
            expected_shadow = current_shadow + delta

            if not visited[neighbor_vertex]:
                visited[neighbor_vertex] = True
                shadow_values[neighbor_vertex] = expected_shadow
                bfs_queue.append(neighbor_vertex)
                continue

            if shadow_values[neighbor_vertex] != expected_shadow:
                return False, []

    if not all(visited[1:]):
        return False, []

    return True, shadow_values


def main() -> None:
    """Read input, solve the constraints, and print the required output."""
    input_numbers = read_all_integers()
    if len(input_numbers) < 2:
        return

    vertex_count = input_numbers[0]
    edge_count = input_numbers[1]

    adjacency_list: list[list[tuple[int, int]]] = []
    for _ in range(vertex_count + 1):
        adjacency_list.append([])

    position = 2
    for _ in range(edge_count):
        from_vertex = input_numbers[position]
        to_vertex = input_numbers[position + 1]
        difference = input_numbers[position + 2]
        position += 3

        adjacency_list[from_vertex].append((to_vertex, difference))
        adjacency_list[to_vertex].append((from_vertex, -difference))

    is_consistent, shadow_values = compute_shadow_values(
        vertex_count,
        adjacency_list,
    )
    if not is_consistent:
        sys.stdout.write("-1")
        return

    shadow_list = shadow_values[1:]
    minimum_shadow = min(shadow_list)
    maximum_shadow = max(shadow_list)

    if maximum_shadow - minimum_shadow != vertex_count - 1:
        sys.stdout.write("-1")
        return

    if len(set(shadow_list)) != vertex_count:
        sys.stdout.write("-1")
        return

    shift = 1 - minimum_shadow
    ranks = [value + shift for value in shadow_list]

    sys.stdout.write(" ".join(map(str, ranks)))


if __name__ == "__main__":
    main()