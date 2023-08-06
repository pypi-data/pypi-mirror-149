#!/usr/bin/env python3

import pytest
from pytest import raises
from hypothesis import given
from hypothesis.strategies import integers
from wellmap import *

@pytest.mark.parametrize(
        'row, col, well', [
            ('A', 1, 'A1'),
            ('A', '1', 'A1'),
            ('A', '01', 'A1'),
])
def test_well_from_row_col(row, col, well):
    assert well_from_row_col(row, col) == well

@pytest.mark.parametrize(
        'i, j, well', [
            (0, 0, 'A1'),
            (0, 1, 'A2'),
            (1, 0, 'B1'),
            (1, 1, 'B2'),
])
def test_well_from_ij(i, j, well):
    assert well_from_ij(i, j) == well

@pytest.mark.parametrize(
        'well, digits, well0', [
            ('A1',  1, 'A1'),
            ('A1',  2, 'A01'),
            ('A1',  3, 'A001'),
            ('A01', 1, 'A1'),
            ('A01', 2, 'A01'),
            ('A01', 3, 'A001'),
])
def test_well0_from_well(well, digits, well0):
    assert well0_from_well(well, digits) == well0

@pytest.mark.parametrize(
        'row, col, digits, well0', [
            ('A', '1',  1, 'A1'),
            ('A', '1',  2, 'A01'),
            ('A', '1',  3, 'A001'),
            ('A', '01', 1, 'A1'),
            ('A', '01', 2, 'A01'),
            ('A', '01', 3, 'A001'),
])
def test_well0_from_row_col(row, col, digits, well0):
    assert well0_from_row_col(row, col, digits) == well0

@pytest.mark.parametrize(
        'i, j, row, col', [
            (0, 0, 'A', '1'),
            (0, 1, 'A', '2'),
            (1, 0, 'B', '1'),
            (1, 1, 'B', '2'),
])
def test_row_col_from_ij(i, j, row, col):
    assert row_col_from_ij(i, j) == (row, col)

@pytest.mark.parametrize(
        'i, j', [
            (-1, 0),
            (0, -1),
])
def test_row_col_from_ij_err(i, j):
    with pytest.raises(LayoutError):
        row_col_from_ij(i, j)

@pytest.mark.parametrize(
        'well, row, col', [
            ('A1', 'A', '1'),
            ('A2', 'A', '2'),
            ('B1', 'B', '1'),
            ('B2', 'B', '2'),

            ('A01', 'A', '1'),
            ('A02', 'A', '2'),
            ('B01', 'B', '1'),
            ('B02', 'B', '2'),

            ('AA1', 'AA', '1'),
            ('AA2', 'AA', '2'),
            ('BB1', 'BB', '1'),
            ('BB2', 'BB', '2'),

            ('AA01', 'AA', '1'),
            ('AA02', 'AA', '2'),
            ('BB01', 'BB', '1'),
            ('BB02', 'BB', '2'),
])
def test_row_col_from_well(well, row, col):
    assert row_col_from_well(well) == (row, col)

@pytest.mark.parametrize(
        'well', ['XXX', '123', '1A']
)
def test_row_col_from_well_err(well):
    with raises(LayoutError, match=well):
        row_col_from_well(well)

@pytest.mark.parametrize(
        'i, row', [
            (0, 'A'),
            (1, 'B'),

            (25, 'Z'),
            (26, 'AA'),
            (27, 'AB'),

            (51, 'AZ'),
            (52, 'BA'),
            (53, 'BB'),
])
def test_i_from_row(i, row):
    assert i_from_row(row.upper()) == i
    assert i_from_row(row.lower()) == i
    assert row_from_i(i) == row

@pytest.mark.parametrize(
        'row', ['', '1', 'A1']
)
def test_i_from_row_err(row):
    with raises(LayoutError):
        i_from_row(row)

@pytest.mark.parametrize(
        'j, col', [
            (0, '1'),
            (1, '2'),
])
def test_j_from_col(j, col):
    assert j_from_col(col) == j
    assert j_from_col(f'0{col}') == j
    assert col_from_j(j) == col

@pytest.mark.parametrize(
        'col', ['', 'A', 'A1']
)
def test_j_from_col_err(col):
    with raises(LayoutError):
        j_from_col(col)

@pytest.mark.parametrize(
        'well, i, j', [
            ('A1', 0, 0),
            ('A2', 0, 1),
            ('B1', 1, 0),
            ('B2', 1, 1),

            ('A01', 0, 0),
            ('A02', 0, 1),
            ('B01', 1, 0),
            ('B02', 1, 1),
])
def test_ij_from_well(well, i, j):
    assert ij_from_well(well) == (i, j)

@pytest.mark.parametrize(
        'row, col, i, j', [
            ('A', '1', 0, 0),
            ('A', '2', 0, 1),
            ('B', '1', 1, 0),
            ('B', '2', 1, 1),

            ('A', '01', 0, 0),
            ('A', '02', 0, 1),
            ('B', '01', 1, 0),
            ('B', '02', 1, 1),
])
def test_ij_from_row_col(row, col, i, j):
    assert ij_from_row_col(row, col) == (i, j)

@pytest.mark.parametrize(
        'a, b, x', [
            (0, 0, 0), (1, 0, 1), (2, 0, 2), (3, 0, 3),
            (0, 1, 1), (1, 1, 0), (2, 1, 3), (3, 1, 2),
            (0, 2, 0), (1, 2, 1), (2, 2, 2), (3, 2, 3),
            (0, 3, 1), (1, 3, 0), (2, 3, 3), (3, 3, 2),
])
def test_interleave(a, b, x):
    assert interleave(a, b) == x

@given(integers(), integers())
def test_interleave_is_its_own_inverse(a, b):
    assert interleave(interleave(a, b), b) == a

@pytest.mark.parametrize(
        'x0, x1, xn, single_step_ok', [
            (0, None, 1, False),
            (0, None, 2, False),
            (0, 1, 2, False),
            (0, 1, 3, False),
            (0, 2, 4, False),
            (0, 2, 6, False),

            (0, None, 0, True),
            (0, None, 1, True),
            (0, 1, 1, True),
            (0, 1, 2, True),
            (0, 1, 3, True),
            (0, 2, 4, True),
            (0, 2, 6, True),
])
def test_check_range(x0, x1, xn, single_step_ok):
    check_range(x0, x1, xn, single_step_ok)

@pytest.mark.parametrize(
        'x0, x1, xn, single_step_ok, err', [
            (0, None, 0, False, r"Expected {first} < {last}"),
            (1, None, 0, False, r"Expected {first} < {last}"),

            (0, 0, 0, False, r"Expected {first} < {second} < {last}"),
            (0, 0, 1, False, r"Expected {first} < {second} < {last}"),
            (0, 1, 0, False, r"Expected {first} < {second} < {last}"),
            (0, 1, 1, False, r"Expected {first} < {second} < {last}"),
            (1, 1, 1, False, r"Expected {first} < {second} < {last}"),
            (0, 2, 1, False, r"Expected {first} < {second} < {last}"),

            (0, 2, 3, False, r"Cannot get from {first} to {last} in steps of 2"),
            (0, 2, 5, False, r"Cannot get from {first} to {last} in steps of 2"),
            (0, 3, 5, False, r"Cannot get from {first} to {last} in steps of 3"),
])
def test_check_range_err(x0, x1, xn, single_step_ok, err):
    with raises(LayoutError, match=err):
        check_range(x0, x1, xn, single_step_ok)

@pytest.mark.parametrize(
        'x0, x1, xn, expected', [
            (0, 1, 1, [0, 1]),
            (0, 1, 2, [0, 1, 2]),
            (0, 2, 2, [0, 2]),
            (0, 2, 4, [0, 2, 4]),
])
def test_inclusive_range(x0, x1, xn, expected):
    assert list(inclusive_range(x0, x1, xn)) == expected

@pytest.mark.parametrize(
        'xs, expected', [
            ([], []),
            ([1], [1]),
            ([1,2], [1,2]),
            ([2,1], [1,2]),
            ([1,3], [1,2,3]),
            ([3,1], [1,2,3]),
        ]
)
def test_range_from_indices(xs, expected):
    actual = util.range_from_indices(*xs)
    assert list(actual) == expected

@pytest.mark.parametrize(
        'key, indices', [
            # A B C D E F G H
            # 0 1 2 3 4 5 6 7

            ('A', [0]),
            ('B', [1]),

            ('A,B', [0, 1]),
            ('B,C', [1, 2]),

            ('A-B', [0, 1]),
            ('A-C', [0, 1, 2]),
            ('B-C', [1, 2]),
            ('B-D', [1, 2, 3]),

            ('A,C-E', [0,2,3,4]),
            ('A-C,E', [0,1,2,4]),
            ('A-C,E-G', [0,1,2,4,5,6]),

            ('A,B,...,C', [0,1,2]),
            ('A,B,...,D', [0,1,2,3]),
            ('A,C,...,E', [0,2,4]),
            ('A,C,...,G', [0,2,4,6]),

            ('B,C,...,D', [1,2,3]),
            ('B,C,...,E', [1,2,3,4]),
            ('B,D,...,F', [1,3,5]),
            ('B,D,...,H', [1,3,5,7]),
])
def test_iter_row_indices(key, indices):
    assert list(iter_row_indices(key)) == indices

@pytest.mark.parametrize(
        'key, err', [
            ('1', "Cannot parse row '1'"),

            ('1-2', "Cannot parse row '1'"),
            ('A-B-C', "Expected '<first>-<last>', not 'A-B-C'"),
            ('A-A', "'A-A': Expected A < A"),
            ('B-A', "'B-A': Expected B < A"),

            ('1,2,...,3', "Cannot parse row '1'"),
            ('A,...,B,D', "Expected '<first>,<second>,...,<last>', not 'A,...,B,D'"),
            ('A,B,...,B', "'A,B,...,B': Expected A < B < B"),
            ('A,C,...,D', "'A,C,...,D': Cannot get from A to D in steps of 2"),
])
def test_iter_row_indices_err(key, err):
    with raises(LayoutError, match=err):
        list(iter_row_indices(key))

@pytest.mark.parametrize(
        'key, indices', [
            ('1', [0]),
            ('2', [1]),

            ('1,2', [0, 1]),
            ('2,3', [1, 2]),

            ('1-2', [0, 1]),
            ('1-3', [0, 1, 2]),
            ('2-3', [1, 2]),
            ('2-4', [1, 2, 3]),

            ('1,3-5', [0,2,3,4]),
            ('1-3,5', [0,1,2,4]),
            ('1-3,5-7', [0,1,2,4,5,6]),

            ('1,2,...,3', [0,1,2]),
            ('1,2,...,4', [0,1,2,3]),
            ('1,3,...,5', [0,2,4]),
            ('1,3,...,7', [0,2,4,6]),

            ('2,3,...,4', [1,2,3]),
            ('2,3,...,5', [1,2,3,4]),
            ('2,4,...,6', [1,3,5]),
            ('2,4,...,8', [1,3,5,7]),
])
def test_iter_col_indices(key, indices):
    assert list(iter_col_indices(key)) == indices

@pytest.mark.parametrize(
        'key, err', [
            ('A', "Cannot parse column 'A'"),

            ('A-B', "Cannot parse column 'A'"),
            ('1-2-3', "Expected '<first>-<last>', not '1-2-3'"),
            ('1-1', "'1-1': Expected 1 < 1"),
            ('2-1', "'2-1': Expected 2 < 1"),

            ('A,B,...,C', "Cannot parse column 'A'"),
            ('1,...,2,4', "Expected '<first>,<second>,...,<last>', not '1,...,2,4'"),
            ('1,2,...,2', "'1,2,...,2': Expected 1 < 2 < 2"),
            ('1,3,...,4', "'1,3,...,4': Cannot get from 1 to 4 in steps of 2"),
])
def test_iter_col_indices_err(key, err):
    with raises(LayoutError, match=err):
        list(iter_col_indices(key))

@pytest.mark.parametrize(
        'key, indices', [
            ('A1', {(0,0)}),
            ('B2', {(1,1)}),

            ('A1,A2', {(0,0), (0,1)}),
            ('B2,B3', {(1,1), (1,2)}),

            # Single row
            ('A1-A2', {(0,0),(0,1)}),
            ('A1-A3', {(0,0),(0,1),(0,2)}),
            ('B2-B3', {(1,1),(1,2)}),
            ('B2-B4', {(1,1),(1,2),(1,3)}),

            ('A1,A2,...,A3', {(0,0),(0,1),(0,2)}),
            ('A1,A2,...,A4', {(0,0),(0,1),(0,2),(0,3)}),
            ('A1,A3,...,A5', {(0,0),(0,2),(0,4)}),
            ('A1,A3,...,A7', {(0,0),(0,2),(0,4),(0,6)}),

            ('B2,B3,...,B4', {(1,1),(1,2),(1,3)}),
            ('B2,B3,...,B5', {(1,1),(1,2),(1,3),(1,4)}),
            ('B2,B4,...,B6', {(1,1),(1,3),(1,5)}),
            ('B2,B4,...,B8', {(1,1),(1,3),(1,5),(1,7)}),

            # Single column
            ('A1-B1', {(0,0),(1,0)}),
            ('A1-C1', {(0,0),(1,0),(2,0)}),
            ('B2-C2', {(1,1),(2,1)}),
            ('B2-D2', {(1,1),(2,1),(3,1)}),

            ('A1,B1,...,C1', {(0,0),(1,0),(2,0)}),
            ('A1,B1,...,D1', {(0,0),(1,0),(2,0),(3,0)}),
            ('A1,C1,...,E1', {(0,0),(2,0),(4,0)}),
            ('A1,C1,...,G1', {(0,0),(2,0),(4,0),(6,0)}),

            ('B2,C2,...,D2', {(1,1),(2,1),(3,1)}),
            ('B2,C2,...,E2', {(1,1),(2,1),(3,1),(4,1)}),
            ('B2,D2,...,F2', {(1,1),(3,1),(5,1)}),
            ('B2,D2,...,H2', {(1,1),(3,1),(5,1),(7,1)}),

            # Rows and columns
            ('A1-B2', {(0,0),(0,1),(1,0),(1,1)}),
            ('B2-C3', {(1,1),(1,2),(2,1),(2,2)}),

            ('A1,B1-B3', {(0,0),(1,0),(1,1),(1,2)}),
            ('A1-A3,B1', {(0,0),(0,1),(0,2),(1,0)}),
            ('A1-B2,A5-B6', {(0,0),(0,1),(1,0),(1,1),(0,4),(0,5),(1,4),(1,5)}),

            ('A1,B2,...,B2', {(0,0),(0,1),(1,0),(1,1)}),
            ('B2,C3,...,C3', {(1,1),(1,2),(2,1),(2,2)}),
            ('A1,C3,...,C5', {(0,0),(0,2),(0,4),(2,0),(2,2),(2,4)}),
            ('A1,C3,...,E3', {(0,0),(0,2),(2,0),(2,2),(4,0),(4,2)}),
])
def test_iter_well_indices(key, indices):
    assert set(iter_well_indices(key)) == indices

@pytest.mark.parametrize(
        'key, err', [
            ('A', "Cannot parse well 'A'"),
            ('1', "Cannot parse well '1'"),

            ('A-B', "Cannot parse well 'A'"),
            ('1-2', "Cannot parse well '1'"),
            ('A1-A2-A3', "Expected '<first>-<last>', not 'A1-A2-A3'"),
            ('A1-A1', "'A1-A1': Expected A1 < A1"),
            ('A2-A1', "'A2-A1': Expected A2 < A1"),
            ('B1-A1', "'B1-A1': Expected B1 < A1"),

            ('1,2,...,4', "Cannot parse well '1'"),
            ('A,B,...,D', "Cannot parse well 'A'"),
            ('A1,...,B2,D4', "Expected '<first>,<second>,...,<last>', not 'A1,...,B2,D4'"),
            ('A1,B1,...,B1', "'A1,B1,...,B1': Expected A1 < B1 < B1"),
            ('A1,A2,...,A2', "'A1,A2,...,A2': Expected A1 < A2 < A2"),
            ('A1,C3,...,D5', "'A1,C3,...,D5': Cannot get from A1 to D5 in steps of 2"),
            ('A1,C3,...,E4', "'A1,C3,...,E4': Cannot get from A1 to E4 in steps of 2"),
])
def test_iter_well_indices_err(key, err):
    with raises(LayoutError, match=err):
        list(iter_well_indices(key))
        
@pytest.mark.parametrize(
        'given, expected', [
            ('A1 to A1',  ( 0,  0)),
            ('A1 to A01', ( 0,  0)),
            
            ('A1 to B1',  ( 1,  0)),
            ('B1 to A1',  (-1,  0)),

            ('A1 to A2',  ( 0,  1)),
            ('A2 to A1',  ( 0, -1)),

            ('A1 to B2',  ( 1,  1)),
            ('B2 to A1',  (-1, -1)),

            ('A2 to B1',  ( 1, -1)),
            ('B1 to A2',  (-1,  1)),

        ],
)
def test_parse_shift(given, expected):
    assert parse_shift(given) == expected

@pytest.mark.parametrize(
        'given', [
            'A1 A2',
            'A to A2',
            'A1 to A',
            'A1 to 2A',
        ],
)
def test_parse_shift_err(given):
    with pytest.raises(LayoutError):
        parse_shift(given)

@pytest.mark.parametrize(
        'row_col, shift, expected', [
            ('A1', (0, 0), 'A1'),
            ('A1', (0, 1), 'A2'),
            ('A1', (1, 0), 'B1'),

            ('A', (0, 0), 'A'),
            ('A', (0, 1), 'A'),
            ('A', (1, 0), 'B'),

            ('1', (0, 0), '1'),
            ('1', (0, 1), '2'),
            ('1', (1, 0), '1'),
        ],
)
def test_shift_row_col(row_col, shift, expected):
    assert shift_row_col(row_col, shift) == expected

@pytest.mark.parametrize(
        'row_col, shift, ', [
            ('A1', (-1,  0)),
            ('A1', ( 0, -1)),
            ('A',  (-1,  0)),
            ('1',  ( 0, -1)),

            ('', (0, 0)),
            ('1A', (0, 0)),
        ],
)
def test_shift_row_col_err(row_col, shift):
    with pytest.raises(LayoutError):
        shift_row_col(row_col, shift)

@pytest.mark.parametrize(
        'key, shift, expected', [
            ('A1', (0, 0), 'A1'),
            ('A1', (0, 1), 'A2'),
            ('A1', (1, 0), 'B1'),

            ('A1,A2', (0, 0), 'A1,A2'),
            ('A1,A2', (0, 1), 'A2,A3'),
            ('A1,A2', (1, 0), 'B1,B2'),

            ('A1,A2,...,A4', (0, 0), 'A1,A2,...,A4'),
            ('A1,A2,...,A4', (0, 1), 'A2,A3,...,A5'),
            ('A1,A2,...,A4', (1, 0), 'B1,B2,...,B4'),

            ('A', (0, 0), 'A'),
            ('A', (0, 1), 'A'),
            ('A', (1, 0), 'B'),

            ('A,B', (0, 0), 'A,B'),
            ('A,B', (0, 1), 'A,B'),
            ('A,B', (1, 0), 'B,C'),

            ('A,B,...,D', (0, 0), 'A,B,...,D'),
            ('A,B,...,D', (0, 1), 'A,B,...,D'),
            ('A,B,...,D', (1, 0), 'B,C,...,E'),

            ('1', (0, 0), '1'),
            ('1', (0, 1), '2'),
            ('1', (1, 0), '1'),

            ('1,2', (0, 0), '1,2'),
            ('1,2', (0, 1), '2,3'),
            ('1,2', (1, 0), '1,2'),

            ('1,2,...,4', (0, 0), '1,2,...,4'),
            ('1,2,...,4', (0, 1), '2,3,...,5'),
            ('1,2,...,4', (1, 0), '1,2,...,4'),
        ],
)
def test_shift_key(key, shift, expected):
    assert shift_key(key, shift) == expected

@pytest.mark.parametrize(
        'a, b, expected', [
            ((0, 0), (0, 0), (0, 0)),
            ((0, 1), (0, 0), (0, 1)),
            ((1, 0), (0, 0), (1, 0)),
            ((0, 0), (0, 1), (0, 1)),
            ((0, 0), (1, 0), (1, 0)),
            ((1, 1), (1, 1), (2, 2)),
        ],
)
def test_add_shifts(a, b, expected):
    assert add_shifts(a, b) == expected

@pytest.mark.parametrize(
        'a, b, expected', [
            ((0, 0), (0, 0), (0, 0)),
            ((0, 1), (0, 0), (0, 1)),
            ((1, 0), (0, 0), (1, 0)),
            ((0, 0), (0, 1), (0, -1)),
            ((0, 0), (1, 0), (-1, 0)),
            ((1, 1), (1, 1), (0, 0)),
        ],
)
def test_sub_shifts(a, b, expected):
    assert sub_shifts(a, b) == expected

@pytest.mark.parametrize(
        'dict, func, level, expected', [
            pytest.param(
                {'a': 1},
                lambda x: x.upper(),
                0,
                {'A': 1},
                id='base case',
            ),
            pytest.param(
                {'a': 1, 'b': 2},
                lambda x: x.upper(),
                0,
                {'A': 1, 'B': 2},
                id='preserve order',
            ),
            pytest.param(
                {'b': 2, 'a': 1},
                lambda x: x.upper(),
                0,
                {'B': 2, 'A': 1},
                id='preserve order',
            ),
            pytest.param(
                {'a': {'b': {'c': 1}}},
                lambda x: x.upper(),
                0,
                {'A': {'b': {'c': 1}}},
                id='nested-0',
            ),
            pytest.param(
                {'a': {'b': {'c': 1}}},
                lambda x: x.upper(),
                1,
                {'a': {'B': {'c': 1}}},
                id='nested-1',
            ),
            pytest.param(
                {'a': {'b': {'c': 1}}},
                lambda x: x.upper(),
                2,
                {'a': {'b': {'C': 1}}},
                id='nested-2',
            ),
        ]
)
def test_map_keys(dict, func, level, expected):
    actual = map_keys(dict, func, level=level)

    assert actual == expected
    assert list(actual.keys()) == list(expected.keys())

@pytest.mark.parametrize(
        'dict, key, expected', [
            ({'a': 1}, 'a', 1),
            ({'a': {'b': 1}}, 'a', {'b': 1}),
            ({'a': {'b': 1}}, 'a.b', 1),
            ({'a': {'b': 1}}, 'a . b', 1),
        ]
)
def test_dotted_key(dict, key, expected):
    assert util.get_dotted_key(dict, key) == expected

@pytest.mark.parametrize(
        'dict, key', [
            ({}, 'a'),
            ({'a': 1}, 'b'),
            ({'a': {'b': 1}}, 'b'),
            ({'a': {'b': 1}}, 'a.c'),
        ]
)
def test_dotted_key_err(dict, key):
    with pytest.raises(KeyError, match=key.replace('.', r'\.')):
        util.get_dotted_key(dict, key)
