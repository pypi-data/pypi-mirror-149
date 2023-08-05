from customLogger import customLogger


class basicComponent():

    __slots__ = ('config', 'log', 'runsafe')

    def __init__(self, **params):

        # Get config object, raise error if failed to
        self.config = params.get('config')
        if self.config is None:
            raise Exception('Failed to pass config to object')

        # Create a log object
        self.log = params.get('log')
        if self.log is None:
            # Check if log is in the config
            if 'log' in self.config:
                # Save value from config
                self.log = self.config.get('log')
            else: # Otherwise create a custom logger object
                self.log = customLogger()

        # Print debug this object has been created
        self.log.debug(f'Initializing {self.__class__.__name__} object')

        # Set runsafe (will perform other checks, default True)
        self.runsafe = params.get('runsafe', True)

    def __del__(self):
        self.config, self.log, self.runsafe = None, None, None

    def _is_hashable(self):
        try:
            self.__hash__()
            return True
        except:
            return False

    def _is_iterable(self):
        try:
            self.__iter__()
            return True
        except:
            return False
