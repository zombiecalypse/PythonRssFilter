import os.path
import filters
def read_config(filename):
    if isinstance(filename, basestring):
        return _read_from_filename(filename)

    return _read_from_file(filename)

def _read_from_file(f):
    return eval (compile(" ".join(map(str.strip, f.readlines())).strip(), f.name, 'eval'), filters.__dict__)


def _read_from_filename(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write(_default_config)
    with open(filename) as f:
        return eval (compile(" ".join(f.readlines()), filename, 'eval'), filters.__dict__)

_default_config = """
GetFeed("http://xkcd.com/rss.xml") >> BlackListFilter('hitler') >> FileSink('xk.rss', title = 'Merged RSS')
"""

