class bun_error(Exception):

def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Error occur in food system: %s"%(', '.join(errors.keys()))
        super().__init__(msg)
        self.errors = errors

def check_numBuns_error(numBuns):
    errors = {}

    if (numBuns > 4):
        errors['numBuns'] = 'Please input no more than 4 buns.'