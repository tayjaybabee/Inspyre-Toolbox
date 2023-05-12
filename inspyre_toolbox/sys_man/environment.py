"""
File:
    PROJECT_ROOT/inspyre_toolbox/sys_man/environment.py

Author:
    Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>

Date:
    08/09/2022 - 19:15 hrs

Description:
    Holds the 'EnvironmentVariablesClass' which enables one to more easily use
    environment variables for python projects.

License:
    MIT
"""

from os import environ
from box import Box
import sys


class EnvironmentVariables(object):
    def __init__(self):
        self.__vars = environ.keys()
        self.__true_vals = ['yes', 'y', 'true', 't', 1]
        self.__false_vals = ['no', 'n', 'false', 'f', 0]

    @property
    def box(self):
        return Box(self.var_dict)

    @property
    def vars(self):
        return list(environ.keys())

    @property
    def var_dict(self):
        return dict(environ.items())

    @property
    def environ(self):
        return environ

    def __get(self, *args, **kwargs):
        ignore_boolean = kwargs['ignore_boolean']
        key = args[0]

        if not self.has_var(key):
            raise KeyError(key)
        entry = self.environ[key]
        if not ignore_boolean:
            for true_val in self.__true_vals:
                if entry.lower() == true_val:
                    return True
            for false_val in self.__false_vals:
                if entry.lower() == false_val:
                    return False

        return entry

    def get(self, key: str, ignore_boolean=False):
        """
        Get the value of a given environment variable.

        Get the value of a given environment variable. If the value is a boolean,
        the value will be returned as a boolean. If the value is not a boolean,
        the value will be returned as a string. You can pass the keyword argument
        :param:`ignore_boolean`  a  :obj:`bool` value of True  to ignore boolean
        values and return the value as a :obj:`string`.

        Arguments:
            key (str, required):
                The environment variable to get the value of.

            ignore_boolean(bool, optional):
                A :obj:`bool` value of True to ignore boolean values and return the
                value as a :obj:`string`.

        Returns:

            str:
                The value of the environment variable.

            bool:
                The value of the environment variable as a boolean.

            None:
                If the environment variable does not exist.

        Raises:
            KeyError:
                If the environment variable does not exist.

        """
        try:
            return self.__get(key, ignore_boolean=ignore_boolean)
        except KeyError as e:
            print(f'An error occurred: {sys.exc_info()[0]}: {e}')
            return None

    @property
    def count(self):
        return len(self.vars)

    def has_var(self, var):
        var = var.upper()
        return var in self.var_dict.keys()
