def inverse_range(length, stop=-1):
    """helper function to iterate in an inverse order
    """
    return range(length - 1, stop, -1)


def is_in(elem, array):
    """given an `elem` and an ordered array, it returns True and its index if the element is in there,
    False, None otherwise
    """
    low = 0
    high = len(array)
    while low < high:
        mid = (low + high) // 2
        if array[mid] < elem:
            low = mid + 1
        else:
            high = mid

    if low < len(array) and low >= 0 and array[low] == elem:
        return True, low
    return False, None


def lower_bound(elem, array):
    """returns the index in which you should insert the element `elem` to keep the order
    """
    low = 0
    high = len(array)
    while low < high:
        mid = (low + high) // 2
        if array[mid] < elem:
            low = mid + 1
        else:
            high = mid

    return low


def insert_ordered(elem, array):
    """inserts `elem` in `array` in an index that keeps the order
    """
    array.insert(lower_bound(elem, array), elem)


subscripts = '₀₁₂₃₄₅₆₇₈₉'  # outside the function so that it mallocs only once (?)
def to_subscript(number):
    if number < 0:
        return ValueError(f"{number} should be positive or zero")

    res = [x for x in str(number)]
    i = len(res) - 1
    while i >= 0:
        res[i] = subscripts[int(res[i])]
        i -= 1
    return ''.join(res)


integer_numbers = {
    '₀': '0',
    '₁': '1',
    '₂': '2',
    '₃': '3',
    '₄': '4',
    '₅': '5',
    '₆': '6',
    '₇': '7',
    '₈': '8',
    '₉': '9',

}  # outside the function so that it mallocs only once (?)
def from_subscript(number):
    res = [x for x in number]
    i = len(res) - 1
    while i >= 0:
        res[i] = integer_numbers[res[i]]
        i -= 1
    return int(''.join(res))
