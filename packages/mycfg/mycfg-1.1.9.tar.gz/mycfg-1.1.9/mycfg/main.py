import yaml

import meta
from mycfg import const
from mycfg.state import State

with open(const.CONFIG_FILE) as f:
    file = yaml.full_load(f)
    print(file)

def main():
    State.config = file
    meta.load_meta()
    # install()


main()
