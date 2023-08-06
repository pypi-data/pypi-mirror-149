import re


if hasattr(re, 'Pattern'):  # >Py3.6
    def is_regex_pattern(obj):
        return isinstance(obj, re.Pattern)
else:  # <=Py3.6
    def is_regex_pattern(obj):
        return "SRE_Pattern" in str(type(obj))

NEVER_COMPARED = object()


class Like:
    """
    Compare an object with something which is similar (or equal) to it.

    :param args: One or multiple criteria that have to match.
                 For example: 42 == Like(42, int, re.compile("4."), lambda v: v == 42)
    :type args: type | Callable[[Any], bool] | re.Pattern | Any
    :param convert: Optional: A function to convert the comparison value before
    matching.
                    For example: [3, 2, 1] == Like([1, 2, 3], convert=sorted)
    :type convert: Callable[[Any], Any]

    Example:
        42 == Like(int)  # -> True

        "http://some.url" == Like(re.compile("http://.*")  # -> True

        10 == Like(lambda v: 9 < v < 11)  # -> True

        {'num': 42, 'alpha': 'abcd'} == {'num': Like(int), 'alpha': Like(str)} # -> True
    """

    def __init__(self, *args, convert=None):
        self._comparison_values = args
        self._convert = convert
        self._comparison_falsy = False
        self._last_compared_value = NEVER_COMPARED

    def __eq__(self, other):
        self._last_compared_value = other
        for comparison_value in self._comparison_values:
            if not self._compare_single_value(comparison_value, other):
                self._comparison_falsy = True
                return False
        self._comparison_falsy = False
        return True

    def __ne__(self, other):
        return not other == self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        args = ', '.join([str(value) for value in self._comparison_values])
        prefix = '!' if self._comparison_falsy else ''
        if self._convert:
            return '{prefix}Like({args}, convert={conversion})'.format(
                prefix=prefix, args=args, conversion=str(self._convert)
            )
        else:
            return '{prefix}Like({args})'.format(prefix=prefix, args=args)

    def _compare_single_value(self, comparison_value, other) -> bool:
        if self._convert is not None:
            other = self._convert(other)
        if isinstance(comparison_value, type):
            return isinstance(other, comparison_value)
        elif callable(comparison_value):
            return comparison_value(other)
        elif is_regex_pattern(comparison_value):
            if isinstance(other, (str, bytes)):
                stringified_value = other
            else:
                stringified_value = str(other)
            try:
                match = comparison_value.match(stringified_value)
            except TypeError:
                # This happens for b"ab" != Like(re.compile('ab')):
                # TypeError: cannot use a string pattern on a bytes-like object
                return False
            if match is None:
                return False
            return match.start() == 0 and match.end() == len(stringified_value)
        return type(other) == type(comparison_value) and other == comparison_value
