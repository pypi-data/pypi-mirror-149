__description__ = "dict implementation supporting attribute access, recursion, json, hashable, subclass, metaclass"
__version__ = "1.0.3rc6"
__long_description__ = """

▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██████╗▒▒██╗▒██████╗████████╗▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██╔══██╗███║██╔════╝╚══██╔══╝▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██║▒▒██║╚██║██║▒▒▒▒▒▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██║▒▒██║▒██║██║▒▒▒▒▒▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██████╔╝▒██║╚██████╗▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒╚═════╝▒▒╚═╝▒╚═════╝▒▒▒╚═╝▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒

d1ct is a hybrid object/mapping.

 - directly inherited from dict
 - accessible by attribute.   o.x == o['x'] 
 - This works also for all corner cases.
 - json.dumps json.loads
 - vars() works on it!
 - hashable! (should not yet trust on it, though)
 - autocomplete works even if the objects comes from a list
 - best of all, it works recursively. So all inner dicts will become d1cts too.
 
 
 - no downsides? 
 
    o hell yeah.  
    the performance which is a magnitude slower (~6x) than builtin dict.
    to give you an impression of timeit results: 
        
        d1ct :  [0.26289230000111274, 0.2543108999961987, 0.25743720002355985, 0.2560539000260178, 0.2556736999831628, 0.25478869999642484, 0.2541010999993887, 0.2552008999919053, 0.2651131000020541, 0.25846979999914765]
        
        dict :  [0.04928750000544824, 0.04902900001616217, 0.049049399996874854, 0.050644999981159344, 0.04969919999712147, 0.04940899999928661, 0.0497540999785997, 0.04959690000396222, 0.04939249999006279, 0.04959330000565387]
 
    
    - this implementation might have effects which i did not notice yet.
   
 
    Usage/Testing:
    
    from d1ct import Dict
    
    d = Dict({"a": 1, "b": {"b1": "c1"}}, kw1=1, kw2=2)
    d["z1"] = {}
    d.z1.update({"yyyy": 2323232})
    
    assert d.a == d['a'] == 1
    assert d.z1 == d['z1'] == {'yyyy': 2323232}
    assert d == {'a': 1, 'b': {'b1': 'c1'}, 'kw1': 1, 'kw2': 2, 'z1': {'yyyy': 2323232}}
    assert type(d.z1) is Dict
    
    d.z1.update({"yyyy": 2323232})
    assert type(d.z1.yyyy) is int
    
    d.z1.update({"yyyy": {"xbb": [1, 2, 23]}})
    assert type(d.z1.yyyy) is Dict
    
    import json
    json.dumps(d)
    
    d |= {'more_keys': {'really': 'yeah!'}}
    
    assert d == {'a': 1,'b': {'b1': 'c1'}, 'kw1': 1,'kw2': 2, 'z1': {'yyyy': {'xbb': [1, 2, 23] } },'more_keys': {'really': 'yeah!'} }
    
"""


from collections.abc import Mapping as _Mapping, Sequence as _Sequence

_DEBUGMODE = False

__all__ = ["Dict"]


class Dict(dict):
    """
    One of the only data types in python which is:
     - directly inherited from dict
     - accessible by attribute.
     - This works also for all corner cases.
     - json.dumps json.loads
     - vars() works on it!
     - hashable! (should not yet trust on it, though)
     - autocomplete works even if the objects comes from a list
     - best of all, it works recursively. So all inner dicts will become addicts too.
       How great this addict is, is TBD
       when code breaks, alwasys  first try commenting this out and try normal dicts.
       as this implementation might have effects which i did not notice yet.
    """

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        if _DEBUGMODE:
            _dbgprint(self, *args, **kwargs)
        super().__init__()
        for k, v in dict(*args, **kwargs).items():
            super().__setitem__(k, _wrap(v))
        super().__setattr__("__dict__", self)

    def __setitem__(self, key, value):
        if _DEBUGMODE:
            _dbgprint(self, key, value)
        super().__setitem__(key, _wrap(value))

    def __setattr__(self, key, value):
        if _DEBUGMODE:
            _dbgprint(self, key, value)
        super().__setitem__(key, _wrap(value))

    def __missing__(self, key):
        if _DEBUGMODE:
            _dbgprint(self, key)
        raise AttributeError(f"{self.__class__} has no attribute '{key}'")

    def __getattribute__(self, item):
        if _DEBUGMODE:
            print("__getattribute__", item)
        return super().__getattribute__(item)

    def __call__(self, *args, **kwargs):
        if _DEBUGMODE:
            _dbgprint(self, *args, **kwargs)
        return self.__class__(*args, **kwargs)

    def update(self, *a, **kw):
        """
        small change compared to dicts .update method
        """
        if _DEBUGMODE:
            _dbgprint(self, *a, **kw)
        d = {}
        if len(a) > 0:
            a = a[0]
            d.update(a)
            if isinstance(a, (str, bytes)):
                pass
        if kw:
            d.update(kw)
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = Dict(v)
            elif isinstance(v, (list, set, tuple, frozenset)):
                d[k] = [Dict(i) for i in v]
        super(Dict, self).update(d)

    def __hash__(self, opt=None):
        if _DEBUGMODE:
            _dbgprint(self, opt=opt)
        tohash = set()
        for i, k in enumerate(self):
            v = self[k]
            if not isinstance(v, (list, set)):
                tohash.add(v)
            else:
                [tohash.add(iv) for iv in v]
        return hash(frozenset(tohash))

    def __dir__(self):
        if _DEBUGMODE:
            _dbgprint(self)
        return list(map(str, super(Dict, self).__dir__()))


def _wrap(v):
    if isinstance(v, _Mapping):
        v = Dict(v)
    elif isinstance(v, _Sequence) and not isinstance(
        v, (str, bytes, bytearray, set, tuple)
    ):
        v = list([_wrap(x) for x in v])
    return v


def _dbgprint(obj, *a, **kw):
    """
    dumb debug printer

    :param obj: instance when called from a method ( like _dbgprint(self, *args, **kwargs) )
    :param *a: args
    :param **kw: kwargs
    :return: None
    """

    import inspect

    caller = inspect.stack()[1].function
    callercls = obj.__class__.__name__
    astr, kwstr, cstr = "", "", ""
    if len(a) > 0:
        astr = str(a)[1:-1]
    if len(a) <= 1:
        astr = astr.replace(",", "")
    if len(kw) > 0:
        for k, v in kw.items():
            kwstr += k.replace("'", "")
            kwstr += "="
            kwstr += str(v)
    if astr and kwstr:
        cstr = ", "
    print(f"called  {callercls}.{caller}({astr}{cstr}{kwstr})")
