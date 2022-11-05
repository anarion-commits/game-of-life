import numpy as np
import pytest

from game import (
    generate_grid_zeroes,
    Dimensions,
    generate_start_grid,
    add_borders,
    get_sum_neighbours_grid,
    Position,
    count_neighbours,
    check_rules,
)

# TODO: Add more robust tests
# TODO: Add animation test
def test_generate_grid_zeroes():
    dims = Dimensions(4, 5)
    actual = generate_grid_zeroes(dims)
    expected = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    np.testing.assert_array_equal(expected, actual)


def test_generate_start_grid():
    dims = Dimensions(4, 5)
    non_zero_index = np.array([[0, 0], [2, 2], [3, 4]])
    actual = generate_start_grid(dims, non_zero_index)
    expected = np.array(
        [
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1],
        ]
    )
    np.testing.assert_array_equal(expected, actual)


def test_add_borders():
    dims = Dimensions(3, 3)
    non_zero_index = np.array([[1, 1]])
    in_grid = generate_start_grid(dims, non_zero_index)
    actual = add_borders(in_grid)
    expected = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    np.testing.assert_array_equal(actual, expected)


def test_count_neighbours():
    dims = Dimensions(5, 5)
    non_zero_index = np.array([[2, 2]])
    in_grid = generate_start_grid(dims, non_zero_index)
    pos = Position(2, 2)
    actual = count_neighbours(in_grid, pos)
    expected = 0
    assert actual == expected
    pos = Position(1, 1)
    actual = count_neighbours(in_grid, pos)
    expected = 1
    assert actual == expected
    with pytest.raises(
        ValueError, match="The inputted element must have 9 surrounding elements"
    ):
        pos = Position(0, 0)
        count_neighbours(in_grid, pos)


def test_sum_neighbours():
    dims = Dimensions(3, 3)
    non_zero_index = np.array([[1, 1]])
    in_grid = generate_start_grid(dims, non_zero_index)
    actual = get_sum_neighbours_grid(in_grid)
    expected = np.array(
        [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ]
    )
    np.testing.assert_array_equal(actual, expected)


def test_check_rules():
    # static
    in_grid = np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]])
    sum_grid = get_sum_neighbours_grid(in_grid)
    actual = check_rules(in_grid, sum_grid)
    expected = in_grid
    np.testing.assert_array_equal(actual, expected)

    # oscillator
    in_grid = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    sum_grid = get_sum_neighbours_grid(in_grid)
    actual = check_rules(in_grid, sum_grid)
    expected = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
    )
    np.testing.assert_array_equal(actual, expected)
