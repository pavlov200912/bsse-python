from hypothesis import given, example
import hypothesis.strategies as st
from main import Array
import random


@example(a=1, b=2, c=3)
@given(st.integers(), st.integers(), st.integers())
def test_index(a, b, c):
    is_distinct = (a != b) and (b != c) and (a != c)
    assert Array(a, b).index(c) == -1 or not is_distinct
    assert Array(a, b).index(a) == 0 or not is_distinct
    assert Array(a, b).index(b) == 1 or not is_distinct


@given(st.integers(), st.integers())
def test_iter(a, b):
    assert list(Array(a, a, a, a)) == [a, a, a, a]
    assert list(Array()) == []
    assert list(Array(a, b, b, a, b)) == [a, b, b, a, b]


@given(st.integers(), st.integers(), st.integers())
def test_equal_for_integers(a, b, c):
    assert Array(a, b, c) == Array(a, b, c)
    assert Array(a, b) == Array(a, b)
    assert Array(b, a) != Array(a, b) or a == b
    assert Array(a, b, c) != Array(c, b, a) or a == c


@given(st.integers())
def test_len(a):
    assert len(Array()) == 0
    assert len(Array(a)) == 1
    assert len(Array(a, a)) == 2
    assert len(Array(a, a, a)) == 3
    assert len(Array(a, a, a, a)) == 4
    assert len(Array(a, a, a, a, a)) == 5


@given(st.integers(), st.integers())
def test_get_item(a, b):
    assert Array(a, b)[0] == a
    assert Array(a, b)[1] == b
    assert Array(a)[0] == a

@given(st.integers(), st.integers())
def test_two_value_init_equals_append(x, y):
    array1 = Array(x, y)
    array2 = Array()
    array2.append(x)
    array2.append(y)
    assert array1 == array2


@given(st.integers())
def test_single_value_init_equals_append(x):
    array_with_x_appended = Array()
    array_with_x_appended.append(x)
    assert Array(x) == array_with_x_appended


@given(st.integers(), st.integers(), st.integers(), st.integers())
def test_add_arrays(a, b, c, d):
    assert Array(a) + Array(b) == Array(a, b)
    assert Array(a, b) + Array(c, d) == Array(a, b, c, d)
    assert Array() + Array(a, b, c, d) == Array(a, b, c, d)


@given(st.integers(), st.integers())
def test_pop(a, b):
    assert Array(a).pop(0) == a
    array_for_pop = Array(a, b)
    array_for_pop.pop(1)
    assert array_for_pop == Array(a)

@given(st.lists(st.integers(), min_size=1))
def test_pop_on_non_empty_lists(xs):
    random_index = random.choice(range(0, len(xs)))
    array = Array(*xs)
    array.pop(random_index)
    xs.pop(random_index)
    assert array == Array(*xs)

@given(st.integers(), st.integers())
def test_remove(a, b):
    array_for_remove = Array(a, b, b, b)
    array_for_remove.remove(b)
    assert array_for_remove == Array(a, b, b)

@given(st.lists(st.integers(), min_size=1))
def test_remove_on_non_empty_lists(xs):
    random_element = random.choice(xs)
    array = Array(*xs)
    array.remove(random_element)
    xs.remove(random_element)
    assert array == Array(*xs)
