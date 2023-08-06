
class Setup(object):
    __slots__ = ('_notcollaterable_names', '_notprocedure_names', '_collaterize_prefix')
    def __init__(self):
        self.reset()
    def reset(self):
        #set of attribute name to protect, in addition to __class__.__dict__.keys()
        self.notcollaterable_names = {
            '__bool__',
            '__class__',
            '__complex__',
            '__float__',
            '__format__',
            '__getattribute__',
            '__hash__',
            '__hex__',
            '__index__',
            '__int__',
            '_ipython_key_completions_',
            '__len__',
            '__nonzero__',
            '__oct__',
            '__qualname__',
            '__repr__',
            '__slots__',
            '__str__',
            '__unicode__',
        }
        self.notprocedure_names = {
            'get',
            'pop',
            '__getattribute__',
            '__getattr__',
            '__getitem__',
        }

        self._collaterize_prefix = "_collateral_"

    @property
    def notcollaterable_names(self):
        return self._notcollaterable_names
    @notcollaterable_names.setter
    def notcollaterable_names(self, names):
        self._notcollaterable_names = set(names)

    @property
    def notprocedure_names(self):
        return self._notprocedure_names
    @notprocedure_names.setter
    def notprocedure_names(self, names):
        self._notprocedure_names = set(names)

    @property
    def collaterize_prefix(self):
        """Prefix to prepend to method name when collaterized, if the method name is protected.
        """
        return self._collaterize_prefix
    @collaterize_prefix.setter
    def collaterize_prefix(self, prefix):
        self._collaterize_prefix = prefix

setup = Setup()
