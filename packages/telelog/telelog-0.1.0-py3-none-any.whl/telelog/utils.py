import os
import sys
import time
import logging
from threading import Thread
from logging.handlers import TimedRotatingFileHandler

ALLOW_LOG_LEVEL = ['FATAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']


def get_logger(logger=None, name='tele', level='info', log_path=None, backup_count=7, terminal=True,
               dynamic_level=False, dynamic_interval=30):
    # 默认仅提供级别：FATAL, ERROR, WARNING, INFO, DEBUG
    logging.addLevelName(logging.DEBUG, 'DEBUG')
    logging.addLevelName(logging.INFO, 'INFO ')
    logging.addLevelName(logging.WARNING, 'WARN ')
    logging.addLevelName(logging.ERROR, 'ERROR')
    logging.addLevelName(logging.FATAL, 'FATAL')

    if logger:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
        logger.propagate = True
    else:
        logger = logging.getLogger(name)

    logging.Formatter.default_msec_format = '%s.%03d'
    logging.Formatter.default_time_format = '%Y%m%dT%I:%M:%S'
    log_formatter = logging.Formatter('%(levelname)s %(asctime)s %(filename)s:%(lineno)s %(threadName)s - %(message)s')
    if log_path is not None:
        handler = TimedRotatingFileHandler(log_path, when='midnight', interval=1, backupCount=backup_count)
        handler.suffix = '%Y-%m-%d'
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)

    if terminal:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)
    log_level = level.upper().strip()
    if log_level not in ALLOW_LOG_LEVEL:
        logger.warning(f'LOG_LEVEL {log_level} is not allowed, set to default INFO')
        log_level = "INFO"
    logger.setLevel(log_level)
    if dynamic_level:
        dynamic_level_thread = Thread(target=dynamic_change_log_level, args=(logger, log_level, dynamic_interval))
        dynamic_level_thread.setDaemon(True)
        dynamic_level_thread.start()

    return logger


def dynamic_change_log_level(logger, log_level, dynamic_interval):
    logger = logger
    current_log_level = log_level
    dynamic_interval = dynamic_interval
    while True:
        log_level = os.environ.get('LOG_LEVEL', None)
        if log_level is not None:
            log_level = log_level.upper().strip()
            if log_level in ALLOW_LOG_LEVEL and log_level != current_log_level:
                logger.setLevel(log_level)
                if log_level == 'ERROR':
                    logger.error(f'Change LOG_LEVEL from {current_log_level} to {log_level}')
                if log_level == 'WARNING':
                    logger.warning(f'Change LOG_LEVEL from {current_log_level} to {log_level}')
                else:
                    logger.info(f'Change LOG_LEVEL from {current_log_level} to {log_level}')
        time.sleep(dynamic_interval)
