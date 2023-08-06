import builtins
from functools import partial, wraps
from collateral.tools import missing
from collateral.collateral import Collateral

_globals = {}

@partial(_globals.__setitem__, 'apply')
def apply(f, collateral, keyword=None, /, pre_args=(), post_args=(), keep_errors=False, **kwargs):
    if keyword:
        pf = lambda e: f(*pre_args, *post_args, **dict(kwargs, **{keyword: e}))
    else:
        pf = lambda e: f(*pre_args, e, *post_args, **kwargs)
    return collateral.collaterals.map(pf, keep_errors=keep_errors)
#Boolean operations
@partial(_globals.__setitem__, 'not_')
def not_(collateral, keep_errors=False):
    f = lambda e: not e
    return collateral.collaterals.map(f, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'or_')
def or_(collateral, other, keep_errors=False):
    f = lambda e: e or other
    return collateral.collaterals.map(f, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'and_')
def and_(collateral, other, keep_errors=False):
    f = lambda e: e and other
    return collateral.collaterals.map(f, keep_errors=keep_errors)


#non-unary functions on iterables
@partial(_globals.__setitem__, 'map')
@wraps(builtins.map)
def map(f, collateral, keep_errors=False):
    pmap = partial(builtins.map, f)
    return collateral.collaterals.map(pmap, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'filter')
@wraps(builtins.filter)
def filter(f, collateral, keep_errors=False):
    pfilter = partial(builtins.filter, f)
    return collateral.collaterals.map(pfilter, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'enumerate')
@wraps(builtins.enumerate)
def enumerate(collateral, start=0, keep_errors=False):
    penumerate = partial(builtins.enumerate, start=start)
    return collateral.collaterals.map(penumerate, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'sorted')
@wraps(builtins.sorted)
def sorted(collateral, /, *, key=None, reverse=False, keep_errors=False):
    psorted = partial(builtins.sorted, key=key, reverse=reverse)
    return collateral.collaterals.map(psorted, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'zip')
@wraps(builtins.zip)
def zip(collateral, /, *args, keep_errors=False, **kwargs):
    pzip = lambda it: zip(it, *args, **kwargs)
    return collateral.collaterals.map(pzip, keep_errors=keep_errors)

#delattr, setattr, getattr, hasattr
@partial(_globals.__setitem__, 'delattr')
@wraps(builtins.delattr)
def delattr(collateral, attr, keep_errors=False):
    pdelattr = lambda elt: builtins.delattr(elt, attr)
    collateral.collaterals.map(pdelattr, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'getattr')
@wraps(builtins.getattr)
def getattr(collateral, attr, default=missing, /, keep_errors=False):
    if default is missing:
        pgetattr = lambda elt: builtins.getattr(elt, attr)
    else:
        pgetattr = lambda elt: builtins.getattr(elt, attr, default)
    return collateral.collaterals.map(pgetattr, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'hasattr')
@wraps(builtins.hasattr)
def hasattr(collateral, attr, keep_errors=False):
    phasattr = lambda elt: builtins.hasattr(elt, attr)
    return collateral.collaterals.map(phasattr, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'setattr')
@wraps(builtins.setattr)
def setattr(collateral, attr, value, keep_errors=False):
    psetattr = lambda elt: builtins.setattr(elt, attr, value)
    collateral.collaterals.map(psetattr, keep_errors=keep_errors)

#format, round
@partial(_globals.__setitem__, 'round')
@wraps(builtins.round)
def round(collateral, ndigits=None, keep_errors=False):
    pround = partial(builtins.round, ndigits=ndigits)
    return collateral.collaterals.map(pround, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'format')
@wraps(builtins.format)
def round(collateral, format_spec='', /, keep_errors=False):
    pformat = lambda value: builtins.format(value, format_spec)
    return collateral.collaterals.map(pformat, keep_errors=keep_errors)

#isinstance, issubclasso
@partial(_globals.__setitem__, 'isinstance')
@wraps(builtins.isinstance)
def isinstance(collateral, class_or_tuple, /, keep_errors=False):
    pisinstance = lambda obj: isinstance(obj, class_or_tuple)
    return collateral.collaterals.map(pisinstance, keep_errors=keep_errors)
@partial(_globals.__setitem__, 'issubclass')
@wraps(builtins.issubclass)
def issubclass(collateral, class_or_tuple, /, keep_errors=False):
    pissubclass = lambda cls: issubclass(cls, class_or_tuple)
    return collateral.collaterals.map(pissubclass, keep_errors=keep_errors)

@partial(_globals.__setitem__, 'print')
@wraps(builtins.print)
def print(collateral, keep_errors=False, **kwargs):
    pprint = partial(builtins.print, **kwargs)
    collateral.collaterals.map(pprint, keep_errors=keep_errors)

#compile, eval, exec
#not implemented

#unary types and functions
def mapper(unary):
    @wraps(unary)
    def aux(collateral, keep_errors=False):
        return collateral.collaterals.map(unary, keep_errors=keep_errors)
    aux.__name__ = unary.__name__
    aux.__doc__ = "Collateral application of {name}:\n\n{doc}".format(name=unary.__name__, doc=unary.__doc__)
    return aux
for unary in (
    bool, bytearray, bytes, complex, dict, float, frozenset, int, list, set, str, tuple, type,
    abs, all, any, ascii, bin, callable, chr, classmethod, dir, hash, hex, id, iter, len, max, memoryview, min, next, oct, ord, property, repr, reversed, staticmethod, vars
):
    _globals[unary.__name__] = mapper(unary)

globals().update(_globals)
__all__ = ['__all__', '__dir__']
__all__.extend(_globals.keys())
__dir__ = lambda: __all__

