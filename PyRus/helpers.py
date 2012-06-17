from functools import wraps
def of_type(type, val):
    assert isinstance(val, type), "Value was of type {} instead".format(val.__class__.__name__)
    return val

def updated(d, **kwargs):
    d2 = dict(d)
    d2.update(kwargs)
    return d2
