import logging
import logging.handlers
import sys
import os

# formatter
CLIENT_FORMATTER = logging.Formatter('%(asctime) - 25s %(levelname) - 10s %(filename) - 21s %(message)s')

# log_filename

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(PATH, 'client_logs\client.log')


STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='midnight')
LOG_FILE.setFormatter(CLIENT_FORMATTER)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(logging.DEBUG)

if __name__ == '__main__':
    print(PATH)
    print(PATH2)
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
