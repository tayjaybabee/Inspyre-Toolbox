"""

Configuration classes and functions for the live_timer package.

"""
from configparser import ConfigParser
from os import makedirs
from pathlib import Path
from inspyre_toolbox.core import __CACHE_DIR__ as DEFAULT_CACHE_DIR, __CONFIG_DIR__ as DEFAULT_CONFIG_DIR


def purge():
    import shutil

    shutil.rmtree(DEFAULT_CONFIG_DIR)


class Cache(ConfigParser):
    """
    The cache object.

    Contains very little information, such as where to find the configuration file if it's not in its default
    cache_filepath.
    """

    def save(self):
        """
        Save the current state of the cache.

        Returns:
            (Saved Path | None):
                * If the file-write was successful 'save' will return with the path at which the 'cache.ini' file was
                written.

                * If the file-write was unsuccessful 'save' will return bool(False).
        """
        with open(self.filepath, 'w') as fp:
            self.write(fp)

        return self.filepath if self.filepath.exists() else False

    def create(self):
        """
        Create a cache-file.
        
        Create a cache-file
          
        Returns:

        """
        default_fp = str(Path(DEFAULT_CONFIG_DIR).joinpath('config.ini'))
        cache = {
            'DEFAULT': {
                'config-filepath': default_fp,
                'config-filepath-divergent': False,
            }
        }

        if not self.dirpath.exists():
            makedirs(self.dirpath)

        self.read_dict(cache)

        self.add_section('USER')

        if str(self.config_filepath) != self.get('USER', 'config-filepath'):
            self.set('USER', 'config-filepath-divergent', 'true')
            self.set('USER', 'config-filepath', str(self.config_filepath))

        self.new = True

        self.save()

    def load(self):
        """

        Load a cache.ini file from disk.

        Returns:
            None

        """
        self.read(self.filepath)

    def __init__(
            self,
            cache_filepath=DEFAULT_CACHE_DIR.joinpath('cache.ini'),
            config_filepath=DEFAULT_CONFIG_DIR.joinpath('config.ini')
    ):
        """

        Create a Cache object.

        Arguments:

            cache_filepath ((Path | str), Optional):
                The filepath of the cache.ini file. If the file doesn't already exist, we'll go ahead and make one. If
                the file does exist, we'll load its values.

        """
        if not isinstance(cache_filepath, Path):
            if not isinstance(cache_filepath, str):
                raise ValueError(f"'cache_filepath' must be of type String, or pathlib.Path not {type(cache_filepath)}")
            else:
                cache_filepath = Path(cache_filepath).expanduser()

        self.filepath = cache_filepath
        self.dirpath = self.filepath.parent
        self.config_filepath = Path(config_filepath).expanduser()
        self.config_dirpath = self.config_filepath.parent
        self.new = False
        super(Cache, self).__init__(self)

        if not cache_filepath.exists():
            self.create()
            self.clear()

        self.load()

        if self.new:
            if self.config_filepath != self.get('USER', 'config-filepath'):
                self.set('USER', 'config-filepath', str(self.config_filepath))
                self.set('USER', 'config-filepath-divergent', 'true')


class DefaultConfig(ConfigParser):
    def __init__(self):
        self.default = {
            'DEFAULT': {
                'treat-pause-as-toggle':    'false',
                'get-elapsed-returns-secs': 'false',
                'disable-timer-history':    'false',
            }
        }


CACHE = Cache()


class Config(ConfigParser):
    def __init__(self,
                 config_filepath=None,
                 ):
        cached_fp = Path(CACHE.get('USER', 'config-filepath'))

        if config_filepath is not None:
            config_filepath = Path(config_filepath).expanduser()
        else:
            CACHE.set('USER', 'config-filepath', config_filepath)

        self.filepath = config_filepath

        self.load()
