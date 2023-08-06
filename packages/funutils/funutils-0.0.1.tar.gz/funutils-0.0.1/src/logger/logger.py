from colorama import Fore
import time
from colorfy import colorfy

class Palette:
    def __init__(self, trace = Fore.GREEN, debug = Fore.BLUE, info = Fore.RESET, warn = Fore.YELLOW, err = Fore.RED, assertion_fail = Fore.MAGENTA):
        self.trace = trace
        self.debug = debug
        self.info = info
        self.warn = warn
        self.err = err
        self.assertion = assertion_fail

class Logger:
    def __init__(self, palette:Palette = Palette()):
        self.palette = palette

    def trace(self, msg):
        def addzero(x):
            if x < 10:
                return '0' + str(x)
            else:
                return str(x)
        tm = time.localtime()
        tmstr = f'{tm.tm_year}-{addzero(tm.tm_mon)}-{addzero(tm.tm_mday)} {addzero(tm.tm_hour)}:{addzero(tm.tm_min)}:{addzero(tm.tm_sec)}'
        msg = colorfy(self.palette.trace, tmstr + ' [TRACE] ' + msg)
        print(msg)

    def debug(self, msg):
        def addzero(x):
            if x < 10:
                return '0' + str(x)
            else:
                return str(x)
        tm = time.localtime()
        tmstr = f'{tm.tm_year}-{addzero(tm.tm_mon)}-{addzero(tm.tm_mday)} {addzero(tm.tm_hour)}:{addzero(tm.tm_min)}:{addzero(tm.tm_sec)}'
        msg = colorfy(self.palette.debug, tmstr + ' [DEBUG] ' + msg)
        print(msg)

    def info(self, msg):
        def addzero(x):
            if x < 10:
                return '0' + str(x)
            else:
                return str(x)
        tm = time.localtime()
        tmstr = f'{tm.tm_year}-{addzero(tm.tm_mon)}-{addzero(tm.tm_mday)} {addzero(tm.tm_hour)}:{addzero(tm.tm_min)}:{addzero(tm.tm_sec)}'
        msg = colorfy(self.palette.info, tmstr + ' [INFOO] ' + msg)
        print(msg)

    def warn(self, msg):
        def addzero(x):
            if x < 10:
                return '0' + str(x)
            else:
                return str(x)
        tm = time.localtime()
        tmstr = f'{tm.tm_year}-{addzero(tm.tm_mon)}-{addzero(tm.tm_mday)} {addzero(tm.tm_hour)}:{addzero(tm.tm_min)}:{addzero(tm.tm_sec)}'
        msg = colorfy(self.palette.warn, tmstr + ' [WARNI] ' + msg)
        print(msg)

    def error(self, msg):
        def addzero(x):
            if x < 10:
                return '0' + str(x)
            else:
                return str(x)
        tm = time.localtime()
        tmstr = f'{tm.tm_year}-{addzero(tm.tm_mon)}-{addzero(tm.tm_mday)} {addzero(tm.tm_hour)}:{addzero(tm.tm_min)}:{addzero(tm.tm_sec)}'
        msg = colorfy(self.palette.err, tmstr + ' [ERROR] ' + msg)
        print(msg)

    def fail_assert(self, msg):
        def addzero(x):
            if x < 10:
                return '0' + str(x)
            else:
                return str(x)
        tm = time.localtime()
        tmstr = f'{tm.tm_year}-{addzero(tm.tm_mon)}-{addzero(tm.tm_mday)} {addzero(tm.tm_hour)}:{addzero(tm.tm_min)}:{addzero(tm.tm_sec)}'
        msg = colorfy(self.palette.assertion, tmstr + ' [ASSRT] ' + msg)
        print(msg)

if __name__ == '__main__':
    logger = Logger()
    logger.trace('trace')
    logger.debug('debug')
    logger.info('info')
    logger.warn('warn')
    logger.error('err')
    logger.fail_assert('assert')