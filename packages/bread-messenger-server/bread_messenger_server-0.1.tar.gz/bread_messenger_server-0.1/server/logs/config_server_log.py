import os
import sys
import logging
import logging.handlers
from common.variables import LOGGING_LEVEL, ENCODING

sys.path.append('../')

# создание формирователя логов (formatter)
SERVER_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# создание потоков вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(LOGGING_LEVEL)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding=ENCODING, interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# создание и настройка регистратора
LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
