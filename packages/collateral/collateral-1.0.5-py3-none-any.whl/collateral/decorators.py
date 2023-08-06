import functools

def keep_errors(f):
    """Transform a callable so that exception raising is replaced by exception returning
    """
    @functools.wraps(f)
    def decored(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return e
    return decored

