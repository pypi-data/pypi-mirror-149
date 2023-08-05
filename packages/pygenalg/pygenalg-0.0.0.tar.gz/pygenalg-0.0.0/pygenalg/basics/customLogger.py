
class customLogger():

    def debug(self, s):
        print(f'   Debug: {s}')

    def info(self, s):
        print(f'    Info: {s}')

    def warning(self, s):
        print(f' WARNING: {s}')
    warn = warning

    def error(self, s):
        print(f'   ERROR: {s}')

    def critical(self, s):
        print(f'CRITICAL: {s}')
