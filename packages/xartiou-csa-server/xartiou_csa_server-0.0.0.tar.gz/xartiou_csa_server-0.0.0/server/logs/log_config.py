import inspect
import logging
import os.path
import sys
import traceback

if sys.argv[0].find('client.py') == -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')

formatter = logging.Formatter("%(asctime)s - %(levelname)-8s - %(module)-8s - %(message)s ")

level_handler = logging.DEBUG
Level_logging = logging.DEBUG


def create_dir():
    storage_name = '../log/log_storage'
    if not os.path.exists(storage_name):
        os.mkdir(storage_name)
    return storage_name


def log(func):
    # @wraps(func)
    def log_saver(*args, **kwargs):
        ret = func(*args, **kwargs)
        logger.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func.__module__}.'
                     f'Вызов из функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}')

        return ret

    return log_saver
