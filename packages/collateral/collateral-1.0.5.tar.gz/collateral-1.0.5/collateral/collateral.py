import builtins, functools, itertools
from collateral.tools import ArgumentSpec, missing
from collateral.decorators import keep_errors
from collateral.exception import collateralErrorFactory
from collateral.parameters import setup

chain = itertools.chain
wraps = functools.wraps
reduce = functools.reduce

__all__ = ['BaseCollateral', 'Collateral']

class CollateralTuple(tuple):
    __slots__ = ()

    def map(self, f, notallnone=False):
        """Applies f on each element and gather the result within a Collateral object

        If an exception `e` is encountered when applying `f` on some element, then an
        exception of type extending both the type of `e` and the `CollateralError`
        `Exception` subclass is raised.  The raised exception has the arguments from
        `e` as first arguments, followed by a Collateral object gathering the pseudo-
        result of `f` on each element, where failure (exception raising) is replaced
        by exception returning — see examples below.

        Parameters
        ----------
        f: callable
            the method to apply on each collateral element.

        notallnone: bool, default=False
            whether to return None if all results are None or not.

        Returns
        -------
        Collateral object with `len(self)` elements.

        Raises
        ------
        CollateralError subclass when applying `f` on some element produces an error.

        Examples
        --------
        >>> C = Collateral(range(2, 3), range(7, 9))
        >>> type(C.collaterals)
        <class 'collateral.CollateralTuple'>
        >>> C.collaterals.map(len)
        Collateral< 1 // 2 >
        >>> C.collaterals.map(bool)
        Collateral< True // True >
        >>> D = C.collaterals.map(tuple)
        >>> D
        Collateral< (2,) // (7, 8) >
        >>> H = D.collaterals.map(hash)
        >>> isinstance(H, BaseCollateral)
        True
        >>> all(isinstance(c, int) for c in H.collaterals)
        True
        >>> D.collaterals.map(hash) == D._collateral___hash__()
        True
        >>> E = Collateral(range(3), 4, "abcde")
        >>> E.collaterals.map(len)
        Traceback (most recent call last):
            ...
        collateral.exception.CollateralTypeError: ("object of type 'int' has no len()", Collateral< 3 // TypeError("object of type 'int' has no len()") // 5 >)

        """
        #return Collateral(*map(f, self), notallnone=notallnone)
        #cannot use builtin map, because of catched inner StopIteration exception
        r = []
        first_exception = None
        for c in self:
            try:
                r.append(f(c))
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                r.append(e)
        r = Collateral(*r, notallnone=notallnone)
        if first_exception is not None:
            e = collateralErrorFactory(r, on_exception=first_exception)
            raise e
        return r
    def filter(self, f=bool, /):
        """Applies f to each element and gather the truthy results only in a Collateral object

        Parameters
        ----------
        f: callable
            the function to use to filter the collateral elements.

        Returns
        -------
        Collateral object, with at most `len(self)` elements.

        Raises
        ------
        CollateralError subclass when applying `f` to some element produces an error
        (see map method).

        Examples
        --------
        >>> C = Collateral(range(2, 3), range(7, 9))
        >>> C.collaterals.filter(bool) == C
        True
        >>> C.collaterals.filter(lambda r: len(tuple(r[:-1])))
        Collateral< range(7, 9) >
        >>> C.collaterals.filter(lambda r: False)
        Collateral<  >

        """
        #return Collateral(*map(f, self), notallnone=notallnone)
        #cannot use builtin map, because of catched inner StopIteration exception
        r = []
        results = []
        first_exception = None
        for c in self:
            try:
                res = f(c)
                if res:
                    r.append(c)
                results.append(res)
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                results.append(e)
        r = Collateral(*r, notallnone=False)
        if first_exception is not None:
            results = Collateral(*results, notallnone=False)
            e = collateralErrorFactory(r, results, on_exception=first_exception)
            raise e
        return r
    def enumerate(self, start=0):
        """Gathers the (index, element) pairs from the enumeration of self within a Collateral object

        Parameters
        ----------
        start: int, default=0
            the starting index (as for enumerate builtin).

        Returns
        -------
        Collateral object with `len(self)` elements, each being a pair (tuple) whose
        first coordinate is an index `i` (int) and the second coordinate is the
        corresponding element in `self`, namely `self[i]`.  The element order is
        preserved.

        Examples
        --------
        >>> C = Collateral([0, 2], True)
        >>> D = C.collaterals.enumerate()
        >>> D
        Collateral< (0, [0, 2]) // (1, True) >
        >>> D.collaterals.enumerate()
        Collateral< (0, (0, [0, 2])) // (1, (1, True)) >
        >>> E = Collateral([0, 2], (3, 8, 5))
        >>> E.collaterals.enumerate()
        Collateral< (0, [0, 2]) // (1, (3, 8, 5)) >
        >>> F = E.collaterals.map(enumerate)
        >>> F #doctest: +ELLIPSIS
        Collateral< <enumerate object at 0x...> // <enumerate object at 0x...> >
        >>> F.collaterals.map(list)
        Collateral< [(0, 0), (1, 2)] // [(0, 3), (1, 8), (2, 5)] >
        >>> E.collaterals.enumerate(start=2)
        Collateral< (2, [0, 2]) // (3, (3, 8, 5)) >

        """
        return Collateral(*enumerate(self, start=start))
    def call(
        self, argspecs, method=None,
        default_args=(), default_kwargs=(),
        common_pre_args=(), common_post_args=(), common_kwargs=(),
        notallnone=False,
        **other_common_kwargs
    ):
        """Calls each of the collateral elements with (possibly distinct) arguments

        Parameters
        ----------
        collateral: BaseCollateral
            the Collateral object on which to call.

        argspecs: iterable
            a specification of a partial mapping from indices of collaterals
            in `self` to `ArgumentSpec`s.  The partial mapping is defined as
            `dict(argspecs)` if it succeeds, or as `dict(enumerate(argspecs))`
            otherwise (assumed to succeed).

        method: str or None, default=None
            the name of a method to call (`str`) or `None`.  If `None`, the
            collaterals themselves are called (whence `method=None` should
            likely produce the same result as `method=__call__`).

        default_args: tuple, default=()
            a tuple of arguments to be used for collateral indices that do not
            have associated argument specification image in the above-defined
            mapping.

        default_kwargs: iterable, default=()
            a dictionary specification whose keys are all expected to be valid
            parameter identifiers, to be used as default list of keyworded
            arguments for collateral indices that do not have associated
            argument specification image in the above-mapping.

        common_pre_args: tuple, default=()
            a tuple of arguments to be prepended to the argument tuple of each
            argument specification defined by `argspecs`.

        common_post_args: tuple, default=()
            a tuple of arguments to be appended to the argument tuple of each
            argument specification defined by `argspecs`.

        common_kwargs: iterable
            a iterable of keyworded parameter to be added to the keyworded
            arguments of each specification defined by `argspecs`, with minor
            priority (namely, a keyworded parameter given in an argument
            specification will be preferred to a same-keyword parameter given
            in `common_kwargs`).

        notallnone: bool, default=False
            whether to return None instead of a Collateral with only None
            elements.

        other_common_kwargs: dict
            additionaly common keyworded parameters to update the mapping
            defined by the common_kwargs parameter.

        Notes
        -----
        When the mapping dictionary is defined, it is used as
        follows. We associate the collateral of index `i` (i.e.,
        `self.collaterals[i]`) with the value associated with the
        integer key `i` in the mapping dictionary, if any. This
        value is expected to be an argument specification
        (`ArgumentSpec`). If it does not exist, the default argument
        specification `ArgumentSpec(`default_args, default_kwargs)`
        is taken instead.

        Examples
        --------
        >>> l, r = [3, 2], [2, 3]
        >>> C = Collateral(l.append, r.append)
        >>> C.collaterals.call((8, 7), notallnone=True)
        >>> l, r
        ([3, 2, 8], [2, 3, 7])
        >>> C = Collateral(l, r)
        >>> C.collaterals.call((9, 0), method='append', notallnone=True)
        >>> C
        Collateral< [3, 2, 8, 9] // [2, 3, 7, 0] >
        >>> l, r
        ([3, 2, 8, 9], [2, 3, 7, 0])

        """
        try:
            argspecs = dict(argspecs)
        except TypeError:
            argspecs = dict(enumerate(argspecs))
        EmptyArgumentSpec = ArgumentSpec(default_args, default_kwargs)
        def pointwise_call(ic):
            #ic=(i,c) from collaterals of self.collaterals.enumerate()
            i, c = ic
            a = argspecs.get(i, EmptyArgumentSpec)
            if not hasattr(a, 'args') or not hasattr(a, 'kwargs'):
                a = ArgumentSpec((a,))
            if method:
                f = getattr(c, method)
            else:
                f = c
            return f(*common_pre_args, *a.args, *common_post_args, **dict(dict(common_kwargs, **other_common_kwargs), **a.kwargs))
        return self.enumerate().collaterals.map(pointwise_call, notallnone=notallnone)

    def join(self, *others):
        return Collateral(*self, *chain.from_iterable(o.collaterals for o in others))
    def add(self, *elements):
        return Collateral(*self, *elements)
    def drop(self, *avoided):
        return Collateral(*(c for c in self if c not in avoided))

    def all(self):
        return all(self)
    def any(self):
        return any(self)
    def all_equal(self):
        return self.map(lambda c: c == self[0]).collaterals.all()
    def reduce(self, f, initial=missing, /):
        if initial == missing:
            return functools.reduce(f, collaterals)
        return functools.reduce(f, collaterals, initial)
    def reversed(self):
        return Collateral(*reversed(self))

    def sorted(self, /, *, key=None, reverse=False):
        return Collateral(*sorted(self, key=key, reverse=reverse))
    def is_sorted(self, /, *, key=None, reverse=False):
        return list(self) == builtins.sorted(self, key=key, reverse=reverse)
    def min(self):
        return min(self)
    def max(self):
        return max(self)

class KeyableCollateralTuple(CollateralTuple):
    def transversal_keys(self, intersection=True):
        """Returns the set of keys of the elements

        Parameters
        ----------
        intersection: bool, default=False
            Whether to keep keys shared by all the elements only
            or not.

        Examples
        --------
        >>> C = Collateral({ 0: True, 1: False, 'other': "bar", 'shared': "foo" }, { 1: False, 0: True, 'shared': "foo" })
        >>> for k in C:
        ...        print(k)
        ...        print(C[k])
        ...        print("---")
        Collateral< 0 // 1 >
        Collateral< True // False >
        ---
        Collateral< 1 // 0 >
        Collateral< False // True >
        ---
        Collateral< 'other' // 'shared' >
        Collateral< 'bar' // 'foo' >
        ---
        >>> for k in C.collaterals.transversal_keys():
        ...        print(k)
        ...        print(C[k])
        ...        print("---")
        0
        Collateral< True // True >
        ---
        1
        Collateral< False // False >
        ---
        shared
        Collateral< 'foo' // 'foo' >
        ---

        """
        if not self:
            return set()
        elif intersection:
            redop = set.intersection
        else:
            redop = set.union
        keys = reduce(redop, (set(e.keys()) for e in self))
        return keys

class BaseCollateral(object):
    """
    The base abstract class for `Collateral` all objects. The
    constructor `__new__` builds a subclass implementing it, and
    instantiate this subclass.

    >>> C = Collateral( (9, 0, 9), [0, 9, 0] )
    >>> repr(C)
    'Collateral< (9, 0, 9) // [0, 9, 0] >'
    >>> C.collaterals.all_equal()
    False
    >>> C.count(0)
    Collateral< 1 // 2 >
    >>> C._collateral___len__()
    Collateral< 3 // 3 >
    >>> C.collaterals.map(len)
    Collateral< 3 // 3 >
    >>> C._collateral___len__() == C.collaterals.map(len)
    True
    >>> C[0]
    Collateral< 9 // 0 >
    >>> C[:1]
    Collateral< (9,) // [0] >
    >>> C.collaterals.map(set).collaterals.all_equal()
    True
    >>> D = C.collaterals.map(list)
    >>> repr(D)
    'Collateral< [9, 0, 9] // [0, 9, 0] >'
    >>> D.append(8)
    >>> repr(D)
    'Collateral< [9, 0, 9, 8] // [0, 9, 0, 8] >'
    >>> D.collaterals.map(sorted).collaterals.all_equal()
    False
    >>> E = D.collaterals.map(lambda c: getattr(c, 'append'))
    >>> E.collaterals.call((0, 9), notallnone=True)
    >>> D.collaterals.map(sorted).collaterals.all_equal()
    True
    >>> repr(D)
    'Collateral< [9, 0, 9, 8, 0] // [0, 9, 0, 8, 9] >'
    >>> D.pop()
    Collateral< 0 // 9 >
    >>> repr(D)
    'Collateral< [9, 0, 9, 8] // [0, 9, 0, 8] >'
    """
    __slots__ = ()
    collaterals = CollateralTuple()

    #MAGICS
    def __getattr__(self, attr):
        """
        >>> class A:
        ...        pass
        >>> l, r = A(), A()
        >>> C = Collateral(l, r)
        >>> l.foo = "bar"
        >>> r.foo = "rab"
        >>> C.foo
        Collateral< 'bar' // 'rab' >
        >>> "foo" in dir(C)
        True
        >>> class B:
        ...        def __dir__(self):
        ...            return []
        >>> l, r = B(), B()
        >>> C = Collateral(l, r)
        >>> l.foo = "babar"
        >>> r.foo = "rabab"
        >>> C.foo
        Collateral< 'babar' // 'rabab' >
        >>> "foo" in dir(C)
        False
        """
        f = lambda c: getattr(c, attr)
        return self.collaterals.map(f, notallnone=False)
    def __eq__(self, other):
        """
        >>> l, r = [2, 3], [2, 3]
        >>> C = Collateral((3, 4, 5), l)
        >>> D = Collateral((3, 4, 5), l)
        >>> C == D
        True
        >>> E = Collateral((3, 4, 5), r)
        >>> C == E
        True
        >>> r.append(2)
        >>> C == E
        False
        """
        if not isinstance(other, __class__):
            return False
        return self.collaterals == other.collaterals
    def __hash__(self):
        """
        >>> C = Collateral((2, 3), "foobar", True, False, None, "9")
        >>> hash(C) == C.__hash__()
        True
        >>> isinstance(hash(C), int)
        True
        >>> D = Collateral([])
        >>> hash(D)
        Traceback (most recent call last):
            ...
        TypeError: unhashable type: 'list'
        """
        return hash((self.__class__.__name__, self.collaterals))
    def __repr__(self):
        """
        >>> C = Collateral((3, 4), [3, 4])
        >>> repr(C) == C.__repr__()
        True
        >>> isinstance(repr(C), str)
        True
        >>> repr(C)
        'Collateral< (3, 4) // [3, 4] >'
        >>> D = Collateral(object(), dict(), set(), tuple(), list(), None)
        >>> len(repr(D).replace(' // ', '|').split('|')) == len(D.collaterals)
        True
        """
        return f"{self.__class__.__name__}< {' // '.join(map(repr, self.collaterals))} >"
    def __dir__(self):
        """
        >>> class A:
        ...        a_class_attribute = frozenset((3, 4))
        ...        def _a_hidden_attribute(self):
        ...            return False
        ...        def a_method(self):
        ...            return True
        ...        @property
        ...        def a_property(self):
        ...            return None
        ...        @classmethod
        ...        def a_class_method(cls):
        ...            return cls.__name__
        ...        @staticmethod
        ...        def a_static_method():
        ...            return "Good job!"
        ...        def __repr__(self):
        ...            return repr(self.foo) if hasattr(self, 'foo') else 'no foo found'
        >>> l, r = A(), A()
        >>> C = Collateral(l, r)
        >>> dir(C) == C.__dir__()
        True
        >>> for k in ['a_class_attribute', '_a_hidden_attribute', 'a_method', 'a_property', 'a_class_method', 'a_static_method', '__repr__', f"{setup.collaterize_prefix}__repr__" ]:
        ...        assert k in dir(C), (k, dir(C))
        >>> for k in dir(C):
        ...        assert isinstance(k, str)
        ...        assert hasattr(C, k)
        >>> C
        Collateral< no foo found // no foo found >
        >>> C.foo = "bar"
        >>> "foo" in dir(C)
        True
        >>> C
        Collateral< 'bar' // 'bar' >
        """
        res = set(__class__.__dict__.keys())
        res = res.union(self.__class__.__dict__.keys())
        if self.collaterals:
            res = res.union(reduce(set.intersection, map(set, map(dir, self.collaterals))))
        res = sorted(res)
        return res

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__( **kwargs)
        if cls.collaterals and hasattr(cls, 'keys') and hasattr(cls, '__getitem__'):
            cls.collaterals = KeyableCollateralTuple(cls.collaterals)
            def _ipython_key_completions_(self):
                return self.collaterals.transversal_keys()
            cls._ipython_key_completions_ = _ipython_key_completions_

def pointwise_attribute(attrname, iscallable=True, leadcls=None):
    """
    Defines a method that applies pointwise on each of the
    collaterals. It is not a function decorator, as the `attrname`
    argument is expected to be a string rather than a function.
    Nevertheless, it could be thought as an attribute decorator,
    applied on the `attrname`-named attribute of each collaterals
    of the `self`, the first argument of the returned method.

    +    attrname: a method name (`str`).
    +    iscallable: a Boolean indicating whether `attrname` correspond
        to a callable attribute of all collaterals. If `False`, then
        the resulting method is returned as a property.
    +    leadcls: a type or `None`. If the former case, the type is
        used for wrapping the resulting method with the `leadcls`
        attribute named `attrname` if any and callable.
    """
    notallnone = attrname not in setup.notprocedure_names
    if iscallable:
        def overloaded(self, *args, **kwargs):
            if any(isinstance(c, BaseCollateral) for c in chain(args, kwargs.values())):
                g = lambda i: (lambda arg: arg.collaterals[i] if isinstance(arg, BaseCollateral) else arg)
                h = lambda i: (lambda kwarg: (kwarg[0], kwarg[1].collaterals[i] if isinstance(kwarg[1], BaseCollateral) else kwarg))
                f = lambda ic: getattr(ic[1], attrname)(*map(g(ic[0]), args), **dict(map(h(ic[0]), kwargs.items())))
                return self.collaterals.enumerate().collaterals.map(f, notallnone=notallnone)
            else:
                f = lambda c: getattr(c, attrname)(*args, **kwargs)
                return self.collaterals.map(f, notallnone=notallnone)
    else:
        def overloaded(self):
            f = lambda c: getattr(c, attrname)
            return self.collaterals.map(f, notallnone=notallnone)
    wrapped = getattr(leadcls, attrname, None)
    if callable(wrapped):
        overloaded = wraps(wrapped)(overloaded)
    doc = getattr(overloaded, '__doc__', False)
    overloaded.__name__ = attrname
    overloaded.__doc__ = f"Pointwise overload of {attrname} in Collateral."
    if doc:
        overloaded.__doc__ = f"""{overloaded.__doc__}
/!\ Documentation and signature have been obtained by wrapping the method {overloaded.__name__} of the first of the collaterals.
    The other collaterals signature/documentation could be different.
-----

{doc}
        """
    if not iscallable:
        overloaded = property(overloaded)
    return overloaded

def Collateral(*collaterals, notallnone=False):
    """
    A constructor of `Collateral` objects. The function builds a
    subclass implementing `BaseCollateral` and returns an
    instantiation of the subclass. This has one exception: when
    all given collaterals are `None` and the `notallnone` argument
    is `True`, then the function returns the value `None`. This
    includes the case of an empty tuple of collaterals.

    +    collaterals: a tuple of objects to manipulate in parallel.
    +    notallnone: a Boolean indicating whether to return `None`
        when all given collaterals are `None` (if `True`) or not
        (if `False`). Default is `False`. This keyword is mostly
        used when calling a method on a `Collateral` object, in
        order to avoid procedure (method with no return) to pollute
        the output.

    >>> Collateral(True, False)
    Collateral< True // False >
    >>> Collateral(None, None, None, notallnone=True)
    >>> Collateral(notallnone=True)
    >>> Collateral(None, None, None, True, None, None, notallnone=True)
    Collateral< None // None // None // True // None // None >
    >>> Collateral(None, None)
    Collateral< None // None >
    """
    if notallnone and all(c is None for c in collaterals):
        return
    elif not collaterals:
        return type("Collateral", (BaseCollateral,), {})()
    lls = type(BaseCollateral.collaterals)(collaterals)

    mdict = dict(__slots__=(), collaterals=lls)
    classes = list(map(type, lls))
    leadcls = classes[0] if classes else None
    clsdirs = map(set, map(dir, classes))
    ndir = reduce(set.intersection, clsdirs)
    bases = (BaseCollateral,)
    protected_names = setup.notcollaterable_names.union(BaseCollateral.__dict__)
    for methname in ndir:
        name = methname
        while name in protected_names:
            name = f"{setup.collaterize_prefix}{methname}"
        iscallable = all(map(callable, map(lambda c: getattr(c, methname, None), classes)))
        mdict[name] = pointwise_attribute(methname, iscallable=iscallable, leadcls=leadcls)
    if '__dir__' in mdict:
        mdir = mdict['__dict__']
        mdict['__dir__'] = mdir + type(mdir)(('collaterals',))
    cls = type("Collateral", bases, mdict)
    self = object.__new__(cls)
    return self

