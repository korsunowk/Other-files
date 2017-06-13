def popItem(tmp, integer=True):
    """
    Function for pop first needed item in sorted array
    :param tmp: sorted array
    :param integer: True if need first number, False if need first str
    :return: item in sorted array
    """
    for i, x in enumerate(tmp):
        if isinstance(x, int) is integer:
            return tmp.pop(i)


def separateArray(arr):
    """
    Function for separate one array to two array which contains 
    only numbers and only strings values
    :param arr: array with string and numbers
    :return: two arrays
    """
    numbers, strings = [], []
    for x in arr:
        if x.isdigit():
            numbers.append(int(x))
            continue
        strings.append(x)

    numbers.sort()
    strings.sort()

    return numbers, strings


def sortArray(string):
    """
    Function for sorting entered string
    :param string: string with values
    :return: sorted string
    """
    arr = string.split()
    tmp_int, tmp_str = separateArray(arr)
    out = []

    for i in arr:
        if i.isdigit():
            out.append(str(popItem(tmp_int)))
            continue
        out.append(popItem(tmp_str, integer=False))

    return " ".join(out)


if __name__ == '__main__':
    s = raw_input()
    print sortArray(s)
