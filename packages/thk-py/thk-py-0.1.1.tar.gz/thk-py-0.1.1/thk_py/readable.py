# -*- coding: utf-8 -*-


def get_readable_size(size: int, round_number: int = 2) -> str:
    """
    Usage::
        >>> get_readable_size(0)
        '0B'
        >>> get_readable_size(1000)
        '1000B'
        >>> get_readable_size(1024)
        '1.0KB'
        >>> get_readable_size(2000)
        '1.95KB'
        >>> get_readable_size(1024 * 1024)
        '1.0MB'
        >>> get_readable_size(int(1024 * 1024 * 1.94))
        '1.94MB'
        >>> get_readable_size(1024 * 1024 * 1024 * 3)
        '3.0GB'
        >>> get_readable_size(1024 * 1024 * 1024 * 1024 * 4)
        '4.0TB'
        >>> get_readable_size(1024 * 1024 * 1024 * 1024 * 1024 * 5)
        '5.0PB'
        >>> get_readable_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 10)
        '10240.0PB'
    """
    unit_list = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    index = 0

    while size >= 1024 and index < len(unit_list) - 1:
        size /= 1024
        index += 1

    return f'{round(size, round_number)}{unit_list[index]}'
