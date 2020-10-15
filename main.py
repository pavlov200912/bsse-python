"""Array class realisation with tuples inside. Education purpose."""


#  I understand that my documentation is excessive
#  I wouldn't add so many comments without linter


class Array(object):  # noqa: WPS214 I need more than 7 methods
    """Class copies list functionality, but with tuples inside."""

    def __init__(self, *initial_array):
        """Array can be initialized with sequence of arguments.

        :param initial_array: object that can be converted to tuple
        """
        self._data = tuple(initial_array)  # noqa: WPS110 I need _data variable

    def append(self, elem):
        """:param elem: object to add in Array."""
        self._data = self._data + (elem,)  # noqa: WPS110

    def __add__(self, other):
        """
        Concatenation of self and other.

        :raises TypeError: if other is not Array instance
        :param other: must be Array
        :return: new instance of Array
        """
        if not isinstance(other, Array):
            raise TypeError
        return Array(*(list(self) + list(other)))

    def __len__(self):
        """:return: length of Array."""
        return len(self._data)  # noqa: WPS110

    # Linter says 'value' is not appropriate variable name here. I think it is.
    def index(self, target_value):
        """
        Find index of value in Array.

        :param target_value: kek
        :return: index of element which equal to target_value
                 or -1 if it's not found.
        """
        try:
            return self._data.index(target_value)  # noqa: WPS110
        except ValueError:
            return -1

    def __iter__(self):
        """:yield: tuple iterator."""
        yield from self._data

    def __getitem__(self, key_item):
        """
         Tuple __getitem__ used. Can raise an exception.

        :param key_item: integer in range(0, len(self))
        :return: value with key_item index
        """
        return self._data[key_item]

    def pop(self, index):
        """
        Remove element by index and return it.

        :raises IndexError: if index in not appropriate range
        :param index: integer in range(0, len(self))
        :return: popped element of array
        """
        # index assumed to be > 0
        if index >= len(self) or index < 0:
            raise IndexError
        value_by_index = self._data[index]
        self._data = self._data[:index] + self._data[index + 1:]  # noqa:WPS110
        return value_by_index

    # Linter says 'value' is not appropriate variable name here. I think it is.
    def remove(self, value_to_remove):
        """
        Find first element equals to value_to_remove and pop it by index.

        :raises ValueError: if value_to_remove is not found
        :param value_to_remove: element of Array
        :return: removed value
        """
        index_to_pop = -1
        for index, cur_value in enumerate(self._data):
            if cur_value == value_to_remove:
                index_to_pop = index
                break
        if index_to_pop == -1:
            raise ValueError
        return self.pop(index_to_pop)

    def __eq__(self, other):
        """
        Object are equals if they are instances of Array with equal tuples.

        :param other: any object
        :return: boolean
        """
        if not isinstance(other, Array):
            return False
        if len(other) != len(self):
            return False
        return all(
            self_elem == other_elem
            for self_elem, other_elem in zip(self, other)
        )
