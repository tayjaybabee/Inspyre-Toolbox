"""
Contains error classes for the inspyre_toolbox.string_kit module.
"""
from inspyre_toolbox.core_helpers.logging import add_isl_child


LOG_NAME = 'inspyre_toolbox.core.errors.string_kit'
LOG = add_isl_child(LOG_NAME)

LOG.debug('Logger started, {LOG_NAME} imported.')


class ParameterStateError(Exception):
    """
    The :class:`ParameterStateError` class is used to raise an error if the
    parameter state of the raising function is not valid.

    Raised when the parameters of a function have been assigned an invalid,
    illogical or; insane state.
    """

    message = 'The parameter state of the function is not valid.'

    def __init__(self, message=None, skip_print=False, *args, **kwargs):
        """
        The :class:`ParameterStateError` class is used to raise an error if the
        parameter state of the raising function is not valid.

        Raised when the parameters of a function have been assigned an invalid,
        illogical or; insane state.

        Arguments:
            message (:class:`str`):
                Provide a custom message for the exception. (Optional, defaults to
                ``None``)

            skip_print (:class:`bool`)
                Prevent the printing of an error message when the exception is
                raised in a try/except block. (Optional, defaults to ``False``).
        """
        # Set up the logger.
        log = add_isl_child(LOG_NAME.__class__.__name__)

        log.debug('Logger started, {LOG_NAME} imported.')

        # If the message parameter is not a string raise an error that we'll recover
        # from immediately.
        if not isinstance(message, str):
            try:
                raise TypeError('The message must be a string.')
            except TypeError as e:
                log.error(e)

        # if the message parameter has a value, fill the message attribute with it.
        if message:
            self.message += f"Addditional information from the caller: {message}"

        # If the user wants to skip printing, don't print the message.
        if not skip_print:
            print(self.message)

        else:
            # If we're skipping printing, log the message.
            log.debug(self.message)
            log.debug('Printing of the error message was skipped.')


class MinimalLengthViolationError(ParameterStateError):
    def __init__(self,  target_str_len, min_len, *args, **kwargs):
        """
        The :class:`MinimalLengthViolationError` class is used to raise an error if the
        length of the string is less than the minimum length.

        Raised when the length of the string is less than the minimum length.

        Arguments:
            target_str_len (:class:`int`):
                The length of the string.

             min_len (:class:`int`):
                The minimum length of the string.

            *args:
                The positional arguments to be passed to the
                :class:`ParameterStateError` class.

            **kwargs:
                The keyword arguments to be passed to the
                :class:`ParameterStateError` class.

        Returns:
            None

        Attributes:
            message (:class:`str`):
                A custom message for the exception, or the default message if no
                value is provided for :param:`message`.
        """
        # Set up the logger.
        log = add_isl_child(LOG_NAME.__class__.__name__)

        log.debug('Logger started, {LOG_NAME} imported.')

        self.minimum_length = min_len
        self.target_string_length = target_str_len

        # Set the message.
        self.message = f'The length of the string ({target_str_len}) is less than ' \
                       f'the minimum configured length ({min_len}).'

        # Call the superclass' __init__ function.
        super().__init__(self.message, *args, **kwargs)
