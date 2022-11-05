import os
from typing import NamedTuple

import numpy as np
from tabulate import tabulate


# TODO: Create a nice grid class
# TODO: Create a separate game class

class Dimensions(NamedTuple):
    x: int
    y: int


class Position(NamedTuple):
    x: int
    y: int


def generate_grid_zeroes(dims: Dimensions) -> np.array:
    return np.repeat([0], dims.x * dims.y).reshape(dims.x, dims.y)


def generate_start_grid(dims: Dimensions, non_zero_index: np.array) -> np.array:
    in_grid = generate_grid_zeroes(dims)
    for i, j in non_zero_index:
        in_grid[i, j] = 1
    return in_grid


def add_borders(grid: np.array) -> np.array:
    dims = Dimensions(grid.shape[0] + 2, grid.shape[1] + 2)
    border_grid = generate_grid_zeroes(dims)
    border_grid[1 : dims.x - 1, 1 : dims.y - 1] = grid
    return border_grid

# TODO: Sort out type error
def count_neighbours(grid: np.array, pos: Position) -> int:
    if pos.x < 1 or pos.y < 1 or pos.x == grid.shape[0] or pos.y == grid.shape[1]:
        raise ValueError("The inputted element must have 9 surrounding elements")

    # TODO: make this tidier
    surrounding_elements = np.concatenate(
        [
            list(grid[pos.x - 1, pos.y - 1 : pos.y + 2]),
            list([grid[pos.x, pos.y - 1]]),
            list(grid[pos.x + 1, pos.y - 1 : pos.y + 2]),
            list([grid[pos.x, pos.y + 1]]),
        ]
    ).ravel()
    count = np.sum(surrounding_elements, axis=None, dtype=int)
    return count


def get_sum_neighbours_grid(grid: np.array) -> np.array:
    sum_grid = add_borders(grid)
    dims = Dimensions(sum_grid.shape[0], sum_grid.shape[1])
    output_grid = grid.copy()
    for i in range(1, dims.x - 1):
        for j in range(1, dims.y - 1):
            pos = Position(i, j)
            n_neighbours = count_neighbours(sum_grid, pos)
            output_grid[i - 1, j - 1] = n_neighbours
    return output_grid


def check_rules(grid: np.array, sum_grid: np.array) -> np.array:
    output_grid = grid.copy()
    mask = grid == 1
    live_cells_index = np.where(mask)
    dead_cells_index = np.where(~mask)
    # TODO: rename these variables
    live_live_cells = (
        (sum_grid[live_cells_index] == 2) | (sum_grid[live_cells_index] == 3)
    ).astype(int)
    output_grid[live_cells_index] = live_live_cells
    live_dead_cells = (sum_grid[dead_cells_index] == 3).astype(int)
    output_grid[dead_cells_index] = live_dead_cells
    return output_grid

# TODO: Implement matplotlib animation
def run_game(grid: np.array, iterations: int) -> np.array:
    clear = lambda: os.system("cls")
    tab_grid = tabulate(grid)
    print(tab_grid)
    clear()

    for i in range(iterations):
        sum_grid = get_sum_neighbours_grid(grid)
        grid = check_rules(grid, sum_grid)
        tab_grid = tabulate(grid)
        print(tab_grid)
        clear()
    return grid
