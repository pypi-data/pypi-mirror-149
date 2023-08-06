"""
This module offers a tool to manipulate several objects behaving
similarly in parallel.  To do so, the objects to manipulate,
called _collaterals_, are gathered in a particular `Collateral`
object, whose attributes and methods allow a user to manipulate
all collaterals in parallel.

Technically speaking, for each attribute name which is present
in each of the collaterals, there is a corresponding attribute
in the Collateral object.  If the attribute is a method in each
of the collaterals, then so is it in the Collateral object.  In
this case, this Collateral's method is a wrapper which will call
the method on each of the collaterals, with the given arguments.
With the exception of only a few dunder methods (see below), the
attribute correspondence preserve the name, namely the attribute
names of Collateral objects are the attribute names shared by
all the collaterals.  The exceptions concern dunder methods
whose return type is enforced (e.g., __hash__, __bool__), making
it impossible to return a Collateral gathering the results.  See
the setup.notcollaterable_names to get and/or alter the set of
protected names.  For each such protected names, there is a
corresponding method in the Collateral object, whose named is
f"{setup.collaterize_prefix}{name}" where name is the original
attribute name (in the surprising cases of conflict, the prefix
setup.collaterize_prefix is prepended as many times as needed to
get a non-preexistent name).

Besides the attributes originating from their collaterals, each
Collateral object has two class attributes (namely 'collaterals'
and '__slots__') and offers a few methods.

Collateral class attributes
---------------------------
collaterals: CollateralTuple
    A CollateralTuple (or subclass) instance, which stores the
    collaterals, and offers a few methods to manipulate them.
__slots__: tuple
    The empty tuple.

Collateral not-collaterized methods
-----------------------------------
__getattr__(self, attr: str) -> any
    The method calling getattr on each collaterals, with the
    given attribute name.
__eq__(self, other: any) -> bool
    The method testing equality of Collateral objects.
__hash__(self) -> int
    The method attempting to produce a hash for the Collateral
    objects.  This strongly relies on computing a hash of each
    collaterals and will thus fail in case some of them is not
    hashable.
__repr__(self) -> str
    The method producing a representation of the Collateral
    object.
__dir__(self) -> frozenset
    The method producing the frozenset resulting from the
    intersection of the dirs of the collaterals.
__init_subclass__(cls, **kwargs) -> NoneType
    The class method setting the Collateral subclass to use
    according to the collaterals to gather in it.

Examples
--------
>>> import collateral as ll
>>> C = ll.Collateral([3, 4, 5, 3], (4, 3, 5))
>>> C
Collateral< [3, 4, 5, 3] // (4, 3, 5) >
>>> C.count(4)
Collateral< 1 // 1 >
>>> C.count(3)
Collateral< 2 // 1 >
>>> D = C.collaterals.map(list)
>>> D
Collateral< [3, 4, 5, 3] // [4, 3, 5] >
>>> D.append(8)
>>> D
Collateral< [3, 4, 5, 3, 8] // [4, 3, 5, 8] >

"""
import collateral.tools as tools
import collateral.decorators as decorators
import collateral.exception as exception
import collateral.parameters as parameters
import collateral.collateral as collateral
import collateral.functions as functions

__version__ = "1.0.5"
__all__ = [ 'Collateral', 'CollateralError', 'tools', 'exception', 'decorators', 'collateral', 'functions' ]

Collateral = collateral.Collateral
CollateralError = exception.CollateralError
setup = parameters.setup
keep_errors = decorators.keep_errors

