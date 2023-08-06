class Hook():
    name = None
    args = {}

    def __init__(self, arglist=None):
        self.arglist = arglist

        if arglist:
            for arg in arglist:
                if '=' in arg:
                    n, v = arg.split('=', 1)
                    self.args[n] = v

    def sleep(self, seconds):
        pass