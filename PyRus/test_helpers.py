from functools import wraps

comp = lambda f,g: lambda x: f(g(x))

def Test(string = None):
    @wraps(Test)
    def wrapped(f):
        x = f if hasattr(f, 'func_name') else f.im_func
        s = x.func_name if string is None else string
        x.func_name = "test " + s
        return f
    if callable(string):
        x = string if hasattr(string, 'func_name') else string.im_func
        return Test(x.func_name)(string)
    return wrapped

def Given(*fs, **kwargs):
    @wraps(Given)
    def wrapping(f):
        @wraps(f)
        def wrapped(self):
            for fp in fs:
                fp(self)
            f(self)
        return wrapped
    if not 'name' in kwargs:
        kwargs['name'] = None
    return comp(Test(kwargs['name']), wrapping)

def only(set):
    assert len(set) == 1
    return next(iter(set))
