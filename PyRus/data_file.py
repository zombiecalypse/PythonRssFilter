import json, os.path
def read_config(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(_default_config, f)
    with open(filename) as f:
        return _validate_format(json.load(f))

_default_config = dict(
        new_name = 'Merged RSS'
        )

def _validate_format(dict):
    assert "url" in dict, "Config must provide url"
    assert "output" in dict, "Config must provide output path"
    assert "new_name" in dict, "Config must provide output name"
    return dict
