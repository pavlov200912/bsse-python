import functools


class ContractError(Exception):
    """We use this error when someone breaks our contract."""


#: Special value, that indicates that validation for this type is not required.
Any = object()


def contract(arg_types=None, return_type=None, raises=None):
    """
    Creates decorator that checks argument type, return type, raised exceptions restrictions

    :param arg_types: tuple with types of arguments or None, Any considered as common type for all objects
    :param return_type: type of returned by func value or None if it's not specified
    :param raises: tuple of Exception inheritors - restrictions on raised by func exceptions or None
    :return: parametrized decorator
    """
    def decorator(func):
        """
        :raises: ContactError if return, args type or called error is inconsistent with specified in contract
        """
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            if arg_types is not None:
                arg_values = list(args) + list(kwargs.values())
                if len(arg_values) != len(arg_types):
                    raise ContractError("Length of arg_types is inconsistent with function arguments")
                for arg_value, arg_type in zip(arg_values, arg_types):
                    if arg_type != Any and not isinstance(arg_value, arg_type):
                        raise ContractError("Can't match arg_value {0}"
                                            " of type {1} with type {2}".format(arg_value,
                                                                                type(arg_value),
                                                                                arg_type))
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if raises is None or isinstance(e, raises):
                    raise e
                else:
                    raise ContractError("Raise of {0} unexpected".format(e.__class__)) from e
            if return_type is not None and not isinstance(result, return_type):
                raise ContractError("Expected return type {0} but found {1}".format(return_type, type(result)))
            return result

        return wrapped

    return decorator