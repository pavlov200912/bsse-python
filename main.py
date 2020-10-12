"""Array class realisation with tuples inside. Education purpose."""


class Array(object):
    """Class copy list functionality, but with tuples inside."""

    def __init__(self, *initial_array):
        self._data = tuple(initial_array)

    def append(self, elem):
        self._data = self._data + (elem,)

    def __add__(self, other):
        if not isinstance(other, Array):
            raise TypeError
        return Array(*(list(self) + list(other)))

    def __len__(self):
        return len(self._data)

    def index(self, value):
        try:
            return self._data.index(value)
        except ValueError:
            return -1

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, item):
        return self._data[item]

    def pop(self, index):
        # index assumed to be > 0
        if index >= len(self) or index < 0:
            raise IndexError
        value = self._data[index]
        self._data = self._data[:index] + self._data[index + 1:]
        return value

    def remove(self, value):
        index_to_pop = -1
        for index, cur_value in enumerate(self._data):
            if cur_value == value:
                index_to_pop = index
                break
        if index_to_pop == -1:
            raise ValueError
        return self.pop(index_to_pop)

    def __eq__(self, other):
        if not isinstance(other, Array):
            return False
        if len(other) != len(self):
            return False
        return all(a == b for a, b in zip(self, other))
