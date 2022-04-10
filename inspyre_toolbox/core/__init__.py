#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
from appdirs import AppDirs
from pathlib import Path


__AUTHOR__ = 'Inspyre-Softworks'
__APP__ = 'Inspyre-Toolbox'

__APP_DIRS__ = AppDirs(appname=__APP__, appauthor=__AUTHOR__)

__CONFIG_DIR__ = Path(__APP_DIRS__.user_config_dir)
__CACHE_DIR__  = Path(__APP_DIRS__.user_cache_dir)
