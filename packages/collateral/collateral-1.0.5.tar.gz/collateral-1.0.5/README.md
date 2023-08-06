# Collateral
This tool package provides a simple way to manipulate several objects with similar behaviors in parallel.
```python
import collateral as ll
```

## Motivation
Often, in software development, we define objects that should behave the same way as known objects.
Typically, a class implementing `collections.abc.MutableMapping` should behave similarly to `dict`.
When developing such objects, we might want to quickly check this behavior similarity (or dissimilarity)
in an interactive way, without having to write down many automatic tests.
The collateral package has been designed for this purpose, to be used within ipython.

We give a constructor a list of objects (typically 2), called _collaterals_
(each of any type, but not all `None`),
and we manipulate them, using the resulting `Collateral` object,
as if there was only one object.
```python
#What is the difference between lists and tuples?
C = ll.Collateral([3, 4, 3], (3, 4, 3))
C.count(3)
C[0]
```

## How it works
Intuitively, the methods and attributes of a `Collateral` objects
are the methods and attributes of its collaterals,
which are applied pointwise on each of them,
in order to form a new `Collateral` object that gathers the results.
<!---
(If the method is a _procedure_ that do not return any value, or more precisely returns `None`,
then all collaterals of the newly built `Collateral` object would be `None`,
whence the resulting `Collateral` object is replaced by `None`.)
--->
Hence, getting an attribute named `attr` or calling a method named `meth` is the same as
1.	getting `attr` from, or calling `meth` on each of the collaterals, respectively;
2.	and gathering the results in a new `Collateral` object.
Methods/attributes with such behavior are said _pointwise_.
```python
C.count(3)	#both have a `count` method that do the same
C[2]				#both support indexing
```
During step 2. above, if each pointwise call returns `None`,
then no `Collateral` object is built
and the (single) value `None` is returned.
However, step 1. is still performed pointwise.
```python
D = ll.Collateral([3, 4], [4, 3])
D.append(5)	#returns None
repr(D)			#shows that 5 has been appended to both collaterals of D
```

By contrast, a few other methods and attributes of `Collateral` objects
are specific to the `Collateral` object and are not applied pointwise.
We say that they are _transversal_.
All the `Collateral` objects have the same transversal methods/attributes.
Some are Python requirement (_e.g._, `__class__`, `__dict__`),
while other offer transversal capabilities on collaterals,
namely, capability that is not pointwise (_e.g._, `_collaterize` (a static method for internal use), `__getattr__`).
Among them, the property `collaterals` returns the tuple of collaterals.
```python
C.collaterals	#returns the tuple of collaterals
C.__repr__()	#returns a string, not a `Collateral` object formed by the pointwise representations of collaterals
C.__dict__		#returns the __dict__ of the `Collateral` object
```

### Pointwise methods and attributes
A method/attribute exists in a `Collateral` object
if it is a method/attribute of at least one of the collaterals.
This is true for most of the method name,
however, some exceptions exist:
1.	If the method/attribute name is equal to a transversal method/attribute name,
	then it is renamed by prepending the string `_collaterize_prefix`,
	which is a transversal class attribute of `Collateral` objects.
	```python
	C._collaterize_prefix
	C._collateral___repr__()
	```
2.	If the method/attribute name is expected to return a result of some precise type
	(_e.g_, `__int__`, `__len__`, `__hash__`)
	then, the `_collaterize_prefix` is appended as well.
	The list of such method/attribute names is store in the `_notcollaterables`
	transversal class attribute of `Collateral` objects.
	```python
	C._notcollaterables
	C._collateral___len__()
	```

An non-method atrribute results in a property in the `Collateral` object.
If the same attribute name corresponds to a callable method in some collaterals
and to a non-callable attribute in some other,
then it is considered as non-callable, namely, it results in a property
(whose return value might be callable).

####	Pointwise additional methods
Some pointwise methods do not originate from the set of methods of the collaterals,
but are rather proposed by the `Collateral` object for easier manipulation.
There are three such common pointwise methods:
+	`collateral_map`: applies a function to each collaterals.
	```python
	C.collateral_map(len)
	```
+	`collateral_filter`: applies a filter on each collaterals.
	```python
	C.collateral_filter(bool)
	```
+	`collateral_call`: calls each collaterals (assumed callable) with given arguments which can be specified precisely.
	```python
	C.collateral_map(lambda c: getattr(c, 'count')).collateral_call((3, 4))
	```

### Transversal methods and attributes

####	Class attributes
+	`collaterals`: the tuple of collaterals.
	Actually, this is not a tuple instance,
	but an instance of a subclass, that provides the `all_equal` method,
	for testing whether all collaterals are equal (in the sense of `__eq__`).
	```python
	C.collaterals.all_equal()
	D.collaterals.all_equal()
	D.collateral_map(sorted).collaterals.all_equal()
	```
+	`_notcollaterables`: a frozen set of method/attribute names, that should be renamed for pointwise application.
+	`_collaterize_prefix`: a string which is used as prefix for renaming non-collaterables
	(c.f., `_notcollaterables`) and transversal methods/attributes
+	`collateral_build`: a static method for building `Collaterable` objects.
	It could have been called `__new__`, but has not for reasons detailed in its documentation.
+	`_collaterize`: a static internal method for creating pointwise methods/properties.

####	Magic methods
+	`__getattr__`
+	`__hash__`: always defined, but returns the hash of the tuple of collaterals which might be undefined
+	`__repr__`: useful for quick visualization of `Collateral` objects.
+	`__dir__`: useful for autocompletion of attributes
+	`_ipython_key_completions_`: useful for autocompletion of keys.
	It is always defined, although not all `Collectable` objects support getiteming.
	For such objects, the returned iterable is always empty.


## Examples:
```python
import collections

class MyDict(collections.abc.Mapping):
	def __init__(self, source_dict):
		self._dict = dict(source_dict)
	def __getitem__(self, k):
		return self._dict[k]
	def __iter__(self):
		return iter(self._dict)
	def __len__(self):
		return len(self._dict)

d = { 3: True, "foo": { 2: None }, True: "foo" }
md = MyDict(d)
C = ll.Collateral(d, md)
repr(C)

C.keys()				#returns ll.Collateral(d.keys(), md.keys())
C.values()			#returns ll.Collateral(d.values(), md.values())
C[3]						#returns ll.Collateral(d[3], md[3])
C[True]					#returns ll.Collateral(d[True], md[True])

C.__init__({})	#call d.__init__({}) and md.__init__({}) and returns None
C.get(3, False)	#3 is still a key of d but not of md (because of the divergence of __init__)
C["bar"] = 0		#setitem does not exist for md
```
