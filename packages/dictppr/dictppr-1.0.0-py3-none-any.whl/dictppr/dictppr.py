def check_nesting(items: list) -> int:
    """
    Checks how many nests are left.

    Parameters
    ----------
    items
        List of items to be checked.

    Returns
    ----------
    The number of nests remaining.
    """
    nests = 0
    for item in items:
        if isinstance(item, dict):
            nests += 1
        if isinstance(item, list):
            nests += check_nesting(item)
    return nests


def check_item(item: any) -> any:
    """
    Checks whether the given item
    is as flattened as possible.

    Parameters
    ----------
    item
        Item to be checked.

    Returns
    ----------
    Ensured item.
    """
    if isinstance(item, dict):
        keys = list(item.keys())
        item = flattener(item)
        item = check_item(item)
        if isinstance(item, list) and len(keys) > 1:
            if not check_nesting(item):
                item = map(lambda k, i: f"{k}:{i}", keys, item)
                item = map(lambda i: i.replace("'", ""), item)
                item = list(item)
    elif isinstance(item, list):
        if check_nesting(item):
            item = flattener(item)
    return item


def flattener(item: any) -> any:
    """
    Flattens the given item.

    Parameters
    ----------
    item
        The item to be flattened.

    Returns
    ----------
    A flattened item.
    """
    length = len(item)
    if length == 0:
        flattened = ""
    elif length == 1:
        if isinstance(item, list):
            flattened = item[0]
        elif isinstance(item, dict):
            flattened = list(item.values())[0]
    elif length > 1:
        if isinstance(item, list):
            flattened = [check_item(elem) for elem in item]
        elif isinstance(item, dict):
            flattened = list(item.values())
    return flattened


def string(item: any) -> str:
    """
    Converts the given item to a string.

    Parameters
    ----------
    item
        The item to be converted.

    Returns
    ----------
    A converted item.
    """
    if isinstance(item, list):
        item = ", ".join(map(lambda i: str(i), item))
    else:
        item = str(item)
    return item


def convert(dictionary: dict):
    """
    Flattens nested dictionaries.

    Parameters
    ----------
    dictionary
        A nested dictionary.

    Returns
    ----------
    A flattened dictionary.
    """
    dictionary = {key: check_item(val) for key, val in dictionary.items()}
    dictionary = {key: string(val) for key, val in dictionary.items()}
    return dictionary


def pprint(dictionary: dict) -> None:
    """
    Pretty prints flattened dictionary.

    Parameters
    ----------
    dictionary
        A nested dictionary.

    Returns
    ----------
    None
    """
    dictionary = convert(dictionary)
    if not dictionary:
        print("")
        return None
    max_key_len = max(map(len, dictionary.keys()))
    for key, value in dictionary.items():
        key_len, val_len = len(key), len(value)
        if key_len < max_key_len:
            key += " " * (max_key_len - key_len)
            key_len = len(key)
        if val_len > 80:
            space = "\n" + " " * (key_len + 4)
            positions = list(range(50, val_len, 50))
            for pos in sorted(positions, reverse=True):
                value = value[:pos] + space + value[pos:]
        print(f"{key} => {value}")


def get(dictionary: dict) -> str:
    """
    Flatten and convert nested dictionary.

    Parameters
    ----------
    dictionary
        A nested dictionary.

    Returns
    ----------
    Flattened and converted dictionary.
    """
    dictionary = convert(dictionary)
    result = check_item(dictionary)
    result = string(result)
    return result
