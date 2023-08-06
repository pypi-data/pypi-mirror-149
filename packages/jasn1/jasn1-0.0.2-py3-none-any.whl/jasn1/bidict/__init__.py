from __future__ import annotations

import warnings

class BiDict(dict):

    def __init__(self, *args, force: bool = False, inverse: BiDict = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._force = force
        if inverse is None:
            self._inverse = BiDict({self[x]: x for x in self}, force=self._force, inverse=self)
        else:
            self._inverse = inverse

    def __setitem__(self, key, val, cascade=True):
        if val in self._inverse and key != self._inverse[val]:
            if not self._force:
                raise ValueError("Values in a BiDict must be unique if the 'force' flag is not set")
            else:
                try:
                    _key = self._inverse[val]
                    self.__delitem__(_key, cascade=False)
                except KeyError as e:
                    pass

        dict.__setitem__(self, key, val)
        if cascade:
            self._inverse.__setitem__(val, key, cascade=False)
        else:
            try:
                _key = self._inverse[val]
                assert _key == key
            except (KeyError, AssertionError) as e:
                warnings.warn("Manually overriding the 'cascade' argument will cause data inconsistency.")

    def __delitem__(self, key, cascade=True):
        try:
            val = self[key]
        except KeyError as e:
            pass
        dict.__delitem__(self, key)

        if cascade:
            self._inverse.__delitem__(val, cascade=False)
        else:
            try:
                _key = self._inverse[val]
                warnings.warn("Manually overriding the 'cascade' argument will cause data inconsistency.")

            except KeyError as e:
                pass

    def rget(self, value):
        return self._inverse.get(value)

    def rdel(self, value):
        try:
            del self._inverse[value]
        except KeyError as e:
            pass
