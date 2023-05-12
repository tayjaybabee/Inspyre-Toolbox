from typing import Any, List, NewType

ChunkifiedList = NewType('ChunkifiedList', list)


def __split_evenly(target):
    """

    Split a target list down the center.

    Arguments:
        target (list):
            The list you'd like to split.

    Returns:
        (list, list):
            Two lists that should be perfectly (or as perfectly as possible
            while keeping whole numbers) split in two while maintaining
            its order.

    """
    length = len(target)
    mi = length // 2

    list1 = target[:mi]
    list2 = target[mi:]

    return list1, list2


def __split_alt(target):
    """

    Split a given list into two columns in an alternating format.


    ========= ===========
      Col 1      Col 2
    ========= ===========
        1          2
    --------- -----------
        3          4
    ========= ===========

    Args:
        target:

    Returns:

    """
    list1 = []
    list2 = []

    for item in target:
        if target.index(item) % 2 == 0:
            list1.append(item)
        else:
            list2.append(item)

    return list1, list2


def split_list(target, split_method='middle'):
    """
    This function takes a list and breaks it into two lists.

    :func:`split_list` returns an object that contains a list of
    two lists. The list of two lists are called 'splits' and represent the
    original list broken into two lists.

    Note:
        The values that will be accepted for the 'split_method'
        parameter are as follows;

           * alternating_columns:

                  Sort into a number of columns where ordering goes from
                  left-to-right.

            * middle:

                  Split a list in half results in two smaller lists containing
                  elements from the original in the same order. (The Default
                  parameter value)

    """
    valid_split_methods = [
            'alternating_columns',
            'middle',
    ]

    if split_method.lower() not in valid_split_methods:
        raise ValueError(f"The value for 'split_method' must be one of; {', '.join(valid_split_methods)}")
    if split_method.lower() == 'middle':
        return __split_evenly(target)
    elif split_method.lower() == 'alternating_columns':
        return __split_alt(target)


def chunkify(target: list, num_per: int) -> ChunkifiedList:
    """
    This function takes a list and breaks it into smaller lists of a
    specified size.

    :func:`chunkify` returns an object that contains a list of
    smaller lists. The list of smaller lists are called 'chunks' and represent the
    original list broken into smaller lists of a specified size.

    Note:
        The last chunk may contain fewer than the specified number of elements.

    Args:
        target (:obj:`list`, required):
            Specify the list that will be chunked

        num_per (:obj:`int`, required):
            Specify how many elements should be in each sublist

    Returns:
        :obj:`ChunkifiedList`:
            A list of lists, where each inner list is ``num_per`` long.

    """
    ret_lst = lambda target, num_per: [target[i:i + num_per] for i in range(0, len(target), num_per)]

    return ChunkifiedList(ret_lst(target, num_per))
