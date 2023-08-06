from datetime import datetime
import time
import logging
import logging.handlers


class RotatingFileHandlerWithHeader(logging.handlers.RotatingFileHandler):
    '''
    Derived class that adds a header every rotating log
    '''
    def __init__(self, header, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFormatter(logging.Formatter('%(message)s'))
        self.header = logging.makeLogRecord({'msg': header})
        self.emit(self.header)

    def doRollover(self):
        super().doRollover()
        original_formatter = self.formatter
        self.setFormatter(logging.Formatter('%(message)s'))
        super().emit(self.header)
        self.setFormatter(original_formatter)


class FormatterMsec(logging.Formatter):

    def formatTime(self, record, _):
        ct = self.converter(record.created)
        t = time.strftime('%Y-%m-%d;%H:%M:%S', ct)
        s = '%s,%03d' % (t, record.msecs)
        return s[:-2]


def set_to_rotate(logger: logging.Logger, file_name_prefix: str,
                  header_field: str = None, level=logging.DEBUG,
                  max_bytes=5000000, backup_count=5) -> None:
    '''
    Set logger to rotate

    Args:
    - logger: logging.Logger instance
    - file_name_prefix: log filename prefix. A timestamp will be appended to the prefix
    - header_field: domain specific field name [Default: message]
    - level: logging.Level
    - max_bytes: Log size limit
    - backup_count: how many old logs must be saved before being overwritten
    '''
    current_time = datetime.now().strftime('%Y%m%d-%H%M%S.%f')
    log_name = f'{file_name_prefix}_{current_time}.log'

    header = f'date;time;level;{header_field}' if header_field else f'date;time;level;message'

    handler = RotatingFileHandlerWithHeader(header=header, filename=log_name,
                                            maxBytes=max_bytes, backupCount=backup_count)

    formatter = FormatterMsec(fmt='%(asctime)s;%(levelname)s;%(message)s',
                              datefmt='%Y%m%d;%H%M%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
