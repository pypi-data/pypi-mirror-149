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

def able_to_keep_errors(f):
    decorator = keep_errors
    @functools.wraps(f)
    def decored(*args, keep_errors=False, **kwargs):
        if keep_errors:
            return decorators(f)(*args, **kwargs)
        return f(*args, **kwargs)

