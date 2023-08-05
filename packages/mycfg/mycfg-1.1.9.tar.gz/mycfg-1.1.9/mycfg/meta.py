import json

from mycfg import const
from mycfg.state import State

default_meta = {
    "package_manager": "",
    "package_managers": [],
    "environment": "",
    "installed_units": [],
    "installed_packages": [],
}


def load_meta():
    with open(const.META_FILE) as f:
        State.meta = json.load(f)
    for key in default_meta:
        if key not in State.meta:
            State.meta[key] = default_meta[key]


def set(key, value):
    State.meta[key] = value


def get(key):
    return State.meta.get(key)


def append(key, value):
    State.meta.get(key).append(value)

def remove(key, value):
    State.meta.get(key).remove(value)


def save():
    with open(const.META_FILE, 'w') as f:
        json.dump(State.meta, f)
