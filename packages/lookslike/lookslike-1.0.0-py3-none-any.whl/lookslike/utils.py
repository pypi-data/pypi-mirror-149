"""Convenience functions that can be used to convert values."""


def filter_keys(keys):
    """
    Restrict comparison of Dictionaries to the given keys.

    :param keys: The keys
    :type keys: list of str
    :return: Filter function that will return a dictionary that only contains the given keys.
    :rtype: Callable[[Dict], Dict]

    Example:
        {'a': 1, 'b': 2, 'c': 3} == Like({'a': 1, 'b': 2}, convert = utils.filter_keys(['a', 'b'])}
    """

    def _filter_keys(dictionary):
        assert isinstance(dictionary, dict)
        return {key: value for key, value in dictionary.items() if key in keys}

    return _filter_keys


def dict_keys_as_set():
    """
    Retrieve a set of dictionary keys. Use to check the presence of some keys in a dictionary without checking its
    contents.

    :return: Conversion function that will return a list of dict keys.
    :rtype: Callable[[Dict[str, Any]], Set[str]]

    Example:
        {'a': 1, 'b': 2} == Like({'a', 'b'}, convert = utils.dict_keys_as_set())
    """

    def _dict_keys_as_set(dictionary):
        return set(dictionary.keys())

    return _dict_keys_as_set


def is_truthy():
    """
    Ensure that a value is truthy.
    Will fail for [], {}, "", b"", 0, None, ...

    :return: Function that checks whether the given value is truthy.
    :rtype: Callable[[Any], bool]
    """

    def _is_truthy(value):
        return bool(value)

    return _is_truthy
