import json, os.path
def read_config(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump(_default_config, f)
    with open(filename) as f:
        return json.load(f)

_default_config = dict(
        new_name = 'Merged RSS'
        )
