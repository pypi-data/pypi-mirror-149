
class CollateralError(Exception):
    __slots__ = ()

def collateralErrorFactory(*args, on_exception=Exception):
    """Collateral exception factory

    The built exception extend both the CollateralError class
    and an exception type given as parameter.

    Parameters
    ----------
    args: tuple
        argument of the exception to build.

    on_exception: Exception or type, default=Exception
        either an exception or an exception type, that should be
        extended by the type of the exception to build.  If an
        exception instance, then its args attribute tuple value
        is prepended to the given args.  If a type, it should be
        compatible with the CollateralError class, as both will
        be extended by the type of the exception to build.

    Returns
    -------
    An Exception instance whose type extends both the
    CollateralError class and the provided on_exception type,
    and whose args attribute contains the given args tuple
    parameter, possibly preceded by the values taken from the
    corresponding attribute of on_exception if an Exception
    instance.

    """
    if isinstance(on_exception, Exception):
        args = (*on_exception.args, *args)
        on_exception = type(on_exception)
    cls = type(f"Collateral{on_exception.__name__}", (CollateralError, on_exception), dict(__slots__=()))
    self = cls(*args)
    return self

