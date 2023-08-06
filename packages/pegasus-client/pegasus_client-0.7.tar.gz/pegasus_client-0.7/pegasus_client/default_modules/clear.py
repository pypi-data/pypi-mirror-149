class module:
    'Clear the terminal screen.'

    def __init__(self):

        pass

    def __run__(self, params=None):

        print('\x1b[2J')
        return('')
