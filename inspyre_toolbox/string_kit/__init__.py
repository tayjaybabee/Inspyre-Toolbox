from inspyre_toolbox.core_helpers.logging import add_isl_child
from inspyre_toolbox.core.errors.string_kit import MinimalLengthViolationError

LOGGER_NAME = 'inspyre_toolbox.string_kit'

LOG = add_isl_child(LOGGER_NAME)

LOG.debug(f'Logger started, {LOGGER_NAME} imported.')

global_minimum_default_length = 5


def append_suffix(target_string, suffix, include_suffix_in_count=False):
    """
    Append a suffix to a string.

    This function appends a suffix to a string.

    Note:
        This function is intended to be used by the :func:`truncate_str` function
        which will truncate the string to the length expected by the user (leave the
        suffix calculations for :func:`append_suffix`) before calling this function.

    Args:
        target_string (:obj:`str`):
            The string to be modified. (Required)

        suffix (:obj:`str`):
            The suffix to be inserted. (Required)

        include_suffix_in_count (:obj:`bool`, optional):
            Whether to include the suffix in the count. (Default: False)


    Returns:
        :obj:`str`: The modified string.
    """
    if include_suffix_in_count:
        return target_string[:len(target_string) - len(suffix)] + suffix
    else:
        return target_string + suffix

def check_min(
        string,
        minimum_length=global_minimum_default_length,
        override_min=False
):
    """
    Check if a string is at least a certain length.

    Args:
        string (:obj:`str`):
            The string to be checked. (Required)

        minimum_length (:obj:`int`, optional):
            The minimum length of the string. (Default: 5)

        override_min (:obj:`bool`, optional):
            Whether to override the minimum length. (Default: False)

    Returns:
        True if the string is at least the minimum length, False otherwise.
    """
    str_len = len(string)
    if str_len < minimum_length and not override_min:
        raise MinimalLengthViolationError(f'String must be at least {minimum_length} characters long.')
    return len(string) >= minimum_length


# @since 1.3.1.dev3
def truncate_str(
        target_str: str,
        max_len: int,
        suffix: str = '...',
        count_suffix: bool = False,
        override_min: bool = False,
        no_trailing_space: bool = True,
        suppress_warnings: bool = True,
        strict: bool = False) -> str:
    """
    Truncate a string to a maximum length.

    The function takes a string (:param:`target_str`) and a maximum length
    (:param:`max_len`) as required positional arguments. If :param:`target_str`
    has a length greater than :param:`max_len`, :param:`target_str` is truncated
    and the :param:`suffix` is appended otherwise; the passed
    :param:`target_str` is returned unmodified.

    Arguments:
        target_str (:obj:`str`):
            The string to truncate.

        max_len (:obj:`int`):
            The maximum length of the string.

        suffix (:obj:`str`, optional):
            The suffix to append to the truncated string (I.E; '...').
            Defaults to '...'.

        count_suffix (:obj:`bool`, optional):
            Whether to count the length of the suffix in the truncation. Defaults to
            False.

        override_min (:obj:`bool`, optional):
            Whether to override the minimum length of the string. Defaults to False.

        no_trailing_space (:obj:`bool`, optional):
            Whether to remove trailing spaces. Defaults to False.

        suppress_warnings (:obj:`bool`, optional):
            Whether to suppress warnings. Defaults to False.

        strict (:obj:`bool`, optional):
            Whether to raise an error if the string is too short. Defaults to False.

    Example:
        >>> truncate_str('This is a string', 10)
        'This is...'

    Returns:
        str:
            The truncated string.

    Raises:
        ValueError:
            If the string is less than the minimum length and :param:`override_min`
            is False.
    """
    global global_minimum_default_length
    suffix_len = len(suffix)
    initial_len = len(target_str)
    min_len = global_minimum_default_length + suffix_len if count_suffix else global_minimum_default_length

    if count_suffix:
        min_len = suffix_len + global_minimum_default_length
    else:
        min_len = global_minimum_default_length

    # Set up logger
    # Set its name.
    log_name = f'{LOGGER_NAME}.truncate_str'

    # Add a child-logger to the ISL log device.
    log = add_isl_child(log_name)

    # Output some debug information
    log.debug(f'Truncating string: {target_str}')
    log.debug(f'Maximum length: {max_len} characters | Minimum Length: '
              f'{min_len} characters {"(overridden)" if override_min else ""})')
    log.debug(f'Suffix: {suffix} | Suffix Length: {suffix_len}')
    log.debug(f'Count suffix: {count_suffix}')
    log.debug(f'Override minimum length: {override_min}')

    # Check if minimum string length has been overridden. If so, and warnings
    # have not been suppressed using the 'suppress_warnings' argument, we
    # warn the user of this.
    if override_min:
        if not suppress_warnings:
            log.warning('Detected override_min parameter evaluating to True. This '
                        'may cause unexpected results, and is not recommended. Use '
                        'with caution.')

        # If the length of the target string is greater than the minimum length
        # anyway, we should inform the user of this with a warning log entry.
    try:
        check_min(target_str)
    except MinimalLengthViolationError as e:
        if not suppress_warnings:
            log.warning('Detected violation of minimum sting length for "target_str".')
            log.warning(f'Minimum length: {e.minimum_length} characters')

        if strict:
            raise e from e
        else:
            if not override_min:
                raise e from e



    # If the length of the target string is greater than the maximum length,
    # we truncate it.
    if len(target_str) > max_len:
        log.debug('String is longer than maximum length.')

        min_len = max_len if override_min else max_len - suffix_len
        res = target_str[:min_len]

        if count_suffix:
            res = res[:-suffix_len]
            log.debug(f'Removing {suffix_len} more characters from the end of the '
                      'string to make room for the suffix.')

        if no_trailing_space and res.endswith(' '):
            log.debug('Removing trailing space.')
            res = res.rstrip()
        res += suffix

        try:
            if res == suffix:
                raise ValueError('The string is too short to truncate, given the '
                                 'parameter state.\n The "suffix" argument is set to '
                                 f'"{suffix}", which has a length of {suffix_len} while the max '
                                 f'allowed length of the returned string is {max_len} and '
                                 f'"count_suffix" is set to {count_suffix}.')
        except ValueError as e:
            log.error(e)
            return target_str
        return res
    else:
        log.debug('String is shorter than maximum length. No changes made.')
        return target_str
